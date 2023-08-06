from django import forms # type: ignore

from imagekit.forms import ProcessedImageField # type: ignore
from imagekit.processors import ResizeToFill # type: ignore


class ImageUploadForm(forms.Form):
    file = forms.ImageField(label='画像ファイル')

    """ Djangoの画像を加工してくれる機能
    file = ProcessedImageField(spec_id='画像ファイル',
                            processors=[ResizeToFill(50, 50)],
                            format='JPEG',
                            options={'quality':60})
    """
