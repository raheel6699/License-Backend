# customsecuritymiddleware/middleware.py
import os
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from dotenv import load_dotenv
from pathlib import Path
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import HttpResponse
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


class CustomSecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        formatted_timestamp = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
        current_parse_time = datetime.strptime(formatted_timestamp,'%Y-%m-%d %H:%M:%S')
        ciphertext = os.environ.get("license_key").encode('utf-8')
        decode_value = os.environ.get("ENCRYPTION_KEY").encode('utf-8')
        iv, encrypted_text = map(b64decode, ciphertext.split(b':'))
        cipher = AES.new(decode_value, AES.MODE_CBC, iv)
        decrypted_text = unpad(cipher.decrypt(encrypted_text), AES.block_size)
        end_timestamp = datetime.strptime(decrypted_text.decode('utf-8'), '%Y-%m-%d %H:%M:%S')
        time_difference = current_parse_time-end_timestamp
        days_difference = time_difference.days
        if days_difference >= 0:
            return HttpResponse("Access restricted",status=HTTP_400_BAD_REQUEST)
        return

    def process_response(self, request, response):
        return response
