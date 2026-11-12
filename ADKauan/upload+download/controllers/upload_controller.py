import os  # Permite mexer com arquivos e pastas do sistema (criar a pasta uploads)
import logging  # Permite registrar mensagens de log (sucesso, aviso, erro) num arquivo
from flask import jsonify, request  # jsonify: devolve respostas em JSON | request: acessa os dados que o cliente enviou (arquivo, IP, tamanho)
from werkzeug.utils import secure_filename  # Limpa o nome do arquivo, removendo caracteres perigosos (ex: ../../)

from config import (
    BASE_DIR,
    UPLOAD_FOLDER,
    LOG_FILE,
    EXTENSOES_PERMITIDAS,
    TAMANHO_MAXIMO_ARQUIVO,
    TAMANHO_MAXIMO_KB,
)
from models.upload_model import UploadModel

# Configuração de logs (utf-8 para aceitar nomes de arquivo com acento no Windows)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8",
)


class UploadController:

    @staticmethod
    def arquivo_permitido(nome_arquivo):
        """Verifica se a extensão do arquivo é permitida."""
        return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

    @staticmethod
    def tamanho_do_arquivo(arquivo):
        """Mede o tamanho real do arquivo enviado (em bytes), sem consumir o conteúdo."""
        arquivo.stream.seek(0, os.SEEK_END)
        tamanho = arquivo.stream.tell()
        arquivo.stream.seek(0)
        return tamanho

    @staticmethod
    def upload_file():
        """Recebe e processa o upload do arquivo."""

        # Verifica se um arquivo foi enviado
        if 'file' not in request.files:
            logging.warning("Falha no upload: Nenhum arquivo enviado")
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400

        arquivo = request.files['file']

        # Verifica se o nome do arquivo está vazio
        if arquivo.filename == '':
            logging.warning("Falha no upload: Nome do arquivo vazio")
            return jsonify({"erro": "Nome do arquivo vazio"}), 400

        # Verifica o tamanho do arquivo (tamanho real do arquivo, não da requisição inteira)
        if UploadController.tamanho_do_arquivo(arquivo) > TAMANHO_MAXIMO_ARQUIVO:
            logging.warning(f"Falha no upload: {arquivo.filename} - Tamanho excede {TAMANHO_MAXIMO_KB} KB")
            return jsonify({
                "erro": f"Arquivo excede o tamanho máximo permitido ({TAMANHO_MAXIMO_KB} KB)"
            }), 413

        # Verifica se o tipo do arquivo é permitido
        if not UploadController.arquivo_permitido(arquivo.filename):
            logging.warning(f"Falha no upload: {arquivo.filename} - Tipo de arquivo não permitido")
            return jsonify({
                "erro": "Tipo de arquivo não permitido!",
                "tipos_permitidos": sorted(EXTENSOES_PERMITIDAS)
            }), 400

        # Limpa o nome ANTES de salvar. Se a limpeza apagar o nome ou a extensão
        # (ex: "中文.pdf" vira "pdf"), o arquivo é recusado em vez de salvo sem extensão.
        nome_arquivo = secure_filename(arquivo.filename)
        if not UploadController.arquivo_permitido(nome_arquivo):
            logging.warning(f"Falha no upload: {arquivo.filename} - Nome de arquivo inválido")
            return jsonify({
                "erro": "Nome de arquivo inválido! Use letras (sem acento), números, '-' ou '_' e uma extensão permitida."
            }), 400

        # Não sobrescreve um arquivo que já existe
        if UploadModel.find_by_filename(nome_arquivo):
            logging.warning(f"Falha no upload: {nome_arquivo} - Já existe um arquivo com esse nome")
            return jsonify({"erro": f"Já existe um arquivo chamado '{nome_arquivo}'"}), 409

        # Salva o arquivo no disco
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        arquivo.save(caminho_arquivo)

        # Registra o arquivo no banco (o download consulta essa tabela)
        caminho_relativo = os.path.relpath(caminho_arquivo, BASE_DIR)
        if not UploadModel.save_file(nome_arquivo, caminho_relativo):
            # Outro upload com o mesmo nome entrou no banco entre a checagem e agora
            logging.warning(f"Falha no upload: {nome_arquivo} - Nome duplicado no banco")
            return jsonify({"erro": f"Já existe um arquivo chamado '{nome_arquivo}'"}), 409

        # Registra o sucesso do upload no log
        ip_usuario = request.remote_addr
        logging.info(f"Upload bem-sucedido: {nome_arquivo} | IP: {ip_usuario}")

        return jsonify({
            "mensagem": "Arquivo salvo com sucesso!",
            "arquivo": nome_arquivo
        }), 200
