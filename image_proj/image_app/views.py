from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from image_app.models import Profile, User
from image_app.serializers import ProfileSerializer, UserSerializer
from image_app.http import invoke_image_processing
from image_app.utils import download_image


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"

    def _process_image(self, request_data: dict):
        b64_image = download_image(request_data["image"])
        invoke_result = invoke_image_processing(b64_image)
        if not invoke_result:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return invoke_result

    def create(self, request):
        data: dict = request.data
        if data.get("image"):
            img_src = self._process_image(request_data=data)
            profile = Profile(**data, image=img_src)
            profile.save()
            return profile

        return Profile.objects.create(**data)

    def partial_update(self, request, id: int):
        q = Profile.objects.filter(id=id).first()
        data: dict = request.data
        if data.get("image"):
            img_src = self._process_image(data)
            q.image = img_src
            q.save()

        for key, value in data.items():
            setattr(q, key, value)

        q.save()
        return Response(status=status.HTTP_200_OK)
