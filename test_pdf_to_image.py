import json
from unittest import TestCase, skip
import base64
from app import handler
import requests
import os

class Pdf2ImageTestCase(TestCase):

    def test_handler(self):

        with open("./40000_report.pdf", 'rb') as f:
            pdf_bytes = f.read()

        event = {
            'body': base64.b64encode(pdf_bytes).decode()
        }
        result = handler(event, None)
        self.assertEqual(len(json.loads(result['body'])), 1)
        self.assertEqual(result['statusCode'], 200)
        data = json.loads(result['body'])
        for i in range(len(data)):
            with open(f"./40000_report_{i}.png", "wb") as f:
                f.write(base64.b64decode(result['body'][i].encode('ascii')))

    def test_exception(self):

        result = handler({}, None)
        self.assertEqual(result['statusCode'], 406)

    @skip
    def test_handler_in_docker(self):
        """
        Ensure that Docker is running
        :return:
        """

        with open("./40000_report.pdf", 'rb') as f:
            pdf_bytes = f.read()

        event = {
            'pdf_bytes': base64.b64encode(pdf_bytes).decode()
        }

        result = requests.post("http://localhost:9000/2015-03-31/functions/function/invocations",
                               json=event)
        self.assertEqual(result.status_code, 200)

        res = json.loads(result.content)
        self.assertEqual(len(res['body']), 1)

        for i in range(len(res['body'])):
            with open(f"./40000_report_docker_{i}.png", "wb") as f:
                f.write(base64.b64decode(res['body'][i].encode('ascii')))

    def test_handler_live(self):


        url = os.environ.get('LIVE_URL')
        result = requests.post(url, json={})
        # print(result.json())
        self.assertEqual(result.status_code, 406)
        self.assertEqual(result.content, b'Unable to get page count.\nSyntax Error: Document stream is empty\n')

    def test_handler_live_with_data(self):

        with open("./40000_report.pdf", 'rb') as f:
            pdf_bytes = f.read()

        data = base64.b64encode(pdf_bytes).decode()

        url = os.environ.get('LIVE_URL')
        result = requests.post(url, data=data)
        self.assertEqual(200, result.status_code)
        images = result.json()
        self.assertEqual(images[0][:15], "iVBORw0KGgoAAAA")

    def test_lambda_event_live_error(self):

        event = base64.b64encode(b"Some Bytes").decode()
        url = os.environ.get('LIVE_URL')
        result = requests.post(url, data=event)
        self.assertEqual(result.status_code, 406)
