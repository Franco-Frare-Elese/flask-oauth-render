from flask import Flask, request, redirect
import requests
import json
import logging

# === CONFIGURACIÓN ===
APP_ID = '1178461234033155'
APP_SECRET = 'e1e9648c5cadbbeaac58845f888556b6'
REDIRECT_URI = 'https://flask-oauth-render.onrender.com/meta/callback'
SCOPES = 'pages_show_list,pages_read_engagement,ads_read,instagram_basic,instagram_manage_insights,business_management'

# === INICIALIZACIÓN DEL SERVIDOR ===
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# === 1. Ruta inicial: genera link de autorización ===
@app.route('/')
def auth_link():
    if APP_ID.startswith('TU_') or APP_SECRET.startswith('TU_'):
        return "❌ ERROR: APP_ID o APP_SECRET no están configurados.", 400

    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
        f"&response_type=code"
    )
    return redirect(auth_url)

# === 2. Ruta de callback que recibe el código ===
@app.route('/meta/callback')
def callback():
    code = request.args.get('code')

    if not code:
        return "❌ No se recibió el parámetro `code` en el callback.", 400

    if APP_ID.startswith('TU_') or APP_SECRET.startswith('TU_'):
        return "❌ ERROR: APP_ID o APP_SECRET no están configurados.", 400

    token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
    params = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    try:
        response = requests.get(token_url, params=params)
        response.raise_for_status()
        token_data = response.json()

        with open('meta_token_nuevo_app_habilitada_1.json', 'w') as f:
            json.dump(token_data, f, indent=4)

        logging.info("✅ Token obtenido y guardado.")
        return f"✅ Token guardado correctamente:<br><pre>{json.dumps(token_data, indent=2)}</pre>"

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error en token exchange: {e}")
        return f"❌ Error en el intercambio de token:<br>{str(e)}", 500

# === 3. Eliminar pantalla de advertencia de ngrok ===
@app.after_request
def skip_ngrok_warning(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# === 4. Arranque del servidor ===
if __name__ == '__main__':
    app.run(port=5000)
