import numpy as np  # type: ignore
from django.shortcuts import render  # type: ignore
from django.views import generic  # type: ignore
from PIL import Image

from .cat_cnn import abs_path_file, predict
from .forms import ImageUploadForm


class IndexView(generic.FormView):
    """
    画像認識フォーム画面

    """

    template_name = "ai/index.html"
    form_class = ImageUploadForm

    def form_valid(self, form):
        # アップロードファイル本体を取得
        file = form.cleaned_data["file"]

        # ファイルを、50*50にリサイズし, ３色にする。
        img = Image.open(file).resize((50, 50)).convert("RGB")

        # 学習時と同じ形に画像データを変換する
        img_array = np.asarray(img)
        img_cmp = []
        img_cmp.append(img_array)
        img_cmp_array = np.array(img_cmp)

        file_path = abs_path_file()

        # 推論した結果を、テンプレートへ渡して表示
        context = {
            "result": predict(img_cmp_array, file_path),
        }
        return render(self.request, "ai/index.html", context)


"""
image_size = 50
X = []

def index(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST)
        if form.is_valid():
            file = form.cleaned_data['file']
            img = Image.open(file).resize((image_size, image_size)).convert('RGB')
            img_array = np.asarray(img)
            X = []
            X.append(img_array)
            X = np.array(X)
            return render(request, 'ai/index.html', {'result': predict(X)})
        else:
            form = ImageUploadForm

    return render(request, 'ai/index.html', {'form': form})
"""
