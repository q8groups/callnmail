from django.contrib.auth import get_user_model,authenticate
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .serializers import (RegistrationSerializer, PhoneNumberValidationSerializer, MailSerializer,
                          MailForwardSerializer, UserProfileSerializer, CountrySerializer, ForgotPasswordSerializer,
                          MailForwardSerializerDestroy, ChangePasswordSerializer,AdvertismentBannerSerializer)
from mail.utils import send_sms, generate_random_number, create_random_password
from .models import TokenValidation, Country
from mail.models import Mail, MailForward, ForgotPasswordToken
from advertisement.models import UserProfile,Banner


User = get_user_model()


class LoginView(generics.CreateAPIView):
    """
    Returns the token of the user if provided username and password is correct

    POST - Returns the token if credentials provided are correct
    """
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            try:
                user_profile = UserProfile.objects.get(user=serializer.object['user'])
                mail_forwards = MailForward.objects.filter(user=serializer.object['user'])
                serializer = UserProfileSerializer(user_profile)
                data = serializer.data
                mail_forwards_list = []
                for mail_forwards_object in mail_forwards:
                    mail_forwards_list.append(MailForwardSerializer(mail_forwards_object).data)
                data['user']['mail_forwards'] = mail_forwards_list
                data['token'] = token.key
            except UserProfile.DoesNotExist:
                data = {'token': token.key}

            return Response({'result': data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(generics.CreateAPIView):
    """
    Registers the user into the system

    POST - Register User
    """
    parser_classes = (FileUploadParser,)
    serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password1')
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            country = request.POST.get("country", "")
            avatar = request.FILES.get("avatar")

            if not User.objects.filter(username=phone_number).exists():
                user = User.objects.create_user(username=phone_number, password=password)
                user.is_active = False
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                #profile = UserProfile.objects.get_or_create(user=user, avatar=avatar, country=country.upper())
                #profile.save()
                random_number = generate_random_number()
                TokenValidation.objects.create(user=user, secret_token=random_number)
                send_sms(phone_number, " Here's your CallNMail Confirmation code " + str(random_number) + " Enter this in the app to verify your mobile number")
            else:
                return Response({'error': 'User already exists with this mobile number'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': 'SMS sent with activation code'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberValidateView(generics.CreateAPIView):
    """
    Validates the phone number with the activation code sent to the mobile of the user

    POST - Returns the token if the secret token and phone number pair is valid
    """
    serializer_class = PhoneNumberValidationSerializer
    parser_classes = (FormParser,)

    def post(self, request, format=None):
        serializer = PhoneNumberValidationSerializer(data=request.DATA)
        if serializer.is_valid():
            phone_number = request.POST.get('phone_number')
            secret_token = request.POST.get('secret_token')
            user = get_object_or_404(User, username=phone_number)
            if TokenValidation.objects.filter(user=user, secret_token=secret_token).exists():
                user.is_active = True
                user.save()

                token,created = Token.objects.get_or_create(user=user)
                mail_forwards = MailForward.objects.filter(user=user)
                mail_forwards_list = []
                for mail_forwards_object in mail_forwards:
                    mail_forwards_list.append(MailForwardSerializer(mail_forwards_object).data)

                try:
                    user_profile = UserProfile.objects.get(user=user)
                    serializer = UserProfileSerializer(user_profile)
                    data = serializer.data
                    data['token'] = token.key
                    data['user']['mail_forwards'] = mail_forwards_list
                except UserProfile.DoesNotExist:
                    data = {'token': token.key}
                return Response({'result': data})
            else:
                return Response({'non_field_errors': 'Invalid Token'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdvertismentBanner(generics.ListAPIView):
    serializer_class = AdvertismentBannerSerializer
    paginate_by = 1000

    def get_queryset(self):
        return Banner.objects.all().order_by('-priority')



class MailView(generics.ListAPIView):
    """
    This returns the mail of the logged in user

    GET - Returns the mail
    """
    serializer_class = MailSerializer
    permission_classes = (IsAuthenticated,)
    paginate_by = 20

    def get_queryset(self):
        return Mail.objects.filter(user=self.request.user)


class MailForwardView(generics.CreateAPIView):
    """
    This creates the mail forward for the logged in user

    POST - Create forwarding email for the logged in user
    """
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = MailForwardSerializer
    permission_classes = (IsAuthenticated,)

    def pre_save(self, obj):
        obj.user = self.request.user


class UserProfileCreateView(generics.CreateAPIView):
    """
    This creates user profile

    GET - Returns the user profile of the logged in user
    POST - Create/Update user profile. If user profile with logged in user already exists update otherwise create
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        mail_forwards = MailForward.objects.filter(user=self.request.user)
        serializer = UserProfileSerializer(user_profile)
        data = serializer.data
        mail_forwards_list = []
        for mail_forwards_object in mail_forwards:
            mail_forwards_list.append(MailForwardSerializer(mail_forwards_object).data)
        data['user']['mail_forwards'] = mail_forwards_list
        return Response(data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.DATA)
        if serializer.is_valid():
            user_profile = UserProfile.objects.get(user=self.request.user)
            gender = request.DATA.get('gender', '')
            age = request.DATA.get('age', '')
            country = request.DATA.get('country', '')
            avatar = request.FILES.get('avatar', '')
            if gender != '':
                user_profile.gender = gender
            if age != '':
                user_profile.age = age
            if avatar != '':
                user_profile.avatar = avatar
            if country != '':
                user_profile.country = country
            user_profile.save()
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryCreateView(generics.ListAPIView):
    """
    Country Information
    GET - Returns All Countries Codes and Names
    """
    serializer_class = CountrySerializer
    paginate_by = 1000

    def get_queryset(self):
        return Country.objects.all().order_by('-priority')


class ForgetPassword(generics.GenericAPIView):
    """
    Forgot Password
    POST - Sends activation code as sms
    """
    parser_classes = (FormParser,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            username = request.DATA.get('username')
            user = User.objects.get(username=username, is_active=True)
            random_number = generate_random_number()
            try:
                obj = ForgotPasswordToken.objects.get(user=user)
                send_sms(user.username, 'Your activation code is ' + str(obj.secret_token))
            except ForgotPasswordToken.DoesNotExist:
                ForgotPasswordToken.objects.create(user=user, secret_token=random_number)
                send_sms(user.username, 'Your activation code is ' + str(random_number))
            return Response({"success": "Sms has been sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.GenericAPIView):
    """
    Reset the password
    GET - If password parameter is supplied password is set to that parameter otherwise random password is
          created and sms is being sent
    """
    serializer_class = ForgotPasswordSerializer

    def get(self, request, secret_token, format=None):
        try:
            obj = ForgotPasswordToken.objects.get(secret_token=secret_token)
            password = request.GET.get("password", create_random_password())
            obj.user.set_password(password)
            obj.user.save()
            send_sms(obj.user.username, 'Your new passsword is ' + password)
            obj.delete()
            token = Token.objects.get(user=obj.user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        except (ForgotPasswordToken.DoesNotExist, ValueError):
            return Response("SMS NOT SENT", status=status.HTTP_200_OK)


class DeleteEmailLink(generics.GenericAPIView):
    model = MailForward
    serializer_class = MailForwardSerializerDestroy
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser,)

    def post(self, request,format=None):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            result = MailForward.objects.filter(user=self.request.user,email=request.DATA.get('email'))
            if result.count()>0:
                result.delete()
                return Response({"success": "Deleted Succesfully "}, status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Email Doesn't Exist"}, status.HTTP_404_NOT_FOUND)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser,)
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            result = authenticate(username=self.request.user.username,password=request.DATA.get("oldpassword"))
            if result:
                result.set_password(request.DATA.get("newpassword"))
                result.save()
                return Response({"success": "Password Changed Successfully"}, status.HTTP_200_OK)
            else:
                return Response({"error": "Old Password is not correct"}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



