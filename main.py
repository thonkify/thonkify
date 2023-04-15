from flask import Flask
from flask import request
from flask import json
import thonkify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return app.response_class(
        response = json.dumps({"success": True}),
        status = 200,
        mimetype = 'application/json'
    )

@app.route('/_webhooks/thonkify', methods=['POST'])
def thonkifyEndpoint():
    text_to_translate = request.form.get('text', 'ThOnK')
    translated_text = thonkify.thonkify(text_to_translate)
    if len(translated_text) > 4000:
        logging.debug("Text too long, reporting characters 3999 - 4001: " + translated_text[3999:4001])
        translated_text = 'I\'m afraid I can\'t do that: <@' + request.form.get('user_id') + '>'
    data = {
        'response_type': 'in_channel',
        'link_names': 1,
        'text': translated_text
    }
    return app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
