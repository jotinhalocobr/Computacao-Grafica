"""
AC01 — Síntese de Imagens com Ray Tracing

Exemplo didático baseado nos conceitos apresentados no repositório público:
https://github.com/rdgarce/Ray_tracing

A imagem é sintetizada a partir de objetos matemáticos, câmera e iluminação.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


LARGURA = 480
ALTURA = 320

CAMERA = np.array([0.0, 0.0, -1.5])
LUZ = np.array([-3.0, 4.0, -2.0])

OBJETOS = [
    {
        "centro": np.array([-0.55, -0.10, 3.0]),
        "raio": 0.55,
        "cor": np.array([0.90, 0.15, 0.12]),
        "brilho": 80,
    },
    {
        "centro": np.array([0.65, -0.15, 3.7]),
        "raio": 0.70,
        "cor": np.array([0.10, 0.35, 0.95]),
        "brilho": 120,
    },
    {
        "centro": np.array([0.0, 0.62, 4.2]),
        "raio": 0.42,
        "cor": np.array([0.15, 0.85, 0.35]),
        "brilho": 60,
    },
    {
        "centro": np.array([0.0, -1001.0, 4.0]),
        "raio": 1000.0,
        "cor": np.array([0.55, 0.55, 0.60]),
        "brilho": 20,
    },
]


def normalizar(vetor):
    """Transforma um vetor em vetor unitário."""
    return vetor / np.linalg.norm(vetor)


def intersectar_esfera(origem, direcao, centro, raio):
    """Calcula a distância entre um raio e uma esfera."""
    origem_centro = origem - centro

    a = np.dot(direcao, direcao)
    b = 2.0 * np.dot(origem_centro, direcao)
    c = np.dot(origem_centro, origem_centro) - raio**2

    discriminante = b**2 - 4 * a * c

    if discriminante < 0:
        return np.inf

    raiz = np.sqrt(discriminante)
    distancia_1 = (-b - raiz) / (2 * a)
    distancia_2 = (-b + raiz) / (2 * a)

    distancias_validas = [
        distancia
        for distancia in (distancia_1, distancia_2)
        if distancia > 0.0001
    ]

    if not distancias_validas:
        return np.inf

    return min(distancias_validas)


def objeto_mais_proximo(origem, direcao):
    """Procura o primeiro objeto atingido pelo raio."""
    objeto_encontrado = None
    menor_distancia = np.inf

    for objeto in OBJETOS:
        distancia = intersectar_esfera(
            origem,
            direcao,
            objeto["centro"],
            objeto["raio"],
        )

        if distancia < menor_distancia:
            menor_distancia = distancia
            objeto_encontrado = objeto

    return objeto_encontrado, menor_distancia


def calcular_cor(origem, direcao):
    """Calcula a cor do pixel usando iluminação e sombra."""
    objeto, distancia = objeto_mais_proximo(origem, direcao)

    if objeto is None:
        altura = max(direcao[1], 0.0)
        return np.array([0.04, 0.07, 0.14]) + altura * np.array(
            [0.15, 0.18, 0.25]
        )

    ponto = origem + distancia * direcao
    normal = normalizar(ponto - objeto["centro"])

    cor = objeto["cor"] * 0.15

    vetor_luz = LUZ - ponto
    distancia_luz = np.linalg.norm(vetor_luz)
    direcao_luz = normalizar(vetor_luz)

    origem_sombra = ponto + normal * 0.001
    objeto_sombra, distancia_sombra = objeto_mais_proximo(
        origem_sombra,
        direcao_luz,
    )

    existe_sombra = (
        objeto_sombra is not None
        and distancia_sombra < distancia_luz
    )

    if not existe_sombra:
        intensidade_difusa = max(np.dot(normal, direcao_luz), 0.0)
        cor += objeto["cor"] * 0.75 * intensidade_difusa

        direcao_visao = normalizar(CAMERA - ponto)
        reflexao = (
            2 * normal * np.dot(normal, direcao_luz) - direcao_luz
        )

        intensidade_especular = max(
            np.dot(reflexao, direcao_visao),
            0.0,
        ) ** objeto["brilho"]

        cor += np.array([1.0, 1.0, 1.0]) * 0.50 * intensidade_especular

    return np.clip(cor, 0.0, 1.0)


def renderizar():
    """Percorre os pixels e sintetiza a imagem."""
    imagem = np.zeros((ALTURA, LARGURA, 3))

    valores_x = np.linspace(-1.4, 1.4, LARGURA)
    valores_y = np.linspace(0.9, -0.9, ALTURA)

    for linha, y in enumerate(valores_y):
        for coluna, x in enumerate(valores_x):
            ponto_tela = np.array([x, y, 0.0])
            direcao = normalizar(ponto_tela - CAMERA)

            imagem[linha, coluna] = calcular_cor(CAMERA, direcao)

    return imagem


def salvar_imagem(imagem):
    """Salva e exibe o resultado renderizado."""
    pasta_resultados = Path(__file__).parent / "resultados"
    pasta_resultados.mkdir(exist_ok=True)

    caminho_saida = pasta_resultados / "cena_ray_tracing.png"

    plt.figure(figsize=(10, 7))
    plt.imshow(imagem)
    plt.title("Síntese de Imagens — Ray Tracing")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.show()

    print(f"Imagem salva em: {caminho_saida}")


if __name__ == "__main__":
    print("Renderizando a cena. Aguarde...")
    cena = renderizar()
    salvar_imagem(cena)
