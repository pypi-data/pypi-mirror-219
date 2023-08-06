from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge

from ...oauth import (OAuthClient, OAuthToken, AuthorizationCodeGrant as AuthCodeGrant, 
                                TokenRevocationEndpoint, TokenValidator, RefreshTokenGrant)

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
    

authorization = AuthServer(
    query_client=OAuthClient().get_by_client_id,
    save_token=OAuthToken().save,
)

require_oauth = ResourceProtector()

def config_oauth(app):
    authorization.init_app(app)
    
    authorization.register_grant(grants.ImplicitGrant)
    #authorization.register_grant(AccessTokenGrant, [CodeChallenge(required=True)])
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(AuthCodeGrant, [CodeChallenge(required=True)])
    
    # authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)
    # support revocation
    # revocation_cls = create_revocation_endpoint()
    authorization.register_endpoint(TokenRevocationEndpoint)
    # authorization.register_token_generator("default", TokenGenerator.generate)
    # authorization.register_token_generator("client_credentials", TokenGenerator.generate)
    # protect resource
    #bearer_cls = create_bearer_token_validator(TokenValidator)
    require_oauth.register_token_validator(TokenValidator())