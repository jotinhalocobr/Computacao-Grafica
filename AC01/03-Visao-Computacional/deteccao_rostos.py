"""
AC01 — Visão Computacional: detecção de rostos

Baseado no exemplo público de detecção facial do OpenCV:
https://github.com/opencv/opencv/blob/4.x/samples/python/facedetect.py

O algoritmo analisa a imagem e informa onde existem rostos.
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt


PASTA_BASE = Path(__file__).resolve().parent
PASTA_IMAGENS = PASTA_BASE / "imagens"
PASTA_RESULTADOS = PASTA_BASE / "resultados"


def localizar_imagem():
    """Localiza uma imagem dentro da pasta de entrada."""
    extensoes = ("*.jpg", "*.jpeg", "*.png", "*.bmp")

    for extensao in extensoes:
        arquivos = list(PASTA_IMAGENS.glob(extensao))

        if arquivos:
            return arquivos[0]

    raise FileNotFoundError(
        "Nenhuma imagem foi encontrada na pasta 'imagens'."
    )


def detectar_rostos():
    """Detecta e destaca rostos presentes na imagem."""
    caminho_imagem = localizar_imagem()
    imagem = cv2.imread(str(caminho_imagem))

    if imagem is None:
        raise ValueError("O OpenCV não conseguiu abrir a imagem.")

    imagem_cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY,
    )

    caminho_classificador = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    classificador = cv2.CascadeClassifier(
        caminho_classificador
    )

    rostos = classificador.detectMultiScale(
        imagem_cinza,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
    )

    imagem_resultado = imagem.copy()

    for numero, (x, y, largura, altura) in enumerate(
        rostos,
        start=1,
    ):
        cv2.rectangle(
            imagem_resultado,
            (x, y),
            (x + largura, y + altura),
            (0, 255, 0),
            3,
        )

        cv2.putText(
            imagem_resultado,
            f"Rosto {numero}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    PASTA_RESULTADOS.mkdir(exist_ok=True)

    caminho_resultado = (
        PASTA_RESULTADOS / "rostos_detectados.png"
    )

    cv2.imwrite(
        str(caminho_resultado),
        imagem_resultado,
    )

    imagem_rgb = cv2.cvtColor(
        imagem_resultado,
        cv2.COLOR_BGR2RGB,
    )

    plt.figure(figsize=(10, 7))
    plt.imshow(imagem_rgb)
    plt.title(
        f"Visão Computacional — {len(rostos)} rosto(s) detectado(s)"
    )
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    print(f"Quantidade de rostos detectados: {len(rostos)}")
    print(f"Resultado salvo em: {caminho_resultado}")


if __name__ == "__main__":
    detectar_rostos()
