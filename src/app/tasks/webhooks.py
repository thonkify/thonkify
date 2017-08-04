import json
import logging
from app.tasks import RequestHandler
from app.util.helpers import json_encode
from app.controllers import thonkify

class ThonkifyEndpoint(RequestHandler):
    def post(self):
        logging.debug(self.request.POST)
        text_to_translate = self.request.POST.get('text', 'ThOnK')
        translated_text = thonkify.thonkify(text_to_translate)
        self.response.headers['Content-Type'] = 'application/json'
        data = {
            'response_type': 'in_channel',
            'text': translated_text
        }
        self.response.out.write(json_encode(data))
