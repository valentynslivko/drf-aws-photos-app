from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from image_app.models import Profile, User
from image_app.serializers import ProfileSerializer, UserSerializer
from image_app.http import invoke_image_processing
from image_app.utils import download_image
import logging

logging.basicConfig(style="{")
logger = logging.getLogger(__name__)


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
        if invoke_result["status"] >= 400:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data="Processing failed on Lambda side",
            )

        if invoke_result["status"] == 200:
            return invoke_result["body"]

        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data="Unknown error during Lambda processing",
        )

    def partial_update(self, request, id: int):
        q = Profile.objects.filter(id=id).first()
        data: dict = request.data

        for key, value in data.items():
            setattr(q, key, value)

        if data.get("image"):
            processing_response = self._process_image(data)
            if isinstance(
                processing_response, dict
            ):  # if dict is returned, workflow is successful, TODO: rework with pydantic
                q.image = processing_response["image"]

        q.save()
        q.refresh_from_db()
        serialized_data = ProfileSerializer(q).data
        return Response(status=status.HTTP_200_OK, data=serialized_data)
