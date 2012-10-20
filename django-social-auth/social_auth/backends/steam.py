"""
Yahoo OpenID support

No extra configurations are needed to make this work.
"""
from social_auth.backends import OpenIDBackend, OpenIdAuth


STEAM_OPENID_URL = 'http://steamcommunity.com/openid'


class SteamBackend(OpenIDBackend):
    """Yahoo OpenID authentication backend"""
    name = 'steam'


class SteamAuth(OpenIdAuth):
    """Yahoo OpenID authentication"""
    AUTH_BACKEND = SteamBackend

    def openid_url(self):
        """Return Yahoo OpenID service url"""
        return STEAM_OPENID_URL


# Backend definition
BACKENDS = {
    'steam': SteamAuth,
}
