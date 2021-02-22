import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
import sys


AUTH0_DOMAIN = 'ma-toka.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'api-manager'

'''
AuthError Exception 
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
Authantication header
'''

def get_token_auth_header():
    auth =  request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)

    parts = auth.split()
    
    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer"
        }, 401)
        
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"
        }, 401)

    token = parts[1]
    return token



'''
User permission
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 401)
    
    return True
'''
verify token with jwt
'''

def verify_decode_jwt(token):
    jsonurl =urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwtks = json.loads(jsonurl.read())
    unveirfied_header =  jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unveirfied_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformated'
        }, 401)



    for key in jwtks['keys']:
        if key['kid'] == unveirfied_header['kid']:
            rsa_key ={
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
            
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to parse authentication token'
    }, 400)
    
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator