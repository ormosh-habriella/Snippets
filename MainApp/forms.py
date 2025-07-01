from django import forms

class SnippetForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Название сниппета",
            }
        )
    )
    lang = forms.ChoiceField(
        label="",
        choices=[
            ('', '--- Выберите язык ---'),
            ("python", "Python"),
            ("cpp", "C++"),
            ("java", "Java"),
            ("javascript", "JavaScript")
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    code = forms.CharField(
        label="",
        max_length=5000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите ваш код здесь'})
    )