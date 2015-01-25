from django import forms
from django.contrib.auth.models import User


from .models import ForgotPasswordToken
from advertisement.models import UserProfile


class RegistrationForm(forms.ModelForm):
    phone_number = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password (Again)')


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if User.objects.filter(username=phone_number, is_active=True):
            raise forms.ValidationError('This phone number is already in use.')

        if phone_number < 0:
            raise forms.ValidationError('Invalid phone number.')

        return phone_number


    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data

    class Meta:
        model = UserProfile
        exclude = ('user',)

class LoginForm(forms.Form):
    phone_number = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordResetRequestForm(forms.Form):
    phone_number = forms.IntegerField()

    def clean(self):
        if not User.objects.filter(username=self.cleaned_data.get('phone_number')):
            raise forms.ValidationError('This phone number is not registered.')

        return self.cleaned_data



class PasswordResetForm(forms.Form):
    phone_number = forms.IntegerField()
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='New Password (Again)')
    secret_token = forms.IntegerField()



    def clean_phone_number(self):
        if not User.objects.filter(username=self.cleaned_data.get('phone_number'), is_active=True):
            raise forms.ValidationError('This phone number is not registered.')

        return self.cleaned_data.get('phone_number')

    def clean_secret_token(self):
        try:
            user_obj = User.objects.get(username=self.cleaned_data.get('phone_number'))
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid token.')


        if not ForgotPasswordToken.objects.filter(user=user_obj, secret_token=self.cleaned_data.get('secret_token')):
            raise forms.ValidationError('Invalid token.')

        return self.cleaned_data.get('secret_token')

    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data

