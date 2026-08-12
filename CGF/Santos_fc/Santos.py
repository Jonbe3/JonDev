import glfw
import ctypes
import numpy as np

from OpenGL.GL import *
from PIL import Image
from pathlib import Path

def criar_quadrado():
    vertices = np.array([
        # posição       # textura
        -0.8,  0.8,     0.0, 1.0,  # superior esquerdo
         0.8,  0.8,     1.0, 1.0,  # superior direito
         0.8, -0.8,     1.0, 0.0,  # inferior direito
        -0.8, -0.8,     0.0, 0.0,  # inferior esquerdo
    ], dtype=np.float32)

    return vertices

def criar_vbo(vertices):
    vbo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return vbo



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

def criar_vao(vbo):
    vao = glGenVertexArrays(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # Posição
    glVertexAttribPointer(
        0,
        2,
        GL_FLOAT,
        GL_FALSE,
        4 * 4,
        ctypes.c_void_p(0)
    )

    glEnableVertexAttribArray(0)

    # Coordenadas da textura
    glVertexAttribPointer(
        1,
        2,
        GL_FLOAT,
        GL_FALSE,
        4 * 4,
        ctypes.c_void_p(2 * 4)
    )

    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao

def criar_vertex_shader():
    codigo = """
    #version 330 core

    layout (location = 0) in vec2 posicao;
    layout (location = 1) in vec2 coordenada_textura;

    out vec2 texCoord;

    void main()
    {
        gl_Position = vec4(posicao, 0.0, 1.0);
        texCoord = coordenada_textura;
    }
    """

    shader = glCreateShader(GL_VERTEX_SHADER)

    glShaderSource(shader, codigo)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(shader).decode()
        print("Erro no Vertex Shader:")
        print(erro)

    return shader

def criar_fragment_shader():
    codigo = """
    #version 330 core

    in vec2 texCoord;

    out vec4 cor;

    uniform sampler2D textura;

    void main()
    {
        cor = texture(textura, texCoord);
    }
    """

    shader = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(shader, codigo)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(shader).decode()
        print("Erro no Fragment Shader:")
        print(erro)

    return shader

def criar_programa_shader():
    vertex_shader = criar_vertex_shader()
    fragment_shader = criar_fragment_shader()

    programa = glCreateProgram()

    glAttachShader(programa, vertex_shader)
    glAttachShader(programa, fragment_shader)

    glLinkProgram(programa)

    if not glGetProgramiv(programa, GL_LINK_STATUS):
        erro = glGetProgramInfoLog(programa).decode()
        print("Erro ao linkar os shaders:")
        print(erro)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return programa



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
    vertices = criar_quadrado()
    vbo = criar_vbo(vertices)
    vao = criar_vao(vbo)

    shader_program = criar_programa_shader()

    # Loop principal
    while not glfw.window_should_close(janela):

    

        # Cor de fundo
        glClearColor(0.05, 0.05, 0.05, 1.0)

        # Limpa a tela
        glClear(GL_COLOR_BUFFER_BIT)

        # Usa nosso shader
        glUseProgram(shader_program)
        local_textura = glGetUniformLocation(shader_program, "textura")
        glUniform1i(local_textura, 0)

        # Usa nosso VAO
        glBindVertexArray(vao)

        # Usa a textura do escudo
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textura_escudo)
        
        
        # Desenha os 4 vértices
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

        # Desvincula
        glBindVertexArray(0)
        glUseProgram(0)

        # Atualiza a janela
        glfw.swap_buffers(janela)

        # Processa eventos
        glfw.poll_events()

if __name__ == "__main__":
    main()
