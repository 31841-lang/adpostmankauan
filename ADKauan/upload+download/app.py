from flask import Flask, jsonify
from config import UPLOAD_FOLDER, TAMANHO_MAXIMO_ARQUIVO, TAMANHO_MAXIMO_KB
from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Limite "de porta": o Flask recusa (erro 413) qualquer requisição maior que isso
# antes de processar o arquivo. A folga de 16 KB cobre o "envelope" do multipart
# (cabeçalhos, nome do campo etc.). O limite exato do arquivo é conferido no
# UploadController.
app.config['MAX_CONTENT_LENGTH'] = TAMANHO_MAXIMO_ARQUIVO + 16 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

app.register_blueprint(upload_bp, url_prefix='/uploads')
app.register_blueprint(download_bp, url_prefix='/downloads')


@app.errorhandler(413)
def arquivo_grande_demais(erro):
    return jsonify({
        "erro": f"Arquivo excede o tamanho máximo permitido ({TAMANHO_MAXIMO_KB} KB)"
    }), 413


if __name__ == '__main__':
    app.run(debug=True)
