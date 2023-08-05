import os
import uuid
import requests
import mimetypes

def get_extension(content_type):
    data = mimetypes.guess_all_extensions(content_type)
    if type(data) == list:
        return data[-1]
    return data

def get_image(url):
    res = requests.get(url, stream=True)
    image_type = res.headers.get('Content-Type')
    
    filename = uuid.uuid4().hex
    extension = get_extension(image_type)
    
    name_file = f"{filename}{extension}"
    return name_file, res.raw.read() if res.status_code == 200 else None

def save_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def dividir_texto(texto, limite=1994):
    partes = []
    texto_atual = ""
    palavras = texto.split()

    for palavra in palavras:
        if len(texto_atual) + len(palavra) + 1 <= limite:  # +1 para incluir um espaço após a palavra
            texto_atual += palavra + " "
        else:
            partes.append(texto_atual.strip())
            texto_atual = palavra + " "

    partes.append(texto_atual.strip())  # Adiciona a última parte, caso haja texto remanescente

    return partes

def contabilizar_caracteres_por_linha(texto):
    linhas = texto.split('\n')
    caracteres_por_linha = []

    for linha in linhas:
        caracteres = len(linha) + 1
        caracteres_por_linha.append((caracteres, f"{linha}\n"))

    # Agrupar em listas com, no máximo, 2000 linhas
    lista_de_listas = []
    lista_atual = []
    caracteres_acumulados = 0

    for caracteres, linha in caracteres_por_linha:
        if caracteres_acumulados + caracteres < 1985:
            lista_atual.append((caracteres, linha))
            caracteres_acumulados += caracteres
        else:
            lista_de_listas.append(lista_atual)
            lista_atual = [(caracteres, linha)]
            caracteres_acumulados = caracteres

    # Adicionar a última lista de itens, se houver
    if lista_atual:
        lista_de_listas.append(lista_atual)

    return lista_de_listas