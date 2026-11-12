# Importa jsonify (transforma um dicionário em JSON) e send_from_directory (envia um arquivo de uma pasta)
from flask import jsonify, send_from_directory

# O Flask NÃO levanta FileNotFoundError quando o arquivo não existe: ele levanta NotFound.
# Por isso o except abaixo precisa capturar NotFound.
from werkzeug.exceptions import NotFound

# Pasta onde os arquivos ficam guardados (caminho absoluto, definido em config.py)
from config import UPLOAD_FOLDER

# Model que consulta o banco de dados
from models.download_model import DownloadModel


# Cria uma classe chamada DownloadController (é tipo uma "caixinha" que guarda funções)
class DownloadController:

    # Diz que a função abaixo é estática, ou seja, pode ser usada sem precisar criar um objeto da classe
    @staticmethod
    def download_file(filename):  # Define uma função chamada download_file que recebe um nome de arquivo (filename)
        # Primeiro confere no banco se esse arquivo foi enviado por upload
        registro = DownloadModel.find_by_filename(filename)
        if registro is None:
            # Retorna "Arquivo não encontrado" em JSON com o código de erro 404
            return jsonify({"erro": "Arquivo não encontrado"}), 404

        try:  # Tenta fazer algo dentro desse bloco
            # Envia o arquivo da pasta UPLOAD_FOLDER com o nome que está registrado no banco
            # O as_attachment=True faz com que o arquivo seja baixado em vez de ser só exibido
            return send_from_directory(UPLOAD_FOLDER, registro['filename'], as_attachment=True)
        except NotFound:  # Se o arquivo está no banco mas sumiu da pasta...
            return jsonify({"erro": "Arquivo não encontrado"}), 404
