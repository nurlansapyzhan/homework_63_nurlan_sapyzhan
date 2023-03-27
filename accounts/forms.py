from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    email = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='', strip=False, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_confirm = forms.CharField(label='', strip=False, required=True,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))
    username = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(label='', required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Адрес электронной почты'}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email', 'password', 'password_confirm', 'avatar'
        )
        labels = {
            'avatar': 'Аватар'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.email = self.cleaned_data['email']
        if self.cleaned_data['avatar']:
            user.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
        return user


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['avatar'].widget.attrs['enctype'] = 'multipart/form-data'


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'avatar', 'user_info', 'phone_number', 'gender')
        labels = {
            'avatar': 'Аватар',
            'first_name': 'Имя',
            'user_info': 'Информация о пользователе',
            'phone_number': 'Номер телефона',
            'gender': 'Пол'
        }
