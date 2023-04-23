from __future__ import annotations

import argparse

from flask import Flask
from flask import json
from flask import request

from thonkify import thonkify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return app.response_class(
        response=json.dumps({'success': True}),
        status=200,
        mimetype='application/json',
    )


@app.route('/_webhooks/thonkify', methods=['POST'])
def thonkify_endpoint():
    text_to_translate = request.form.get('text', 'ThOnK')
    translated_text = thonkify.thonkify(text_to_translate)
    if len(translated_text) > 4000:
        translated_text = 'I\'m afraid I can\'t do that: <@' + \
            request.form.get('user_id') + '>'
    data = {
        'response_type': 'in_channel',
        'link_names': 1,
        'text': translated_text,
    }
    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json',
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args(argv)

    kwargs = {'port': args.port, 'debug': True}
    app.run(host='0.0.0.0', **kwargs)
    raise SystemExit(1)


if __name__ == '__main__':
    raise SystemExit(main())
