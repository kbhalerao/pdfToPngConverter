import json
from pdf2image import convert_from_bytes
import gc
import base64
from io import BytesIO


def handler(event, context):
    """
    Receives a JSON event containing the following data
    event = {
        'body': base64.b64encode(pdf_bytes).decode()
    }
    :param event:
    :param context:
    :return: a list containing image data encoded as base64. To decode each image, do the following:
    image_bytes =  base64.b64decode(result[i].encode('ascii'))
    """
    try:
        pdf_bytes = event.get('body', dict())
        if pdf_bytes:
            imgs = list()
            decoded = base64.b64decode(pdf_bytes.encode())
            images = convert_from_bytes(decoded)
            for img in images:
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                buffered.seek(0)
                data_uri = base64.b64encode(buffered.read()).decode('ascii')
                imgs.append(data_uri)
                buffered.close()
                img.close()
            return {
                'statusCode': 200,
                'body': json.dumps(imgs),
                'headers': {'Content-Type': 'application/json'},
            }

        return {
            'statusCode': 406,
            'body': "No Data",
            'headers': {'Content-Type': 'application/json'},
        }
    except Exception as e:
        return {
            'statusCode': 406,
            'body': str(e),
            'headers': {'Content-Type': 'application/json'},
        }
