import itertools
import logging
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

SIX_LETTER_WORD_PATTERN = r'\b(\w{6})\b'
EMOJI_LIST = itertools.cycle(['😀', '😍', '😈'])

NON_VISIBLE_TAGS = [
    'style',
    'script',
    'head',
    'title',
    'meta',
    '[document]'
]

log = logging.getLogger('python-proxy')

HEADERS_TO_DELETE = [
    'Content-Encoding',
]


def add_emoji(content):
    """Add emodji after each 6 letter word """
    for element in content.find_all(['p', 'li']):
        if not getattr(element, 'text', None):
            continue
        text = element.text
        new_text = re.sub(
            SIX_LETTER_WORD_PATTERN,
            r'\1 {emoji}'.format(emoji=get_emoji()),
            text
        )
        element.string = new_text
        print(element.text)

    return content


def get_emoji():
    return next(EMOJI_LIST)


class ProxyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        response = requests.get(self.path)
        if response:
            content = self.modify_content(response.text)
            self.send_response(HTTPStatus.OK)
            self.send_headers(response.headers)
            self.wfile.write(bytes(str(content), "utf-8"))
        else:
            log.error(f'Error: {response.reason} {response.status_code}')
            self.send_error(response.status_code, response.reason)

    def clean_headers(self, headers):
        [
            headers.pop(header_to_delete, None)
            for header_to_delete in HEADERS_TO_DELETE
        ]
        return headers

    def send_headers(self, headers):
        """Need to clean some headers"""
        cleaned_headers = self.clean_headers(headers)
        for header, value in cleaned_headers.items():
            self.send_header(header, value)

        self.end_headers()

    def modify_content(self, html):
        soup = BeautifulSoup(html, 'lxml')
        content = add_emoji(soup)
        return content


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8080)
    server = HTTPServer(server_address, ProxyServer)
    server.serve_forever()
