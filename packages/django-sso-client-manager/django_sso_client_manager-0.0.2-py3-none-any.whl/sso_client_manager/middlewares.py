import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .utils import decrypt_data

signer = Signer()

User = get_user_model()

class ParseCodeDataMiddleware(MiddlewareMixin):
    
    def __call__(self, request):
        code = request.COOKIES.get('code')
        my_code_mod = None

        if (not request.user.is_authenticated and 
            code and 'set-code/' not in request.path):    

            my_code = request.COOKIES.get('my_code')
            try:
                my_code = signer.unsign_object(my_code)
                username = my_code['username']
                my_code = code == my_code['code'] 
            except:
                my_code = None

            if not my_code:
                sso_server = settings.SSO_SERVER_SESSIONID
                response = requests.get(
                    url=sso_server,
                    params={
                        'code':code,
                        'application_id':settings.APPLICATION_ID
                    }
                )

                response_json = response.json()
                if not response.ok:
                    response = JsonResponse(response_json, status=response.status_code)
                    response.delete_cookie('code')
                    response.delete_cookie('my_code')
                    return response
                
                response_json = response_json['code']
                username = decrypt_data(key=settings.KEY, ciphertext=response_json)['username']
                
                my_code_mod = signer.sign_object({
                    'username' : username,
                    'code' : code,   
                }) 

            try:
                request.user = User.objects.filter(username=username).first()
            except:
                response = JsonResponse({
                    'message' : "user is not found."
                    }, status=400)
                response.delete_cookie('code')
                response.delete_cookie('my_code')
                return response

        response = self.get_response(request)
        if my_code_mod:
            response.set_cookie('my_code', my_code_mod, expires=30)
        return response
