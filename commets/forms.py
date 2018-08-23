from django import  forms

#定义modleform
from commets.models import Comment


class CommentModleForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','url','context']
        
