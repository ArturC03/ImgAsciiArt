from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import numpy as np
import base64
import os
# Bing Chilling
def urlParaImagem(url):
    resposta = requests.get(url)
    return BytesIO(resposta.content)

def imagemParaAsciiArt(caminhoImagem):
    def pixelParaCaracter(valorDoPixel, caracteres='$@b%8&wm#*oahkbdpqwmzo0qlcjuyxzcvunxrjft/\|\'()1{}[]?-_+~<>i!lI;:,"^`\'.                    '):
        return caracteres[-1 * int((valorDoPixel / 255.0) * (len(caracteres) - 1))]

    imagem = Image.open(caminhoImagem).convert('L')
    largura, altura = imagem.size
    larguraNova = 150 
    razaoAltura = altura / largura
    alturaNova = int(larguraNova * razaoAltura)
    imagem = imagem.resize((larguraNova, alturaNova))

    # Determina o número de cores únicas na imagem
    cores = imagem.getcolors(larguraNova * alturaNova)  # Obtém as cores e suas frequências
    numeroDeCores = len(cores) if cores is not None else 0

    # Ajusta o conjunto de caracteres com base no número de cores

    arteAscii = ""
    for y in range(alturaNova):
        for x in range(larguraNova):
            valorDoPixel = imagem.getpixel((x, y))
            arteAscii += pixelParaCaracter(valorDoPixel)
        arteAscii += os.linesep
    
    return arteAscii
   
def asciiParaImagem(arteAscii, fonteTamanho=30):
    linhas = arteAscii.split(os.linesep)
    larguraLinha = max(len(linha) for linha in linhas)
    alturaImagem = len(linhas)
    
    # Carrega uma fonte monoespaçada padrão ou customizada
    try:
        fonte = ImageFont.truetype("DejaVuSansMono.ttf", fonteTamanho)
    except IOError:
        print("Fonte monoespaçada padrão não encontrada. Usando fonte padrão do sistema.")
        fonte = ImageFont.load_default()
    
    # Estima a largura e altura de um caractere
    bbox = fonte.getbbox("X")
    larguraFonte= bbox[2] - bbox[0]
    alturaFonte= bbox[3] - bbox[1]   # Ajusta as dimensões da imagem para acomodar a proporção correta de caracteres
    larguraImagem = larguraLinha * larguraFonte
    alturaImagem = alturaImagem * alturaFonte  # Ajusta com base na altura estimada da fonte
    
    imagem = Image.new('RGB', (larguraImagem, alturaImagem), 'black')
    desenho = ImageDraw.Draw(imagem)
    
    y = 0
    for linha in linhas:
        desenho.text((0, y), linha, fill="white", font=fonte)
        y += alturaFonte  # Usa a altura da fonte para avançar as linhas corretamente
    
    img_byte_arr = BytesIO()
    imagem.save(img_byte_arr, format="WEBP")  # Save your image to the byte array as WEBP
    img_byte_arr.seek(0)  # Ensure the buffer's start

    # Encode the byte array to base64
    base64_encoded_result = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
    
    # Format the base64 string for HTML embedding
    base64_img_html = f"data:image/webp;base64,{base64_encoded_result}"
    
    return base64_img_html
def ImageToAsciiArtImage(UrlImagem):
    urlImagem = UrlImagem.strip().strip('\'')
    caminhoImagem = urlParaImagem(urlImagem)
    arteAscii = imagemParaAsciiArt(caminhoImagem)
    arquivoSaida = BytesIO()
    
    asciiParaImagem(arteAscii, arquivoSaida)
    
def ImageToAsciiArtBytes(UrlImagem):
    urlImagem = UrlImagem.strip().strip('\'')
    caminhoImagem = urlParaImagem(urlImagem)
    arteAscii = imagemParaAsciiArt(caminhoImagem)

    imagemEmBytes = asciiParaImagem(arteAscii)  # Agora retorna um BytesIO
    return imagemEmBytes
