import os
import datetime

import webapp2
import webob.util
from google.appengine.api import logservice
from google.appengine.ext.webapp import blobstore_handlers
from webapp2_extras import sessions

from app import config
from app.util import template
from app.util import users


class HTTPTooManyRequests(webob.exc.HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the client has sent too many requests in a
    given amount of time.  Useful for rate limiting.

    From RFC 6585, "Additional HTTP Status Codes".

    code: 429, title: Too Many Requests
    """
    code = 429
    title = 'Too Many Requests'
    explanation = (
        'The client has sent too many requests in a given amount of time')


webob.exc.status_map[429] = HTTPTooManyRequests
webob.util.status_reasons[429] = HTTPTooManyRequests.title


class RequestHandler(webapp2.RequestHandler):
    """Base class to be used for all request handlers.

    This class provides a number of useful utility functions for rendering.

    Attributes:
      _log (bool): Whether to log request information. In this class, it just
        controls logging of rendered JSON output. Subclasses may use it to control
        other request-related logging, such as request parameters.
    """
    _log = True

    def enforce_ssl(self):
        if config.get('DEV_SERVER'):
            return
        if os.getenv('HTTPS', '') == 'on':
            return
        if self.request.headers.get('X-Forwarded-Proto', '') == 'https':
            return
        # redirect to HTTPS
        self.redirect(
            'https://%s%s' % (os.getenv('HTTP_HOST'), self.request.path_qs),
            abort=301,
        )

    def dispatch(self, *args, **kwargs):
        self.session_store = sessions.get_store(request=self.request)
        self.enforce_ssl()
        self.fetch_user()
        logservice.flush()
        self.response.headers.add_header('X-Frame-Options', 'DENY')
        self.response.headers.add_header('Content-Type', 'text/html; charset=UTF-8')
        self.response.headers.add_header('X-Content-Type-Options', 'nosniff')
        self.response.headers.add_header('X-XSS-Protection', '1; mode=block')
        try:
            webapp2.RequestHandler.dispatch(self, *args, **kwargs)
        except Exception:
            raise
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return template.get_jinja2(app=self.app)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    @webapp2.cached_property
    def messages(self):
        return self.session.get_flashes(key='_messages')

    def add_message(self, message, level=None):
        self.session.add_flash(message, level, key='_messages')

    def get_browser_locale(self):
        browserLocale = None
        header = self.request.headers.get('Accept-Language', '')

    def fetch_user(self):
        self.gae_user = users.get_current_user()
        self.logged_in = self.gae_user is not None

    def render_page(self, template_file, vars=None):
        """Render a template to the response output stream.

        Some variables are automatically provided to the template:

          CONFIG: provides access to app.config
          CURRENT_PAGE: contains the name of the template file (excluding path and
            extension).
          USER: provides access to the current user object

        Args:
          template_file: path to the template to render, relative to TEMPLATE_DIR.
          vars: additional template variables to set, if any. Note that the
            automatic variables will override any with the same name.
        """

        params = vars or {}
        params['CONFIG'] = config
        params['CURRENT_PAGE'] = os.path.splitext(os.path.split(template_file)[1])[0]
        params['CURRENT_TIME'] = datetime.datetime.now()
        params['path'] = self.request.path
        if not 'user' in params:
            params['user'] = self.user
        if not 'errors' in params:
            params['errors'] = {}

        rendered = self.jinja2.render_template(template_file, **params)
        self.response.out.write(rendered)

    def abort_not_found(self):
        """Render a standard "not found" page to the response output stream, and
        abort further processing with the 404 status code.

        Note that the default template is "404.html".
        """
        self.render_page('404.html')
        self.abort(404)


class BlobstoreUploadHandler(blobstore_handlers.BlobstoreUploadHandler, RequestHandler):
    """Blobstore upload handler subclass, which mixes RequestHandler and
    BlobstoreUploadHandler.
    """

    def __init__(self, *args, **kwargs):
        blobstore_handlers.BlobstoreUploadHandler.__init__(self, *args, **kwargs)
        RequestHandler.__init__(self, *args, **kwargs)


class RpcError(StandardError):
    """Representation of an RPC error."""
    pass


class FormError:
    error_dict = {}

    def addError(self, field, error_msg):
        if self.error_dict.get(field):
            self.error_dict[field].append(error_msg)
        else:
            self.error_dict[field] = [error_msg]

    def hasErrors(self):
        return len(self.error_dict.keys()) > 0

    def getErrors(self):
        return self.error_dict

    def clearErrors(self):
        self.error_dict = {}


def rpc_precondition(test, error):
    """Immediately abort processing with an error if a precondition is not met.

    Args:
      test: The precondition to test.
      error: The error message to raise.
    """
    if not test:
        raise RpcError(error)
