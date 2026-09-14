"""
AC02 — Transformações Geométricas 2D

Resolve e representa graficamente os dez exercícios da atividade
utilizando NumPy e Matplotlib.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PASTA_RESULTADOS = Path(__file__).resolve().parent / "resultados"


# ---------------------------------------
# Funções das transformações geométricas
# ---------------------------------------

def translacao(pontos, tx, ty):
    """Translada os pontos por meio do vetor (tx, ty)."""
    return pontos + np.array([tx, ty], dtype=float)


def escala(pontos, sx, sy=None):
    """Aplica escala uniforme ou não uniforme."""
    if sy is None:
        sy = sx

    matriz = np.array([
        [sx, 0],
        [0, sy],
    ], dtype=float)

    return pontos @ matriz.T


def rotacao(pontos, angulo_graus):
    """Rotaciona os pontos ao redor da origem."""
    angulo = np.radians(angulo_graus)

    matriz = np.array([
        [np.cos(angulo), -np.sin(angulo)],
        [np.sin(angulo), np.cos(angulo)],
    ])

    return pontos @ matriz.T


def reflexao_x(pontos):
    """Reflete os pontos em relação ao eixo x."""
    matriz = np.array([
        [1, 0],
        [0, -1],
    ], dtype=float)

    return pontos @ matriz.T


def reflexao_y(pontos):
    """Reflete os pontos em relação ao eixo y."""
    matriz = np.array([
        [-1, 0],
        [0, 1],
    ], dtype=float)

    return pontos @ matriz.T


def cisalhamento_horizontal(pontos, k):
    """Aplica cisalhamento horizontal: x' = x + k*y."""
    matriz = np.array([
        [1, k],
        [0, 1],
    ], dtype=float)

    return pontos @ matriz.T


# -----------------------------------------
# Funções para apresentação dos resultados
# -----------------------------------------

def formatar_numero(valor):
    """Formata números e elimina resultados como -0.00."""
    if abs(valor) < 1e-10:
        valor = 0.0

    return f"{valor:.2f}".rstrip("0").rstrip(".")


