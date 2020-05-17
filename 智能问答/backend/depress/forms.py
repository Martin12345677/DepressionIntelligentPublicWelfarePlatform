from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput, label='密码')


class SignupForm(forms.Form):
    email = forms.EmailField(label='邮箱*')
    verify = forms.CharField(min_length=4, max_length=4, label='验证码*')
    name = forms.CharField(min_length=5, max_length=20, label='用户名*')
    password1 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput, label='密码*')
    password2 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput, label='确认密码*')

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            return email
        else:
            raise forms.ValidationError('该邮箱已被注册！')

    def clean(self):
        value = self.cleaned_data.get('password2')
        if value != self.cleaned_data.get('password1'):
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data


class ChangeDetailForm(forms.Form):
    email = forms.EmailField(label='邮箱', disabled=True, required=False)
    name = forms.CharField(min_length=5, max_length=20, label='用户名*')
    sex = forms.ChoiceField(choices=((None, '保密'), (True, '男'), (False, '女')), required=False, label='性别')
    address = forms.CharField(required=False, max_length=50, label='地址', widget=forms.TextInput)
    tel = forms.CharField(max_length=15, label='电话', required=False)
    newPassword1 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput, label='新密码', required=False)
    newPassword2 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput, label='确认新密码', required=False)

    def clean(self):
        value = self.cleaned_data.get('password1')
        if value != '' and value != self.cleaned_data.get('password2'):
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data
