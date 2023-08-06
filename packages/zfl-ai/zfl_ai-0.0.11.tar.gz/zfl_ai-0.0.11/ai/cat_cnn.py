"""

画像が挿入されると、猫・ライオン・チーターを学習したCNNモデルをロードして.

与えられた画像に対しての予測結果を出力する.

"""

import os

from tensorflow.keras.models import load_model  # type: ignore

classes = ["猫", "ライオン", "チーター"]


def abs_path_file():
    """
    学習済みモデルの取得
    """

    file_path = "ai/catai_cnn_new.h5"
    if not os.path.isfile(file_path):
        abs_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(abs_path)
        file_path = os.path.join(dir_path, "catai_cnn_new.h5")
    return file_path


def predict(img, file_path):
    """
    モデルのロード
    """

    if not os.path.isfile(file_path):
        raise ValueError
    model = load_model(file_path)
    result = model.predict([img])[0]
    predicted = result.argmax()
    return str(classes[predicted])
