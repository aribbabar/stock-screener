from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={"placeholder": "Last Name"}))
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={"placeholder": "Email"}))
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={"placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))


class LoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={"placeholder": "Username"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={"placeholder": "Password"}))
