import glfw
from OpenGL.GL import *

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
        
