import http.client, json

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .renderers import UserJSONRenderer
from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer, \
    OtpDetailsSerializer
from .models import User, OTPDetails, UserProfile

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        """"
        The create serializer, validate serializer, save serializer pattern
        below is common and you will see it a lot throughout this course and
        your own work later on. Get familiar with it.
        """

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            if serializer.data and 'token' in serializer.data:
                conn = http.client.HTTPConnection("2factor.in")
                payload = ""
                headers = {'content-type': "application/x-www-form-urlencoded"}
                conn.request("GET", "/API/V1/ca819fb2-e222-11ea-9fa5-0200cd936042/SMS/" +
                             serializer.data['phone_number'] + "/AUTOGEN",
                             payload, headers)
                res = conn.getresponse()
                data = res.read()

                OTPDetails.objects.get_or_create(
                    otp_response=data.decode("utf-8"),
                    user=User.objects.get(id=serializer.data['id'])
                )
                UserProfile.objects.get_or_create(user=User.objects.get(id=serializer.data['id']))

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)

        return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        """
        Notice here that we do not call `serializer.save()` like we did for
        the registration endpoint. This is because we don't  have
        anything to save. Instead, the `validate` method on our serializer
        handles everything we need.
        """

        serializer = self.serializer_class(context={'request': request},data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    @method_decorator(login_required)
    def post(self, request):
        request.user.auth_token.delete()
        # logout(request)
        return Response({'detail': "User is successfully logged out !!!"}, status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(login_required)
    def retrieve(self, request, *args, pk=None):
        """
        There is nothing to validate or save here. Instead, we just want the
        serializer to handle turning our `User` object into something that.
        """

        document = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        user_data = request.data.copy()
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=user_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OTPDetailsView(viewsets.ModelViewSet):
    queryset = OTPDetails.objects.all()
    serializer_class = OtpDetailsSerializer
    authentication_classes = (TokenAuthentication,)

    @method_decorator(login_required)
    def otp_view(self, request=None):
        if request:
            data = json.loads(request.body.decode('utf8'))
            response_data = dict()
            response_data['verify'] = False
            response_data['message'] = "Please resend OTP"
            if data:
                otp = data.get('otp')
                otp_session_id = OTPDetails.objects.filter(user=request.user).last()

                if otp_session_id and otp_session_id.otp_response:
                    otp_response = json.loads(otp_session_id.otp_response)
                    if otp_response['Status']:

                        conn = http.client.HTTPConnection("2factor.in")

                        payload = ""

                        headers = {'content-type': "application/x-www-form-urlencoded"}

                        conn.request("GET",
                                     "/API/V1/ca819fb2-e222-11ea-9fa5-0200cd936042/SMS/VERIFY/" +
                                     otp_response['Details'] + "/" + str(otp),
                                     payload, headers)

                        res = conn.getresponse()
                        data = res.read()
                        data = json.loads(data.decode("utf-8"))
                        response_data['message'] = data.get('Details')
                        if data.get('Status') == 'Success' and data.get('Details') == "OTP Matched":
                            response_data['verify'] = True
                            user = User.objects.filter(id=request.user.id).first()
                            user.is_active = True
                            user.otp_verify = True
                            user.save()
                            return Response(response_data, status=status.HTTP_200_OK)
                        if data.get('Status') == 'Error' and data.get('Details') == \
                            "SMS sending to this number is denied - Contact admin":
                            response_data['message'] = "Mobile number not found"
                            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            return Response(response_data, status=status.HTTP_202_ACCEPTED)

    @method_decorator(login_required)
    def otp_resent_view(self, request=None):
        if request:
            conn = http.client.HTTPConnection("2factor.in")
            payload = ""
            headers = {'content-type': "application/x-www-form-urlencoded"}
            conn.request("GET", "/API/V1/ca819fb2-e222-11ea-9fa5-0200cd936042/SMS/" +
                         request.user.phone_number + "/AUTOGEN",
                         payload, headers)
            res = conn.getresponse()
            data = res.read()
            OTPDetails.objects.get_or_create(
                otp_response=data.decode("utf-8"),
                user=User.objects.get(id=request.user.id)
            )
            return Response({'message': "OTP has sent to your registered mobile number"},
                            status=status.HTTP_202_ACCEPTED)
        return Response({'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
