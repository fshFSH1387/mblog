from django import  forms

#定义modleform
from blog.models import Tag

class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'