import os

# Pasta onde está o projeto. Todos os caminhos partem daqui, então o projeto
# funciona não importa de qual pasta você execute o "python app.py".
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
LOG_FILE = os.path.join(BASE_DIR, 'uploads.log')

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

TAMANHO_MAXIMO_KB = 30
TAMANHO_MAXIMO_ARQUIVO = TAMANHO_MAXIMO_KB * 1024
