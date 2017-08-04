from __future__ import unicode_literals

import logging
import webapp2
from webapp2_extras.routes import PathPrefixRoute
from google.appengine.ext import ndb

import app.config
from app import tasks
from app.tasks import webhooks

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'ezAK4re16aXlKG80cAMz'
}
application = ndb.toplevel(webapp2.WSGIApplication([
    PathPrefixRoute('/_webhooks', [
        webapp2.Route('/thonkify', webhooks.ThonkifyEndpoint),
        webapp2.Route('/debug', tasks.LogParams)
    ]),
    (r'.*', tasks.NotFound),
], debug=app.config.DEBUG, config=config))


def main():
    logging.getLogger().setLevel(logging.INFO)
    application.run()


if __name__ == "__main__":
    main()
