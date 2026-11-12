# Importa a função get_db_connection do arquivo database.db
# Essa função serve para conectar com o banco de dados
from database.db import get_db_connection

# Cria uma classe chamada DownloadModel (ela vai cuidar das interações com o banco de dados)
class DownloadModel:

    @staticmethod  # Diz que a função pode ser chamada sem precisar criar um objeto da classe
    def find_by_filename(filename):  # Define uma função que busca um arquivo pelo nome no banco de dados
        """Busca um arquivo pelo nome no banco de dados."""
        conn = get_db_connection()  # Abre uma conexão com o banco de dados
        # Executa um comando SQL para pegar todas as informações da tabela uploads onde o nome do arquivo é o que foi passado
        file = conn.execute('SELECT * FROM uploads WHERE filename = ?', (filename,)).fetchone()
        conn.close()  # Fecha a conexão com o banco de dados
        return file  # Retorna o arquivo encontrado (ou None se não achar nada)

