from django import forms

from posts.models import Comment


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label='Search')


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Комментарий'
        }
