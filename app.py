from flask import Flask
from controllers.wallet_controller import wallet_bp
from services.db_service import db, init_app 
from sqlalchemy import text

app = Flask(__name__)


init_app(app)

# Register blueprints
app.register_blueprint(wallet_bp, url_prefix="/wallet")
@app.route('/')
def index():
    return "Wallet service is up", 200


@app.route('/health')
def health():
    return 'OK', 200

@app.route('/wallets/health')
def health_check():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "OK - Database Connected wallet", 200
    except Exception as e:
        return f"Database Connection Failed (wallet): {str(e)}", 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
