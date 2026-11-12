# adpostmankauan

# API de Upload e Download de Arquivos

Uma API feita com Flask para enviar arquivos para o servidor e baixá-los depois. Funciona assim: você manda um arquivo, ela confere se ele é permitido, guarda na pasta `uploads/` e anota tudo num log.

## O que ela faz

- Recebe arquivos (upload) e entrega eles de volta (download)
- Só aceita `png`, `jpg`, `jpeg`, `gif`, `pdf` e `txt`
- Limita o tamanho do arquivo (30 KB)
- Limpa o nome do arquivo antes de salvar, para ninguém mandar algo perigoso como `../../coisa.txt`
- Registra cada tentativa de upload no `uploads.log`, com data, nome do arquivo e IP

## Como rodar

```bash
pip install flask
python app.py
```

Pronto, ela sobe em `http://127.0.0.1:5000`. A pasta `uploads/` e o banco `database.db` são criados sozinhos na primeira vez.

## Rotas

| Método | Rota                             | Para que serve        |
|--------|----------------------------------|-----------------------|
| POST   | `/uploads/upload`                | Enviar um arquivo     |
| GET    | `/downloads/download/<filename>` | Baixar um arquivo     |

## Como usar

### Enviar um arquivo

Mande o arquivo em `multipart/form-data`, no campo `file`:

```bash
curl -X POST -F "file=@documento.pdf" http://127.0.0.1:5000/uploads/upload
```

**Deu certo (200):**

```json
{
  "mensagem": "Arquivo salvo com sucesso!",
  "arquivo": "documento.pdf"
}
```

**Deu errado (400):** a resposta traz uma chave `erro` explicando o motivo:

- Não mandou o campo `file`: `Nenhum arquivo enviado`
- Mandou o arquivo sem nome: `Nome do arquivo vazio`
- Arquivo grande demais: `Arquivo excede o tamanho máximo permitido (15 KB)`
- Extensão não permitida: `Tipo de arquivo não permitido!`, junto com a lista `tipos_permitidos`

### Baixar um arquivo

Passe o nome do arquivo no final da rota:

```bash
curl -O -J http://127.0.0.1:5000/downloads/download/documento.pdf
```

Se o arquivo existir, ele é baixado. Se não existir, a resposta é 404.

## Testando no Postman

- **Upload:** método `POST`, aba Body, opção `form-data`, chave `file` com o tipo trocado para `File`
- **Download:** método `GET`, só com a URL da rota

Atenção ao endereço: é `/uploads/upload` e `/downloads/download/<nome>`, e não só `/upload`.

## Como o projeto está organizado

```
.
├── app.py          # inicia a aplicação e registra as rotas
├── routes/         # define os endereços (upload e download)
├── controllers/    # regras de cada rota (validações, salvar, enviar)
├── models/         # consultas ao banco de dados
├── database/       # conexão e criação da tabela (SQLite)
└── uploads/        # onde os arquivos ficam guardados
```

O caminho de uma requisição é sempre **rota → controller → model**.

## Coisas que vale saber

- A mensagem de erro de tamanho diz 15 KB, mas o limite real no código é 30 KB.
- O upload salva o arquivo na pasta, mas não registra ele no banco. A tabela `uploads` fica vazia.
- Quando o arquivo não existe, o código tenta devolver um JSON de erro, mas o `except` não pega esse caso. Hoje vem a página de erro padrão do Flask.
- Não tem autenticação: qualquer pessoa que acessar a API consegue enviar e baixar arquivos.
- O `debug=True` é só para desenvolvimento, não deve ir para produção.
- No Render (plano gratuito) o disco é apagado quando o serviço reinicia ou faz novo deploy. Os arquivos enviados e o banco somem.
