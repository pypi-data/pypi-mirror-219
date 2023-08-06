import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views import View

from .utils import decrypt_data

User = get_user_model()
signer = Signer()

def profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'user_data':None
        }, status=401)
    
    user = request.user
    return JsonResponse({
        'user_data':{
            'id': user.id,
            'username': user.username,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }
    })
    
def login(request):
    next_url = request.GET.get('next') or '/'
    if request.user.is_authenticated:        
        return redirect(next_url)

    signed_obj = signer.sign_object({
        'date_time' : str(timezone.now()),
        'secret_key' : request.build_absolute_uri('/'),   
    })

    url_path = request.build_absolute_uri(reverse('set-code'))
    
    url = f'{settings.SSO_SERVER_LOGIN}?next={url_path}&frontend_url={next_url}&verify_code={signed_obj}&application_id={settings.APPLICATION_ID}'
    return redirect(url)

def logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message':'You have not login to this sytem.'})

    next_url = request.GET.get('next') or request.build_absolute_uri('/')
    url = f'{settings.SSO_SERVER_LOGOUT}?next={next_url}'
    response = redirect(url)
    response.delete_cookie('my_code')
    response.delete_cookie('code')
    return response

class SetCodeView(View):
    def create_or_update_user(self, user_data):
        try:
            user = User.objects.get(username=user_data['username'])
            user.last_login = user_data.get('last_login', timezone.now())
            user.save()
        except:
            user = User.objects.create(
                username=user_data.get('username'),
                is_staff = user_data.get('is_staff', False),
                is_active = user_data.get('is_active', False),
                is_superuser = user_data.get('is_superuser', False),
                date_joined = user_data.get('created_at', timezone.now()),
                last_login = user_data.get('last_login', timezone.now()),
            )

        if hasattr(user, 'sso_id') and user_data.get('id'):
            user.sso_id = user_data.get('id')
            user.save()

        return user

    def get(self, request):

        verify_code = request.GET.get('verify_code')
        if not verify_code:
            return JsonResponse({
                'verify_code':'This field is required.',
            }, status=400)
        
        try:
            obj = signer.unsign_object(verify_code)
        except:
            return JsonResponse({
                'message':'Problems while decrypt data.',
            }, status=401)
        
        try:
            date_time = parse_datetime(obj['date_time'])
        except:
            return JsonResponse({
                'message':'Cannot parse time while decrypt data.',
            }, status=401)
        
        try:
            secret_key = parse_datetime(obj['secret_key'])
        except:
            return JsonResponse({
                'message':'Cannot parse secret_key while decrypt data.',
            }, status=401)
        
        if secret_key == request.build_absolute_uri('/'):
            return JsonResponse({
                'message':'Request is not origined from thios site.',
            }, status=401)
        
        diff_time = (timezone.now() - date_time).total_seconds()
        if diff_time > 60:
            return JsonResponse({
                    'message':'Token is expiry or invalid.',
                }, status=401)
        
        code = request.GET.get('code')
        if not code:
            return JsonResponse({
                'code':'This field is required.',
            }, status=400)
        
        plain_code = decrypt_data(key=settings.KEY, ciphertext=code)

        signed_obj = plain_code['signed_obj']
        user_data = json.loads(plain_code['user_data'])
        user = self.create_or_update_user(user_data)
        
        my_code = signer.sign_object({
            'username' : user.username,
            'code' : code,   
        }) 
        
        frontend_url = request.GET.get('frontend_url') or '/'
        response = HttpResponseRedirect(frontend_url)
        response.set_cookie('my_code', my_code, expires=30)
        response.set_cookie('code', signed_obj)
        return response
