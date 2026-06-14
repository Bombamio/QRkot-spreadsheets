# import os
# import pickle

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient import discovery

from app.core.config import settings


# OAuth 2.0
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    "installed": {
        "client_id": settings.client_id_oauth,
        "project_id": settings.project_id_oauth,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":
            "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": settings.client_secret_oauth,
        "redirect_uris": [
            "http://localhost"
        ]
    }
}

# creds = None
#
# if os.path.exists('token.pickle'):
#     with open('token.pickle', 'rb') as token:
#         creds = pickle.load(token)
#
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_config(
#             INFO,
#             SCOPES
#         )
#         creds = flow.run_local_server(port=0)
#
#     with open('token.pickle', 'wb') as token:
#         pickle.dump(creds, token)
#
# SHEETS_SERVICE = discovery.build(
#     'sheets',
#     'v4',
#     credentials=creds
# )


# Service Account
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
