from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class UpdateImageForm(forms.ModelForm):
    class Meta:
        fields = ('caption', )
        model = Image

    def __init__(self, *args, **kwargs):
        super(UpdateImageForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'caption',
            Submit('update', 'Update', css_class='btn primary')
        )


class CreateImageForm(forms.ModelForm):
    image = forms.FileField(label="",)
    caption = forms.CharField(label="", 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Write caption here...',}),
        max_length=1000, required=False)
    class Meta:
        fields = ('image', 'caption', )
        model = Image
		
  
