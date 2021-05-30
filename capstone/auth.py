import ssl
import json
import traceback
import ssl
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get['ALGORITHMS']
API_AUDIENCE = os.environ.get('API_AUDIENCE')
JWKS_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
The get_token_auth_header() method attempts to get the header from the request and parse it.  It
takes in a payload from the request, validates that it is properly formatted, splits the
authorization header into the two parts of a bearer token, and returns the token.
Calling:
    get_token_auth_header()
Requires:
    Auth header with a breaer token (payload)
Returns:
    Auth token
Known errors
    AuthError if no header is present.
    AuthError if the header is malformed.
    AuthError is the token is not a proper bearer token.

'''


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    # print(auth_header)

    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # split the auth header parts
    header_parts = auth_header.split(" ")

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = header_parts[1]
    return token

    # print(token)


'''
The get_token_auth_header() method attempts to get the header from the request and parse it.  It
takes in a payload from the request, validates that it is properly formatted, splits the
authorization header into the two parts of a bearer token, and returns the token.

Calling:
    check_permissions(permission, payload)
Parameters:
    Permission:  desired permission as a string (i.e. 'post:drink').
    Payload:  decoded jwt token.
Requires:
    Auth header with a breaer token (payload)
    Permissions that are needed to complete the requested action.
Returns:
    Boolean:  True (success) or Errors
Known errors
    Abort (400) if permissions are not included in the token.
    AuthError (401) if desired permission is not in the token.
'''


def check_permissions(permission, payload):
    # print(permission,payload)
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Requested Permission not found.'
        }, 401)

    return True


'''
The verify_decode_jwt() method takes in the authorization token and decodes it for use in the
authorization functions.  It takes an encoded jwt token and attempts to parse it.  It returns the
parsed and decoded token.

Calling:
    verify_decode_jwt(token).
Parameters:
    token: a json web token (string).
Requires:
    JWT token.
Returns:
    Decoded JWT payload.
Known Errors:
    401 status code invalid_header:  malformed authroization header.
    401 status code token_expired:  expired token.
    401 status code invalid_claims:  incorrect audience or issuer.
    400 status code invalid_header:  unable to parse token.
    400 status code invalid_header:  unable to find RSA key.
'''
# ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def verify_decode_jwt(token):
    # print('token passed to function',token)
    try:
        # GET THE PUBLIC KEY FROM AUTH0
        jsonurl = urlopen(
            f'https://{AUTH0_DOMAIN}/.well-known/jwks.json',
            context=ssl_context
        )
        # print('verify 2')
        jwks = json.loads(jsonurl.read())
        # print('verify 3')

        # GET THE DATA IN THE HEADER
        unverified_header = jwt.get_unverified_header(token)
        # print('verify 4', unverified_header)

        # CHOOSE OUR KEY
        rsa_key = {}
        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        # Finally, verify!!!
        if rsa_key:
            try:
                # USE THE KEY TO VALIDATE THE JWT
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )

                return payload

            # Expired token
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)
            # Token error in audience or issuer
            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            # Catch any other exceptions that arise
            except Exception as e:
                traceback.print_exc()
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
        # If no RSA key raise an auth error
        raise AuthError({
            'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
        }, 400)
    # Traceback is helping in debugging during dev
    except Exception as e:
        traceback.print_exc()


'''
The @requires_auth(permission) decorator method is used to check permissions before preforming
certain acitons of the api.  It calls the get_token_auth_header, verify_decode_jwt, and check_permissions
methods to authorize particular actions.

Calling:
    @requires_auth(permission)
Parameters:
    permission: string permission (i.e. 'post:drink')
Returns:
    Reuslts of get_token_auth_header, verify_decode_jwt, and check_permissions methods.
Known errors:
    None
'''
# def requires_auth(permission=''):
#     def requires_auth_decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             token = get_token_auth_header()
#             payload = verify_decode_jwt(token)
#             check_permissions(payload,permission)
#             return f(payload, *args, **kwargs)

#         return wrapper
#     return requires_auth_decorator


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as authError:
                raise abort(authError.status_code,
                            authError.error["description"])

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
