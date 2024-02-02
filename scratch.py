import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bing_image_downloader import downloader

# Função para obter o nome real da imagem a partir do link usando web scraping
def get_real_image_name(image_url):
    response = requests.get(image_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Exemplo: extrair o nome real do final da URL
    real_name = image_url.split("/")[-1]
    return real_name

# Carregar o arquivo CSV
df = pd.read_csv('C:/teste/csv/ibili-new.csv')

# Diretório de destino para as imagens
diretorio_destino = 'C:/teste/img-ibili-new/'

# Criar o diretório se não existir
if not os.path.exists(diretorio_destino):
    os.makedirs(diretorio_destino)

# Loop sobre as linhas do DataFrame
for index, row in df.iterrows():
    referencia = row['Referencia']
    nome_produto = row['Produtos']

    try:
        # Inclua a referência e o nome do produto na consulta de pesquisa
        query = f"{referencia} {nome_produto}"

        # Faça o download das imagens usando a API do Bing
        downloader.download(query, limit=3, output_dir=diretorio_destino, adult_filter_off=True, force_replace=False)

        # Obtenha os nomes reais das imagens usando web scraping
        for file_name in os.listdir(diretorio_destino):
            file_path = os.path.join(diretorio_destino, file_name)
            real_name = get_real_image_name(file_path)
            print(f"Nome real da imagem: {real_name}")
    except Exception as e:
        print(f"Falha ao baixar imagens para a referência {referencia} - {nome_produto}: {e}")

print("Download de imagens concluído!")
