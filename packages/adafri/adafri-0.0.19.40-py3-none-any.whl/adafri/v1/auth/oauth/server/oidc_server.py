from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from ...oauth import (OAuthClient, OAuthToken, OpenIDAuthorizationCodeGrant as AuthCodeGrant,TokenValidator)
from ...oauth import OpenIDImplicitGrant, OpenIDHybridGrant, OpenIDCode

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