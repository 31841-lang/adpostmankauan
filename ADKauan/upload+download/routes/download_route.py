# Importa a classe Blueprint do Flask, que serve para organizar rotas
from flask import Blueprint

# Importa a classe DownloadController do arquivo download_controller (ela tem a lógica para baixar arquivos)
from controllers.download_controller import DownloadController

# Cria um Blueprint chamado 'download_bp', que é tipo um mini aplicativo dentro do Flask
download_bp = Blueprint('download_bp', __name__)

# Define uma rota que responde quando alguém acessa '/downloads/download/<filename>' (o prefixo '/downloads' vem do app.py) usando o método GET
@download_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):  # Função que recebe o nome do arquivo como parâmetro
    # Chama a função de download que está no DownloadController e retorna o arquivo
    return DownloadController.download_file(filename)
