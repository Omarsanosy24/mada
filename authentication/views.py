from rest_framework import generics, status, permissions
from authentication.serializers import LoginSerializer, LogoutSerializer, UserInfoSer, ChangePasswordSer

from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from main_.permissions import HasAPIKeyWithTimeCheck


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            return Response(
                {
                    "status": True,
                    "message": _("logged successfully"),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            # r = serializer.data.get("email")
            return Response(
                {"status": False, "message": serializer.errors, "data": {}}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"status": True, "message": "logout done"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "message": serializer.errors},
                status=status.HTTP_200_OK,
            )


class UserInfoView(generics.GenericAPIView):
    serializer_class = UserInfoSer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ser = self.serializer_class(request.user, context={"request": request})
        return Response({
            "status": True,
            "message": _("all is done"),
            "results": ser.data
        })

    def patch(self, request):
        ser = UserInfoSer(data=request.data, instance=request.user, context={"request": request}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({
            "status": True,
            "message": _("all is done"),
            "results": ser.data
        })


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": _("password changed successfully"),
            })
        return Response({
            "status": False,
            "message": serializer.errors,
        })