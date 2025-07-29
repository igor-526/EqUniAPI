from gallery.serializers import PhotoSerializer

from profile_management.serializers import UserNameOnlySerializer

from rest_framework import serializers

from .models import Breed, Horse


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class BreedNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class HorseMainInfoSerializer(serializers.ModelSerializer):
    breed = BreedNameOnlySerializer(many=False)
    age = serializers.SerializerMethodField()
    bdate_formatted = serializers.SerializerMethodField()
    ddate_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex", "bdate_formatted",
                  "ddate_formatted", "description", "age"]

    def get_age(self, obj: Horse):
        return obj.age

    def get_bdate_formatted(self, obj: Horse):
        return obj.bdate_formatted

    def get_ddate_formatted(self, obj: Horse):
        return obj.ddate_formatted


class HorseAdminSerializer(serializers.ModelSerializer):
    created_by = UserNameOnlySerializer(read_only=True)
    breed = BreedNameOnlySerializer(read_only=True)
    children = HorseMainInfoSerializer(many=True, read_only=True)
    mother = serializers.SerializerMethodField()
    father = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    bdate_formatted = serializers.SerializerMethodField()
    ddate_formatted = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex", "bdate",
                  "ddate", "description", "children",
                  "bdate_mode", "ddate_mode", "mother", "father",
                  "created_at", "created_by", "age",
                  "bdate_formatted", "ddate_formatted", "photos"]

    def get_age(self, obj: Horse):
        return obj.age

    def get_bdate_formatted(self, obj: Horse):
        return obj.bdate_formatted

    def get_ddate_formatted(self, obj: Horse):
        return obj.ddate_formatted

    def get_mother(self, obj: Horse):
        mother = obj.mother
        if mother is None:
            return None
        return HorseMainInfoSerializer(mother).data

    def get_father(self, obj: Horse):
        father = obj.father
        if father is None:
            return None
        return HorseMainInfoSerializer(father).data


class HorseSerializer(serializers.ModelSerializer):
    breed = BreedNameOnlySerializer(read_only=True)
    children = HorseMainInfoSerializer(many=True, read_only=True)
    mother = serializers.SerializerMethodField()
    father = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    bdate_formatted = serializers.SerializerMethodField()
    ddate_formatted = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex",
                  "description", "mother", "father", "children", "age",
                  "bdate_formatted", "ddate_formatted", "photos"]

    def get_age(self, obj: Horse):
        return obj.age

    def get_bdate_formatted(self, obj: Horse):
        return obj.bdate_formatted

    def get_ddate_formatted(self, obj: Horse):
        return obj.ddate_formatted

    def get_mother(self, obj: Horse):
        mother = obj.mother
        if mother is None:
            return None
        return HorseMainInfoSerializer(mother).data

    def get_father(self, obj: Horse):
        father = obj.father
        if father is None:
            return None
        return HorseMainInfoSerializer(father).data
