import os
from django.contrib import messages
from django.db import IntegrityError

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin

from braces.views import LoginRequiredMixin

from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm, ActivateForm, \
    ChangePasswordForm, ProfileChangeForm, ContactUsForm
from .utils import send_sms, determine_mime_type, generate_random_number
from .models import Mail, MailAttachment, ForgotPasswordToken, MailForward, AccountActivation
from advertisement.models import UserProfile


class HomePage(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('mail:mailforward_list'))
        return render(request, 'index.html')


class RegistrationView(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('mail:mailforward_list'))
        rform = RegistrationForm()
        form = LoginForm()
        return render(request, 'registration.html', {'form': form, 'rform': rform})

    def post(self, request):
        rform = RegistrationForm(request.POST, request.FILES or None)
        if rform.is_valid():
            country_codes = request.POST.get('country_codes')
            phone_number = request.POST.get('phone_number')
            phone_number = country_codes + phone_number
            if User.objects.filter(username=phone_number, is_active=True).exists():
                return render(request, 'registration.html', {'form': LoginForm(), 'rform': rform,
                                                    'number_error': 'User with that phone number already exists.'})

            password = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            avatar = request.FILES.get('avatar')
            # gender = request.POST.get('gender')
            # age_group = request.POST.get('age_group')
            # country = request.POST.get('country')
            activation_code = generate_random_number()
            message = 'User created for %s. Your activation code is %s' % (phone_number, str(activation_code))

            try:
                user = User.objects.get(username=phone_number)
                user.set_password(password)
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                user.save()
                send_sms(phone_number, message)
                profile = UserProfile.objects.get(user=user)
                profile.avatar = avatar
                # profile.gender = gender
                # profile.age_group = age_group
                # profile.country = country
                profile.save()

            except User.DoesNotExist:
                user = User.objects.create_user(username=phone_number, password=password)
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                user.is_active = False
                user.save()
                try:
                    UserProfile.objects.create(user=user, avatar=avatar)
                except IntegrityError:
                    pass
                send_sms(phone_number, message)

            activation = AccountActivation.objects.filter(user=user)
            if activation.exists():
                activation.delete()
            AccountActivation.objects.create(user=user, activation_code=activation_code)
            return HttpResponseRedirect(reverse('mail:activate_user'))
        else:
            return render(request, 'registration.html', {'form': LoginForm(), 'rform': rform})


class LoginView(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('mail:mailforward_list'))
        form = LoginForm()
        #from django.core.mail import EmailMessage
        #email = EmailMessage('Hello', 'This is the bodysss', 'hell@localhost', ['admin@localhost'])
        #email.attach_file('/home/sachitad/hi.py')
        #email.send(fail_silently=False)
        return render(request, 'login.html', {'form': form, 'rform': RegistrationForm()})

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = request.POST.get('phone_number')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

            else:
                return render(request, 'login.html', {'form': form, 'error': 'Username or password not correct.'})

        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, request):
        data = {'gender': request.user.userprofile.gender, 'age': request.user.userprofile.age,
                'country': request.user.userprofile.country}
        form = ProfileChangeForm(initial=data)
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        form = ProfileChangeForm(request.POST or None)
        if form.is_valid():
            gender = request.POST.get('gender')
            birthday = request.POST.get('password')
            country = request.POST.get('country')
            profile = get_object_or_404(UserProfile, user=request.user)
            if gender:
                profile.gender = gender
            if birthday:
                profile.age = birthday
            if country:
                profile.country = country
            profile.save()
            messages.success(request, 'Profile successfully updated.')
            return HttpResponseRedirect(reverse('mail:profile'))
        else:
            return render(request, 'profile.html', {'form': form})


class ActivateUser(generic.View):
    def get(self, request):
        form = ActivateForm()
        return render(request, 'activate_account.html', {'form': form})

    def post(self, request):
        form = ActivateForm(request.POST or None)
        if form.is_valid():
            country_codes = request.POST.get('country_codes')
            username = request.POST.get('phone_number')
            username = country_codes + username
            activation_code = request.POST.get('activation_code')
            activation = AccountActivation.objects.filter(user__username=username, activation_code=activation_code)
            if activation.exists():
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()
                AccountActivation.objects.filter(user=user).delete()
                messages.success(request, 'Account successfully activated.')
                return HttpResponseRedirect(reverse('mail:login'))
            else:
                return render(request, 'activate_account.html', {'form': form, 'error': 'Invalid Activation Code.'})

        else:
            return render(request, 'activate_account.html', {'form': form})


