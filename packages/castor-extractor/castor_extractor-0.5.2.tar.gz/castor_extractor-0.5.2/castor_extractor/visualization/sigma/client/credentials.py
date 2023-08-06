from dataclasses import dataclass
from enum import Enum


class CredentialsKey(Enum):
    """Value enum object for the credentials"""

    CLIENT_SECRET = "client_secret"
    CLIENT_ID = "client_id"
    HOST = "host"
    GRANT_TYPE = "grant_type"
    API_TOKEN = "api_token"


CLIENT_ALLOWED_KEYS = (
    CredentialsKey.HOST.value,
    CredentialsKey.CLIENT_ID.value,
    CredentialsKey.API_TOKEN.value,
)


@dataclass
class SigmaCredentials:
    """Class to handle Sigma rest API permissions"""

    api_token: str
    client_id: str
    host: str

    @classmethod
    def from_secret(cls, secret: dict) -> "SigmaCredentials":
        credentials = {
            k: v for k, v in secret.items() if k in CLIENT_ALLOWED_KEYS
        }
        return cls(**credentials)
