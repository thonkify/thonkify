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
        if len(translated_text) > 4000:
            logging.debug("Text too long, reporting characters 3999 - 4001: " + translated_text[3999:4001])
            translated_text = 'I\'m afraid I can\'t do that: <@' + self.request.POST.get('user_id') + '>'
        self.response.headers['Content-Type'] = 'application/json'
        data = {
            'response_type': 'in_channel',
            'link_names': 1,
            'text': translated_text
        }
        self.response.out.write(json_encode(data))
