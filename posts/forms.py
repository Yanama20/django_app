from django import forms

from posts.models import Category, Post, Tag


class PostCreateForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField(max_length=156)
    content = forms.CharField(max_length=1056)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if (title and content) and (title.lower()==content.lower()):
            raise forms.ValidationError(message="Title and content should not be same")
        return cleaned_data
        
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and title.lower() == "python":
            raise forms.ValidationError(message="'Python' is not allowed value for title")
        return title
    
class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Поиск'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    orderings = (
        ('title', 'По заголовку'),
        ('-title', 'По заголовку в обратном порядке'),
        ('rate', 'По рейтингу'),
        ('-rate', 'По рейтингу в обратном порядке'),
        ('created_at', 'По дате создания'),
        ('-created_at', 'По дате создания в обратном порядке'),
    )
    ordering = forms.ChoiceField(
        choices=orderings, 
        widget=forms.Select(attrs={'class':'form-control'})
    )


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'rate']
        
