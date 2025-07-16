from django import forms
from MainApp.models import LANG_CHOICES, Snippet, Comment
from django.contrib.auth.models import User


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["name", "lang", "code", "description", "public"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название сниппета'}),
            'lang': forms.Select(
                choices=LANG_CHOICES,
                attrs={'class': 'form-control'}
            ),
            'code': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Код сниппета'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание сниппета'}),
        }

        # Пример валидации на уровне поля (опционально)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Название должно содержать не менее 3 символов.")

        if len(name) >20:
            raise forms.ValidationError("Название должно содержать не больше 20 символов.")
        return name

    # Пример валидации на уровне формы (опционально)
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        description = cleaned_data.get('description')

        if code and len(code) < 10 and not description:
            # Если код очень короткий, а описание отсутствует, добавить ошибку
            self.add_error(None, "Для очень короткого кода требуется описание.")  # Общая ошибка формы
        return cleaned_data


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
        }

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'confirm password'})
    )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 == password2:
            return password2
        raise forms.ValidationError("Пароли пустые или не совпадают")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите ваш комментарий здесь...',
                    'rows': 5,
                    'cols': 30,
                }),
        }
