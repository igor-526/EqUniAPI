from profile_management.serializers import UserNameOnlySerializer

from rest_framework import serializers

from .models import Photo, PhotoCategory


class PhotoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCategory
        fields = ["id", "name"]


class PhotoDetailSerializer(serializers.ModelSerializer):
    created_by = UserNameOnlySerializer()
    category = PhotoCategorySerializer(many=True)

    class Meta:
        model = Photo
        fields = ["title", "description", "image",
                  "category", "created_at", "created_by"]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image"]
