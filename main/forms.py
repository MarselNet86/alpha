from django import forms
from .models import User


class LoginForm(forms.Form):
    name = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите текущий пароль'
            }
        )
    )

    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите новый пароль'
            }
        )
    )

    secondary_password = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль еще раз'
            }
        )
    )



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'role', 'last_login_date', 'is_blocked', 'is_password_changed']
        widgets = {
            'last_login_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'role', 'last_login_date', 'is_blocked', 'is_password_changed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'last_login_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }