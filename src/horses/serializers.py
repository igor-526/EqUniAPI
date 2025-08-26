from datetime import datetime

from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from gallery.models import Photo
from gallery.serializers import PhotoMainInfoSerializer

from profile_management.serializers import UserNameOnlySerializer

from rest_framework import serializers

from .models import Breed, Horse, HorseOwner
from .validators import validate_phone_numbers


class HorseOwnerNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = HorseOwner
        fields = ["id", "name"]


class HorseOwnerSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = HorseOwner
        fields = ["id", "name", "description", "type",
                  "address", "phone_number"]

    @staticmethod
    def get_phone_number(obj):
        return obj.phone_number

    def create(self, validated_data):
        phone_numbers = self.context.get("request").POST.getlist("phone_number[]")
        if phone_numbers:
            try:
                validate_phone_numbers(phone_numbers)
            except DjangoValidationError as ex:
                raise ValidationError({"phone_number": str(ex.message)})
        owner = HorseOwner.objects.create(**validated_data, phone_number=phone_numbers)
        return owner

    def update(self, instance: HorseOwner, validated_data):
        phone_numbers = self.context.get("request").POST.getlist("phone_number[]")
        if phone_numbers:
            try:
                validate_phone_numbers(phone_numbers)
                validated_data["phone_number"] = phone_numbers
            except DjangoValidationError as ex:
                raise ValidationError({"phone_number": str(ex.message)})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'description']


class BreedNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class HorseMainInfoSerializer(serializers.ModelSerializer):
    breed = BreedNameOnlySerializer()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex", "bdate_formatted",
                  "ddate_formatted", "description", "age", "photos"]

    def get_photos(self, obj):
        cache_key = f'horse_{obj.id}_photos'
        photos = cache.get(cache_key)
        if photos:
            return PhotoMainInfoSerializer(photos, many=True).data
        photos = getattr(obj, 'prefetched_photos', None)
        if photos is None:
            photos = obj.photos.all()
        cache.set(cache_key, photos, timeout=60 * 15)
        return PhotoMainInfoSerializer(photos, many=True).data


class HorseSerializer(serializers.ModelSerializer):
    breed = BreedNameOnlySerializer(read_only=True)
    photos = PhotoMainInfoSerializer(many=True, read_only=True)
    owner = HorseOwnerNameOnlySerializer(read_only=True)

    class Meta:
        model = Horse
        fields = ["id", "name", "breed", "sex",
                  "description", "age", "kind", "owner",
                  "bdate_formatted", "ddate_formatted", "photos"]

    def to_representation(self, instance: Horse):
        data = super().to_representation(instance)

        request = self.context.get('request')
        pedigree = None if request is None else request.query_params.get('pedigree', None)
        try:
            pedigree = int(pedigree)
            if pedigree < 1:
                pedigree = 1
            elif pedigree > 5:
                pedigree = 5
        except (TypeError, ValueError):
            pedigree = None

        if self.context.get('has_moderate_access', False):
            data['bdate'] = instance.bdate
            data['ddate'] = instance.ddate
            data['bdate_mode'] = instance.bdate_mode
            data['ddate_mode'] = instance.ddate_mode
            data['created_at'] = instance.created_at
            data['created_by'] = UserNameOnlySerializer(instance.created_by).data

        if pedigree:
            self.context.update({'pedigree': pedigree})
            data['pedigree'] = self.get_pedigree(instance)
            data['children'] = self.get_children(instance)

        return data

    def get_pedigree(self, obj: Horse):
        return obj.get_pedigree(self.context["pedigree"], HorseMainInfoSerializer)

    @staticmethod
    def get_children(obj: Horse):
        children = getattr(obj, 'prefetched_children', None)
        if children is None:
            children = obj.children.select_related('breed').prefetch_related('photos')

        return HorseMainInfoSerializer(children, many=True).data

    def create(self, validated_data):
        post_data = self.context.get("request").POST

        dates_data = {
            "bdate": post_data.get("bdate"),
            "bdate_mode": post_data.get("bdate_mode"),
            "ddate": post_data.get("ddate"),
            "ddate_mode": post_data.get("ddate_mode"),
        }

        if dates_data["bdate"]:
            try:
                dates_data["bdate"] = datetime.strptime(dates_data["bdate"], "%Y-%m-%d").date()
            except ValueError:
                dates_data["bdate"] = None
        if dates_data["ddate"]:
            try:
                dates_data["ddate"] = datetime.strptime(dates_data["ddate"], "%Y-%m-%d").date()
            except ValueError:
                dates_data["ddate"] = None

        horse = Horse.objects.create(
            **validated_data,
            **dates_data
        )

        breed = post_data.get("breed")
        photos = post_data.get("photos[]")
        owner = post_data.get("owner")

        if breed is not None:
            horse.set_breed(breed)
        if photos:
            photos = Photo.get_photos(
                request=self.context.get("request"),
                description=f'Фотография {horse.name}',
                categories=["Фотографии лошадей"]
            )
            horse.set_photos(photos)
        if owner is not None:
            try:
                owner_id = int(owner)
                owner = HorseOwner.objects.get(id=owner_id)
            except (TypeError, ValueError):
                owner = HorseOwner.objects.create(name=owner)
            except HorseOwner.DoesNotExist:
                owner = None
            horse.owner = owner
            horse.save()
        return horse
