from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge

from ...oauth import (OAuthClient, OAuthToken, AuthorizationCodeGrant as AuthCodeGrant, 
                                TokenRevocationEndpoint, TokenValidator, RefreshTokenGrant)
from ...oauth import OpenIDImplicitGrant, OpenIDHybridGrant, OpenIDCode
class AuthServer(AuthorizationServer):
    OAUTH2_TOKEN_EXPIRES_IN = {
    'authorization_code': 864000,
    'implicit': 3600,
    'password': 864000,
    'client_credentials': 864000
    }
    def authenticate_client(self, request, methods, endpoint='token'):
        return super().authenticate_client(request, methods, endpoint)
    
    def handle_error_response(self, request, error):
        return self.handle_response(*error(self.get_error_uri(request, error)))
    

# oidc_authorization_server = AuthServer(
#     query_client=OAuthClient().get_by_client_id,
#     save_token=OAuthToken().save,
# )
oidc_authorization_server = AuthorizationServer()
require_oidc_oauth = ResourceProtector()

def config_oidc_oauth(app):
    oidc_authorization_server.query_client = OAuthClient().get_by_client_id
    oidc_authorization_server.save_token = OAuthToken().save
    oidc_authorization_server.init_app(app)
    oidc_authorization_server.register_grant(AuthCodeGrant, [
        OpenIDCode(require_nonce=True),
    ])
    oidc_authorization_server.register_grant(OpenIDImplicitGrant)
    oidc_authorization_server.register_grant(OpenIDHybridGrant)
    require_oidc_oauth.register_token_validator(TokenValidator())