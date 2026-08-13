import glfw
from OpenGL.GL import *
import numpy as np


# Vertices
vertices = np.array([
    -0.05,  0.3,
     0.05,  0.3,
    -0.05, -0.3,
     0.05, -0.3
], dtype=np.float32)

# Indices
indices = np.array([
    0, 1, 2,
    1, 3, 2
], dtype=np.uint32)


# Matriz de translacao
def matriz_translacao(x, y):
    return np.array([
        [1.0, 0.0, 0.0, x],
        [0.0, 1.0, 0.0, y],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)


def criar_vao():
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    # Ativa VAO
    glBindVertexArray(vao)

    # Confg VBO
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    # Config EBO
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        indices.nbytes,
        indices,
        GL_STATIC_DRAW
    )

    # Posição dos vertices
    glVertexAttribPointer(
        0,
        2,
        GL_FLOAT,
        GL_FALSE,
        2 * vertices.itemsize,
        None
    )

    glEnableVertexAttribArray(0)

    # DEsvincula VAO
    glBindVertexArray(0)

    return vao


# Vertex Shader
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec2 posicao;

uniform mat4 transformacao;

void main()
{
    gl_Position = transformacao * vec4(posicao, 0.0, 1.0);
}
"""


# Fragment Shader
fragment_shader_source = """
#version 330 core

out vec4 cor;

void main()
{
    cor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""


def criar_shader_program():
    
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)

    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(vertex_shader).decode()
        print("Erro no Vertex Shader:")
        print(erro)

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)

    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        erro = glGetShaderInfoLog(fragment_shader).decode()
        print("Erro no Fragment Shader:")
        print(erro)

    shader_program = glCreateProgram()

    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)

    glLinkProgram(shader_program)

    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        erro = glGetProgramInfoLog(shader_program).decode()
        print("Erro ao linkar o Shader Program:")
        print(erro)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program


raquete_esquerda_x = -0.9
raquete_esquerda_y = 0.0

raquete_direita_x = 0.9
raquete_direita_y = 0.0


def main():

    # Inicializa o GLFW
    if not glfw.init():
        print("Não foi possível inicializar o GLFW.")
        return

    # Cria a janela
    janela = glfw.create_window(
        800,
        600,
        "Pong - CGF",
        None,
        None
    )

    if not janela:
        glfw.terminate()
        print("Não foi possível criar a janela.")
        return

    # Define a janela como contexto atual do OpenGL
    glfw.make_context_current(janela)

    vao = criar_vao()
    shader_program = criar_shader_program()

    transformacao = matriz_translacao(
        raquete_esquerda_x,
        raquete_esquerda_y
    )

    transformacao_direita = matriz_translacao(
        raquete_direita_x,
        raquete_direita_y
    )

    local_transformacao = glGetUniformLocation(
        shader_program,
        "transformacao"
    )

    # Loop principal
    while not glfw.window_should_close(janela):

        # Cor de fundo
        glClearColor(0.05, 0.05, 0.05, 1.0)

        # Limpa a tela
        glClear(GL_COLOR_BUFFER_BIT)

        # Usa nosso shader
        glUseProgram(shader_program)

        # Envia transformação da raquete esquerda
        glUniformMatrix4fv(
            local_transformacao,
            1,
            GL_TRUE,
            transformacao
        )

        # Usa nosso VAO
        glBindVertexArray(vao)

        # Desenha raquete esquerda
        glDrawElements(
            GL_TRIANGLES,
            6,
            GL_UNSIGNED_INT,
            None
        )

        # Envia transformação da raquete direita
        glUniformMatrix4fv(
            local_transformacao,
            1,
            GL_TRUE,
            transformacao_direita
        )

        # Desenha raquete direita
        glDrawElements(
            GL_TRIANGLES,
            6,
            GL_UNSIGNED_INT,
            None
        )

        # Desvincula
        glBindVertexArray(0)
        glUseProgram(0)

        # Atualiza a janela
        glfw.swap_buffers(janela)

        # Processa eventos
        glfw.poll_events()

    # Encerra o GLFW
    glfw.terminate()


if __name__ == "__main__":
    main()