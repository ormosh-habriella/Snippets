from django import forms
from MainApp.models import LANG_CHOICES, Snippet



class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["name", "lang", "code", "description"]
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
