"""
AC01 — Processamento de Imagens com OpenCV

Exemplo baseado nos códigos públicos do OpenCV:
https://github.com/opencv/opencv/tree/4.x/samples/python

Uma imagem existente é transformada em outras imagens.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt


PASTA_BASE = Path(__file__).resolve().parent
PASTA_IMAGENS = PASTA_BASE / "imagens"
PASTA_RESULTADOS = PASTA_BASE / "resultados"


def localizar_imagem():
    """Localiza a primeira imagem disponível na pasta de entrada."""
    extensoes = ("*.jpg", "*.jpeg", "*.png", "*.bmp")

    for extensao in extensoes:
        arquivos = list(PASTA_IMAGENS.glob(extensao))

        if arquivos:
            return arquivos[0]

    raise FileNotFoundError(
        "Nenhuma imagem foi encontrada na pasta 'imagens'."
    )


def processar_imagem():
    """Aplica transformações em uma fotografia existente."""
    caminho_imagem = localizar_imagem()
    imagem_original = cv2.imread(str(caminho_imagem))

    if imagem_original is None:
        raise ValueError("O OpenCV não conseguiu abrir a imagem.")

    tons_cinza = cv2.cvtColor(
        imagem_original,
        cv2.COLOR_BGR2GRAY,
    )

    desfoque = cv2.GaussianBlur(
        tons_cinza,
        (11, 11),
        0,
    )

    bordas = cv2.Canny(
        desfoque,
        50,
        150,
    )

    PASTA_RESULTADOS.mkdir(exist_ok=True)

    cv2.imwrite(
        str(PASTA_RESULTADOS / "tons_cinza.png"),
        tons_cinza,
    )

    cv2.imwrite(
        str(PASTA_RESULTADOS / "desfoque_gaussiano.png"),
        desfoque,
    )

    cv2.imwrite(
        str(PASTA_RESULTADOS / "bordas_canny.png"),
        bordas,
    )

    imagem_rgb = cv2.cvtColor(
        imagem_original,
        cv2.COLOR_BGR2RGB,
    )

    figura, eixos = plt.subplots(2, 2, figsize=(12, 8))

    eixos[0, 0].imshow(imagem_rgb)
    eixos[0, 0].set_title("Imagem original")

    eixos[0, 1].imshow(tons_cinza, cmap="gray")
    eixos[0, 1].set_title("Escala de cinza")

    eixos[1, 0].imshow(desfoque, cmap="gray")
    eixos[1, 0].set_title("Desfoque Gaussiano")

    eixos[1, 1].imshow(bordas, cmap="gray")
    eixos[1, 1].set_title("Detecção de bordas Canny")

    for eixo in eixos.flat:
        eixo.axis("off")

    plt.suptitle("Processamento de Imagens com OpenCV")
    plt.tight_layout()

    caminho_comparacao = (
        PASTA_RESULTADOS / "comparacao_processamento.png"
    )

    plt.savefig(
        caminho_comparacao,
        dpi=150,
        bbox_inches="tight",
    )

    plt.show()

    print(f"Imagem utilizada: {caminho_imagem}")
    print(f"Resultados salvos em: {PASTA_RESULTADOS}")


if __name__ == "__main__":
    processar_imagem()
