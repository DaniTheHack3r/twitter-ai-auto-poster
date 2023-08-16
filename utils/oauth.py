from fastapi.security import OAuth2PasswordBearer
import oauthlib.oauth1


def sign_oauth1(
    consumer_key: str,
    consumer_secret: str,
    access_token: str,
    access_token_secret: str,
    url: str,
    http_method: str,
):
    client = oauthlib.oauth1.Client(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    _, headers, _ = client.sign(url, http_method)

    return headers

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")