class MailListView(LoginRequiredMixin, generic.ListView):
    template_name = 'mail_list.html'
    context_object_name = 'mails'
    model = Mail
    paginate_by = 20

    def get_queryset(self):
        return Mail.objects.filter(user=self.request.user)


class MailDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'mail_detail.html'
    context_object_name = 'mail'
    model = Mail



class PasswordResetRequestView(generic.View):
    def get(self, request):
        return render(request, 'password_reset_request_form.html', {'form': PasswordResetRequestForm()})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        random_number = generate_random_number()
        if form.is_valid():
            country_codes = request.POST.get('country_codes')
            phone_number = request.POST.get('phone_number')
            phone_number = country_codes + phone_number
            user_obj = get_object_or_404(User, username=phone_number)

            token_check = ForgotPasswordToken.objects.filter(user=user_obj)

            if token_check:
                token_check.delete()

            ForgotPasswordToken.objects.create(user=user_obj, secret_token=random_number)
            send_sms(phone_number, message='Your token is %s' %(random_number))
            return HttpResponseRedirect(reverse('mail:reset_password'))

        else:
            return render(request, 'password_reset_request_form.html', {'form': form})


class PasswordResetView(generic.View):
    def get(self, request):
        return render(request, 'password_reset_form.html', {'form': PasswordResetForm()})


    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            country_codes = request.POST.get('country_codes')
            phone_number = request.POST.get('phone_number')
            phone_number = country_codes+ phone_number
            password = request.POST.get('new_password1')
            user_obj = get_object_or_404(User, username=phone_number)
            user_obj.set_password(password)
            user_obj.save()
            ForgotPasswordToken.objects.filter(user=user_obj).delete()
            send_sms(phone_number, message='Password Successfully Reset.')
            return HttpResponseRedirect(reverse('mail:login'))

        else:
            return render(request, 'password_reset_form.html', {'form': form})


class PasswordChangeView(LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'change_password.html', {'form': ChangePasswordForm()})


    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = request.POST.get('new_password1')
            old_password = request.POST.get('old_password')

            if not request.user.check_password(old_password):
                return render(request, 'change_password.html', {'form': form, 'error': 'Invalid old password.'})
            request.user.set_password(password)
            request.user.save()
            messages.success(request, 'Password successfully changed')
            return HttpResponseRedirect(reverse('mail:profile'))

        else:
            return render(request, 'change_password.html', {'form': form})


def download_attachment(request, pk):
    obj = get_object_or_404(MailAttachment, pk=pk)
    file_path = obj.attachment.name
    filename = file_path.split('/')[-1]
    mime_type = determine_mime_type(os.path.join(settings.MEDIA_ROOT, file_path))
    response = HttpResponse(obj.attachment, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' %(filename)
    return response


class MailForwardListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'emails'
    template_name = 'mail_forward_list.html'
    model = MailForward
    def get_queryset(self):
        super(MailForwardListView, self).get_queryset()
        return MailForward.objects.filter(user=self.request.user)


class MailForwardCreateView(LoginRequiredMixin, generic.CreateView):
    model = MailForward
    template_name = 'mail_forward_create.html'
    success_url = reverse_lazy('mail:mailforward_list')
    fields = ('email',)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MailForwardCreateView, self).form_valid(form)


class AboutView(generic.TemplateView):
    template_name = 'about.html'


class ContactView(SuccessMessageMixin, generic.CreateView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('mail:contact')
    success_message = 'Thank you for contacting us. We will get back to you shortly.'


class FAQView(generic.TemplateView):
    template_name = 'faq.html'


class PrivacyView(generic.TemplateView):
    template_name = 'privacy.html'


class ChangeAvatar(LoginRequiredMixin, generic.View):
    def get(self, request):
        return HttpResponseRedirect(reverse('mail:profile'))

    def post(self, request):
        avatar = request.POST.get('avatar')
        path = request.POST.get('path')
        if avatar:
            profile = get_object_or_404(UserProfile, user=request.user)
            profile.avatar = avatar
            profile.save()
            messages.success(request, 'Profile Avatar successfully changed.')
        return HttpResponseRedirect(path)