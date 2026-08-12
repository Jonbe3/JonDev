import glfw
from OpenGL.GL import *
from PIL import Image
from pathlib import Path

def carregar_textura(caminho):
    imagem = Image.open(caminho)

    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    imagem =  imagem.convert("RGBA")

    largura, altura = imagem.size
    dados = imagem.tobytes()

    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        largura,
        altura,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        dados
    )

    glBindTexture(GL_TEXTURE_2D, 0)

    return textura

def main():

    # Iniciando GLFW
    if not glfw.init():
        print("Não foi possivel inicializar o GLFW.")
        return
    
    # Criando Janela
    janela = glfw.create_window(800, 600, "SantosFC - CGF", None, None)

    if not janela:
        glfw.terminate()
        print("Não foi possivel criar a janela.")
        return

    # Define janela como contexto atual do OpenGL
    glfw.make_context_current(janela)
    caminho_escudo = Path(__file__).parent / "escudo.jpg"
    textura_escudo = carregar_textura(caminho_escudo)

    # Loop principal
    while not glfw.window_should_close(janela):

        # Cor de fundo  
        glClearColor(0.05, 0.05, 0.05, 1.0)

        # Limpar tela
        glClear(GL_COLOR_BUFFER_BIT)

        # Atualiza janela
        glfw.swap_buffers(janela)

        # Processa eventos
        glfw.poll_events()

    # Encerra GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()
