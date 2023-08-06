import requests
from typing import List
import json
from requests.compat import urljoin
from neuralpit import NeuralPitSDK

TIKA_SERVER_URL = 'https://tika.3rd.neuralpit.com'

class FileConversionService():

    def __init__(self) -> None:
        super().__init__()


    def convertFileToText(self, file):
        put_url = urljoin(TIKA_SERVER_URL,'/tika')
        headers = {'x-api-key':self.api_key, 'Accept':'application/json'}
        put_call = requests.put(put_url, headers = headers, data = file)
        resp =  json.loads(put_call.content)
        return resp
