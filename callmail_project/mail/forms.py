from django import forms
from django.contrib.auth.models import User


from .models import ForgotPasswordToken, ContactUs
from advertisement.models import UserProfile


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=False)
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Mobile', 'required': 'true'}),
                                      required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'required': 'true'}))

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
        fields = ('first_name', 'last_name', 'phone_number', 'avatar', 'password1', 'password2')


class LoginForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Mobile', 'required': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))


class ActivateForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Mobile', 'required': 'true'}))
    activation_code = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Activation Code', 'required': 'true'}))



class PasswordResetRequestForm(forms.Form):
    phone_number = forms.IntegerField()

    def clean(self):
        if not User.objects.filter(username=self.cleaned_data.get('phone_number')):
            raise forms.ValidationError('This phone number is not registered.')

        return self.cleaned_data



class PasswordResetForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Mobile', 'required': 'true'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'required': 'true'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat New Password', 'required': 'true'}))
    secret_token = forms.IntegerField(widget=forms.PasswordInput(attrs={'placeholder': 'Secret Token', 'required': 'true'}))



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


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'required': 'true'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'required': 'true'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat New Password', 'required': 'true'}))

    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'age', 'country')


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'contact_email': forms.TextInput(attrs={'placeholder': 'Contact Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'}),

        }
