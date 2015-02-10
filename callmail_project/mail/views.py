import os
import user

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings

from braces.views import LoginRequiredMixin

from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from .utils import send_sms, determine_mime_type, generate_random_number
from .models import Mail, MailAttachment, ForgotPasswordToken, MailForward
from advertisement.models import UserProfile


class HomePage(generic.TemplateView):
    template_name = 'index.html'


class RegistrationView(generic.View):
    def get(self, request):
        rform = RegistrationForm()
        form = LoginForm()
        return render(request, 'registration.html', {'form': form, 'rform': rform})

    def post(self, request):
        rform = RegistrationForm(request.POST, request.FILES or None)
        if rform.is_valid():
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password1')
            avatar = request.POST.get('avatar')
            # gender = request.POST.get('gender')
            # age_group = request.POST.get('age_group')
            # country = request.POST.get('country')
            message = 'User created for %s' %(phone_number)

            try:
                user = User.objects.get(username=phone_number)
                user.is_active = True
                user.set_password(password)
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
                UserProfile.objects.create(user=user, avatar=avatar)
                send_sms(phone_number, message)

            return HttpResponseRedirect(reverse('mail:index'))
        else:
            return render(request, 'registration.html', {'form': LoginForm(), 'rform': rform})


class LoginView(generic.View):
    def get(self, request):
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
            phone_number = request.POST.get('phone_number')
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
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('new_password1')
            user_obj = get_object_or_404(User, username=phone_number)
            user_obj.set_password(password)
            user_obj.save()
            ForgotPasswordToken.objects.filter(user=user_obj).delete()
            send_sms(phone_number, message='Password Successfully Reset.')
            return HttpResponseRedirect(reverse('mail:login'))

        else:
            return render(request, 'password_reset_form.html', {'form': form})


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