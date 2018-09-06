from django import forms
from blog_app.models import Post, Comment

class PostForm(forms.ModelForm):
    #do tego stworzyc post_form.html
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = { #stylowanie textinputow, atrrs łączą sie z plikiem CSS
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}), #potem w post_form.html skorzystamy z tych klas
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }

