from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)

# === TU CONFIGURACIÓN DE CLIENTE OAUTH ===
GOOGLE_CLIENT_CONFIG = {
    "web": {
        "client_id": "120289t.com",
        "project_id": "vw-analytics-access",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "GOCSPX-t
            "https://flask-oauth-render.onrender.com/google/callback"
        ]
    }
}

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/analytics.readonly"
]

REDIRECT_URI = "https://flask-oauth-render.onrender.com/google/callback"

# === INICIO DE LOGIN GOOGLE ===
@app.route("/google/login")
def login_google():
    flow = Flow.from_client_config(
        GOOGLE_CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

# === CALLBACK GOOGLE ===
@app.route("/google/callback")
def callback_google():
    flow = Flow.from_client_config(
        GOOGLE_CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    # Acá podés usar creds para acceder a APIs
    return "✅ Autenticación Google completada"

if __name__ == "__main__":
    app.run(debug=True)
