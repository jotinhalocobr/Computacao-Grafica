"""
AC01 — Visualização Computacional com Matplotlib

Baseado nos exemplos públicos do Matplotlib:
https://github.com/matplotlib/matplotlib/tree/main/galleries/examples

Dados numéricos são transformados em representações visuais.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


PASTA_BASE = Path(__file__).resolve().parent
ARQUIVO_DADOS = PASTA_BASE / "dados.csv"
PASTA_RESULTADOS = PASTA_BASE / "resultados"


def carregar_dados():
    """Carrega as linguagens e quantidades do arquivo CSV."""
    linguagens = []
    estudantes = []

    with open(
        ARQUIVO_DADOS,
        mode="r",
        encoding="utf-8",
        newline="",
    ) as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            linguagens.append(linha["linguagem"])
            estudantes.append(int(linha["estudantes"]))

    return linguagens, estudantes


def criar_visualizacao():
    """Transforma os dados em gráficos de barras e setores."""
    linguagens, estudantes = carregar_dados()

    cores = [
        "#3776AB",
        "#E76F00",
        "#F7DF1E",
        "#00599C",
        "#68217A",
    ]

    figura, eixos = plt.subplots(
        1,
        2,
        figsize=(13, 6),
    )

    barras = eixos[0].bar(
        linguagens,
        estudantes,
        color=cores,
    )

    eixos[0].set_title("Preferência por linguagem")
    eixos[0].set_xlabel("Linguagem")
    eixos[0].set_ylabel("Quantidade de estudantes")
    eixos[0].bar_label(barras)
    eixos[0].grid(
        axis="y",
        linestyle="--",
        alpha=0.4,
    )

    eixos[1].pie(
        estudantes,
        labels=linguagens,
        colors=cores,
        autopct="%1.1f%%",
        startangle=90,
    )

    eixos[1].set_title("Distribuição percentual")

    figura.suptitle(
        "Visualização Computacional de Dados",
        fontsize=16,
    )

    plt.tight_layout()

    PASTA_RESULTADOS.mkdir(exist_ok=True)

    caminho_resultado = (
        PASTA_RESULTADOS / "visualizacao_linguagens.png"
    )

    plt.savefig(
        caminho_resultado,
        dpi=150,
        bbox_inches="tight",
    )

    plt.show()

    print(f"Dados lidos de: {ARQUIVO_DADOS}")
    print(f"Visualização salva em: {caminho_resultado}")


if __name__ == "__main__":
    criar_visualizacao()
