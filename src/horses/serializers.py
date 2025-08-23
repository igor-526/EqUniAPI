from gallery.serializers import PhotoMainInfoSerializer

from profile_management.serializers import UserNameOnlySerializer

from rest_framework import serializers

from .models import Breed, Horse


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'description']


class BreedNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class HorseMainInfoSerializer(serializers.ModelSerializer):
    breed = BreedNameOnlySerializer(many=False)
    photos = PhotoMainInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex", "bdate_formatted",
                  "ddate_formatted", "description", "age", "photos"]


class HorseAdminSerializer(serializers.ModelSerializer):
    created_by = UserNameOnlySerializer(read_only=True)
    breed = BreedNameOnlySerializer(read_only=True)
    children = serializers.SerializerMethodField()
    pedigree = serializers.SerializerMethodField()
    photos = PhotoMainInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex", "bdate",
                  "ddate", "description", "children", "pedigree",
                  "bdate_mode", "ddate_mode",
                  "created_at", "created_by", "age",
                  "bdate_formatted", "ddate_formatted", "photos"]

    def get_pedigree(self, obj: Horse):
        pedigree = self.context.get('request').query_params.get('pedigree',
                                                                None)
        if pedigree is None:
            return None
        try:
            pedigree = int(pedigree)
            if pedigree < 1:
                pedigree = 1
            elif pedigree > 5:
                pedigree = 5
        except (TypeError, ValueError):
            return None
        return obj.get_pedigree(pedigree, HorseMainInfoSerializer)

    def get_children(self, obj: Horse):
        pedigree = self.context.get('request').query_params.get('pedigree',
                                                                None)
        if pedigree is None:
            return None
        try:
            pedigree = int(pedigree)
        except (TypeError, ValueError):
            return None
        if not pedigree:
            return None
        return HorseMainInfoSerializer(obj.children.all(), many=True).data


class HorseSerializer(serializers.ModelSerializer):
    breed = BreedNameOnlySerializer(read_only=True)
    children = serializers.SerializerMethodField()
    pedigree = serializers.SerializerMethodField()
    photos = PhotoMainInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex",
                  "description", "pedigree", "children", "age",
                  "bdate_formatted", "ddate_formatted", "photos"]

    def get_pedigree(self, obj: Horse):
        pedigree = self.context.get('request').query_params.get('pedigree',
                                                                None)
        if pedigree is None:
            return None
        try:
            pedigree = int(pedigree)
            if pedigree < 1:
                pedigree = 1
            elif pedigree > 5:
                pedigree = 5
        except (TypeError, ValueError):
            return None
        return obj.get_pedigree(pedigree, HorseMainInfoSerializer)

    def get_children(self, obj: Horse):
        pedigree = self.context.get('request').query_params.get('pedigree',
                                                                None)
        if pedigree is None:
            return None
        try:
            pedigree = int(pedigree)
        except (TypeError, ValueError):
            return None
        if not pedigree:
            return None
        return HorseMainInfoSerializer(obj.children.all(), many=True).data
