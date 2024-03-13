from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import numpy as np

# Bing Chilling
def urlParaImagem(url):
    resposta = requests.get(url)
    return BytesIO(resposta.content)

def imagemParaAsciiArt(caminhoImagem):
    def pixelParaCaracter(valorDoPixel, caracteres='$@b%8&wm#*oahkbdpqwmzo0qlcjuyxzcvunxrjft/\|\'()1{}[]?-_+~<>i!lI;:,"^`\'.                    '):
        return caracteres[-1 * int((valorDoPixel / 255.0) * (len(caracteres) - 1))]

    imagem = Image.open(caminhoImagem).convert('L')
    largura, altura = imagem.size
    larguraNova = largura
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
        arteAscii += '\n'
    
    return arteAscii
   
def asciiParaImagem(arteAscii, arquivoSaida, fonteTamanho=30):
    linhas = arteAscii.split('\n')
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
    
    imagem.save(arquivoSaida, "WEBP")

def ImageToAsciiArtImage(UrlImagem):
    urlImagem = UrlImagem.strip().strip('\'')
    caminhoImagem = urlParaImagem(urlImagem)
    arteAscii = imagemParaAsciiArt(caminhoImagem)
    arquivoSaida = "./saida_ascii.webp"
    
    asciiParaImagem(arteAscii, arquivoSaida)
    
def ImageToAsciiArtBytes(UrlImagem):
    urlImagem = UrlImagem.strip().strip('\'')
    caminhoImagem = urlParaImagem(urlImagem)
    arteAscii = imagemParaAsciiArt(caminhoImagem)

    imagemEmBytes = asciiParaImagem(arteAscii)  # Agora retorna um BytesIO
    return imagemEmBytes
