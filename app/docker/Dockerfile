FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta padrão da aplicação Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "run.py"]