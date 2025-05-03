import boto3
from botocore.config import Config
from rest_framework import generics, status, permissions
from rest_framework.views import APIView

from authentication.serializers import LoginSerializer, LogoutSerializer, UserInfoSer, ChangePasswordSer

from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from mada.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME, AWS_S3_ENDPOINT_URL, \
    AWS_STORAGE_BUCKET_NAME
from main_.permissions import HasAPIKeyWithTimeCheck


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # permission_classes = [permissions.AllowAny]

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


class GeneratePresignedUrl(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(region_name=AWS_S3_REGION_NAME),
            endpoint_url=AWS_S3_ENDPOINT_URL
        )

        bucket_name = AWS_STORAGE_BUCKET_NAME
        object_name = request.query_params.get('file_name')  # اسم الملف الذي سيتم رفعه
        # file_type = request.query_params.get('file_type')  # اسم الملف الذي سيتم رفعه

        try:
            # توليد رابط موقّع
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_name,
                    # "ContentType": "image/webp",
                    # "conditions": [{"Content-Type": "image/webp"}]

                },
                ExpiresIn=3600  # صلاحية الرابط لمدة ساعة
            )
            return Response({"url": presigned_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