def plotar_etapas(
    etapas,
    titulo,
    nome_arquivo,
    rotulos,
    poligono=False,
):
    """Plota e salva todas as etapas de uma transformação."""
    cores = ["#1565C0", "#2E7D32", "#EF6C00", "#C62828"]
    estilos = ["-", "--", "-.", ":"]
    deslocamentos = [(7, -14), (7, 7), (7, -14), (7, 7)]

    figura, eixo = plt.subplots(figsize=(8, 7))

    for indice, (nome, pontos) in enumerate(etapas):
        cor = cores[indice % len(cores)]
        estilo = estilos[indice % len(estilos)]

        if poligono:
            pontos_fechados = np.vstack([pontos, pontos[0]])

            eixo.plot(
                pontos_fechados[:, 0],
                pontos_fechados[:, 1],
                marker="o",
                color=cor,
                linestyle=estilo,
                linewidth=2,
                label=nome,
            )
        else:
            eixo.scatter(
                pontos[:, 0],
                pontos[:, 1],
                color=cor,
                s=90,
                label=nome,
                zorder=3,
            )

        for rotulo, (x, y) in zip(rotulos, pontos):
            texto = (
                f"{rotulo} "
                f"({formatar_numero(x)}, {formatar_numero(y)})"
            )

            eixo.annotate(
                texto,
                (x, y),
                xytext=deslocamentos[indice % len(deslocamentos)],
                textcoords="offset points",
                fontsize=9,
                color=cor,
            )

    if not poligono and len(etapas) > 1:
        caminho = np.vstack([pontos for _, pontos in etapas])

        eixo.plot(
            caminho[:, 0],
            caminho[:, 1],
            color="#666666",
            linestyle=":",
            alpha=0.7,
        )

    eixo.axhline(0, color="black", linewidth=0.8)
    eixo.axvline(0, color="black", linewidth=0.8)
    eixo.set_xlabel("Eixo x")
    eixo.set_ylabel("Eixo y")
    eixo.set_title(titulo)
    eixo.grid(True, linestyle="--", alpha=0.4)
    eixo.legend()
    eixo.axis("equal")
    eixo.margins(0.25)

    figura.tight_layout()

    figura.savefig(
        PASTA_RESULTADOS / nome_arquivo,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(figura)


def imprimir_resultado(numero_exercicio, rotulos, pontos):
    """Mostra as coordenadas finais no terminal."""
    coordenadas = ", ".join(
        f"{rotulo}'({formatar_numero(x)}, {formatar_numero(y)})"
        for rotulo, (x, y) in zip(rotulos, pontos)
    )

    print(f"Exercício {numero_exercicio}: {coordenadas}")


# -------------------------
# Resolução dos exercícios
# -------------------------

def executar_exercicios():
    PASTA_RESULTADOS.mkdir(exist_ok=True)

    # Exercício 1 — Translação simples
    ponto = np.array([[2, 3]], dtype=float)
    resultado = translacao(ponto, 4, -2)

    plotar_etapas(
        [("Original", ponto), ("Transladado", resultado)],
        "Exercício 1 — Translação simples",
        "exercicio_01.png",
        ["P"],
    )

    imprimir_resultado(1, ["P"], resultado)

    # Exercício 2 — Escala uniforme
    triangulo = np.array([
        [1, 1],
        [3, 1],
        [2, 4],
    ], dtype=float)

    resultado = escala(triangulo, 2)

    plotar_etapas(
        [("Original", triangulo), ("Escala 2", resultado)],
        "Exercício 2 — Escala uniforme",
        "exercicio_02.png",
        ["A", "B", "C"],
        poligono=True,
    )

    imprimir_resultado(2, ["A", "B", "C"], resultado)

    # Exercício 3 — Escala não uniforme
    resultado = escala(triangulo, 2, 0.5)

    plotar_etapas(
        [
            ("Original", triangulo),
            ("Escala (2; 0,5)", resultado),
        ],
        "Exercício 3 — Escala não uniforme",
        "exercicio_03.png",
        ["A", "B", "C"],
        poligono=True,
    )

    imprimir_resultado(3, ["A", "B", "C"], resultado)

    # Exercício 4 — Rotação de 90° anti-horária
    ponto = np.array([[1, 0]], dtype=float)
    resultado = rotacao(ponto, 90)

    plotar_etapas(
        [
            ("Original", ponto),
            ("Rotação 90° anti-horária", resultado),
        ],
        "Exercício 4 — Rotação em torno da origem",
        "exercicio_04.png",
        ["P"],
    )

    imprimir_resultado(4, ["P"], resultado)

    # Exercício 5 — Rotação de 45° horária
    quadrado = np.array([
        [1, 1],
        [1, 4],
        [4, 4],
        [4, 1],
    ], dtype=float)

    resultado = rotacao(quadrado, -45)

    plotar_etapas(
        [
            ("Original", quadrado),
            ("Rotação 45° horária", resultado),
        ],
        "Exercício 5 — Rotação de um quadrado",
        "exercicio_05.png",
        ["A", "B", "C", "D"],
        poligono=True,
    )

    imprimir_resultado(
        5,
        ["A", "B", "C", "D"],
        resultado,
    )

    # Exercício 6 — Reflexão no eixo y
    ponto = np.array([[2, 5]], dtype=float)
    resultado = reflexao_y(ponto)

    plotar_etapas(
        [
            ("Original", ponto),
            ("Reflexão no eixo y", resultado),
        ],
        "Exercício 6 — Reflexão no eixo y",
        "exercicio_06.png",
        ["P"],
    )

    imprimir_resultado(6, ["P"], resultado)

    # Exercício 7 — Reflexão no eixo x
    triangulo_reflexao = np.array([
        [2, 3],
        [4, 3],
        [3, 5],
    ], dtype=float)

    resultado = reflexao_x(triangulo_reflexao)

    plotar_etapas(
        [
            ("Original", triangulo_reflexao),
            ("Reflexão no eixo x", resultado),
        ],
        "Exercício 7 — Reflexão de um triângulo",
        "exercicio_07.png",
        ["A", "B", "C"],
        poligono=True,
    )

    imprimir_resultado(7, ["A", "B", "C"], resultado)

    # Exercício 8 — Cisalhamento horizontal
    ponto = np.array([[2, 3]], dtype=float)
    resultado = cisalhamento_horizontal(ponto, 2)

    plotar_etapas(
        [
            ("Original", ponto),
            ("Cisalhamento k=2", resultado),
        ],
        "Exercício 8 — Cisalhamento horizontal",
        "exercicio_08.png",
        ["P"],
    )

    imprimir_resultado(8, ["P"], resultado)

    # Exercício 9 — Composição de transformações
    ponto_original = np.array([[3, 2]], dtype=float)
    apos_translacao = translacao(ponto_original, 1, -1)
    apos_rotacao = rotacao(apos_translacao, 90)
    resultado = escala(apos_rotacao, 2)

    plotar_etapas(
        [
            ("Original", ponto_original),
            ("Após translação", apos_translacao),
            ("Após rotação", apos_rotacao),
            ("Após escala", resultado),
        ],
        "Exercício 9 — Composição de transformações",
        "exercicio_09.png",
        ["P"],
    )

    imprimir_resultado(9, ["P"], resultado)

    # Exercício 10 — Combinação em um retângulo
    retangulo = np.array([
        [1, 1],
        [5, 1],
        [5, 3],
        [1, 3],
    ], dtype=float)

    apos_translacao = translacao(retangulo, -2, 3)
    apos_escala = escala(apos_translacao, 1.5, 0.5)
    resultado = reflexao_y(apos_escala)

    plotar_etapas(
        [
            ("Original", retangulo),
            ("Após translação", apos_translacao),
            ("Após escala", apos_escala),
            ("Após reflexão", resultado),
        ],
        "Exercício 10 — Combinação de transformações",
        "exercicio_10.png",
        ["A", "B", "C", "D"],
        poligono=True,
    )

    imprimir_resultado(
        10,
        ["A", "B", "C", "D"],
        resultado,
    )

    print()
    print(f"Gráficos salvos em: {PASTA_RESULTADOS}")


if __name__ == "__main__":
    executar_exercicios()
