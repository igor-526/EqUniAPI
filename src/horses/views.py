from django.core.exceptions import ValidationError
from django.db.models import Count, Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Breed, Horse, HorseOwner
from .permissions import HorsePermission, get_has_horses_moderate_permission
from .serializers import (
    BreedNameOnlySerializer,
    BreedSerializer,
    HorseMainInfoSerializer,
    HorseOwnerNameOnlySerializer,
    HorseOwnerSerializer,
    HorseSerializer,
)
from .validators import validate_child, validate_dame, validate_sire


@extend_schema(tags=["Лошади"])
class HorseListCreateAPIView(ListCreateAPIView):
    model = Horse
    permission_classes = [HorsePermission]
    serializer_class = HorseSerializer

    def build_query_dict(self, *args, **kwargs):
        query_params = self.request.query_params

        name = query_params.get("name")
        sex = query_params.getlist("sex[]")
        bdate_year_start = query_params.get("bdate_year_start")
        bdate_year_end = query_params.get("bdate_year_end")
        ddate_year_start = query_params.get("ddate_year_start")
        ddate_year_end = query_params.get("ddate_year_end")
        breeds = query_params.getlist("breed[]")
        description = query_params.get("description")
        has_photo = query_params.get("has_photo")
        children_count = query_params.get("children_count")
        kind = query_params.getlist("kind[]")
        has_owner = query_params.get("has_owner")
        owner = query_params.get("owner[]")

        query_dict = dict()

        if bdate_year_start:
            try:
                bdys = int(bdate_year_start)
                if bdys > 0:
                    query_dict["bdate__year__gte"] = bdys
            except ValueError:
                pass

        if bdate_year_end:
            try:
                bdye = int(bdate_year_end)
                if bdye > 0:
                    query_dict["bdate__year__lte"] = bdye
            except ValueError:
                pass

        if ddate_year_start:
            try:
                ddys = int(ddate_year_start)
                if ddys > 0:
                    query_dict["ddate__year__gte"] = ddys
            except ValueError:
                pass

        if ddate_year_end:
            try:
                ddye = int(ddate_year_end)
                if ddye > 0:
                    query_dict["bdate__year__lte"] = ddye
            except ValueError:
                pass

        if name is not None:
            query_dict["name__icontains"] = name

        if sex:
            query_dict["sex__in"] = sex

        if kind:
            query_dict["kind__in"] = kind

        if breeds:
            breeds_ids = []
            breeds_names = []
            for breed in breeds:
                try:
                    breeds_ids.append(int(breed))
                except ValueError:
                    breeds_names.append(breed)
            if breeds_ids:
                query_dict["breed__id__in"] = breeds_ids
            else:
                query_dict["breed__name__in"] = breeds_names

        if description:
            query_dict["description__icontains"] = description

        if has_photo == "true":
            query_dict["photos_c__gte"] = 1
        elif has_photo == "false":
            query_dict["photos_c"] = 0

        if children_count:
            try:
                cc = int(children_count)
                if cc == -1:
                    query_dict["children_c__gte"] = 1
                if cc >= 0:
                    query_dict["children_c"] = cc
            except ValueError:
                pass

        if has_owner == "true":
            query_dict["owner__isnull"] = False
        elif has_owner == "false":
            query_dict["owner__isnull"] = True

        if owner:
            query_dict["owner__id__in"] = owner

        return query_dict

    def get_sort_list(self, *args, **kwargs):
        query_params = self.request.query_params

        sort_params = query_params.getlist("sort[]")
        sort_list = list()
        if sort_params:
            for param in sort_params:
                if param == "breed":
                    sort_list.append("breed__name")
                elif param == "-breed":
                    sort_list.append("-breed__name")
                elif param in [
                    "name",
                    "-name",
                    "sex",
                    "-sex",
                    "bdate",
                    "-bdate",
                    "ddate",
                    "-ddate",
                    "created_at",
                    "-created_at",
                    "kind",
                    "-kind",
                ]:
                    sort_list.append(param)
        return sort_list

    def get_queryset(self, *args, **kwargs):
        prefetch_query = ["photos"]

        if self.request.query_params.get("pedigree"):
            prefetch_children = Prefetch(
                lookup="children",
                queryset=Horse.objects.select_related("breed").prefetch_related(
                    "photos"
                ),
                to_attr="prefetched_children",
            )

            prefetch_parents = Prefetch(
                lookup="parents",
                queryset=Horse.objects.select_related("breed").prefetch_related(
                    "photos"
                ),
                to_attr="prefetched_parents",
            )

            prefetch_query.append(prefetch_children)
            prefetch_query.append(prefetch_parents)

        queryset = (
            Horse.objects.annotate(
                children_count=Count("children", distinct=True),
                photos_count=Count("photos", distinct=True),
            )
            .select_related("breed", "owner")
            .prefetch_related(*prefetch_query)
        )

        return queryset.filter(**self.build_query_dict()).order_by(
            *self.get_sort_list()
        )

    def paginate_queryset(self, queryset):
        query_params = self.request.query_params
        qp_limit = query_params.get("limit")
        qp_offset = query_params.get("offset")

        try:
            qp_limit = int(qp_limit)
            if qp_limit < 1:
                qp_limit = 1
            elif qp_limit > 100:
                qp_limit = 100
        except (ValueError, TypeError):
            qp_limit = 50

        try:
            qp_offset = int(qp_offset)
            if qp_offset < 0:
                qp_offset = 0
        except (ValueError, TypeError):
            qp_offset = 0

        return queryset[qp_offset : qp_limit + qp_offset]

    def list(self, request, *args, **kwargs):
        has_moderate_access = (
            request.user.is_authenticated
            and get_has_horses_moderate_permission(request.user)
        )
        queryset = self.get_queryset(has_moderate_access=has_moderate_access)
        count = queryset.count()
        queryset = self.paginate_queryset(queryset)

        serializer_data = self.serializer_class(
            queryset,
            many=True,
            context={"request": request, "has_moderate_access": has_moderate_access},
        ).data
        return Response(
            data={"count": count, "items": serializer_data}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Лошади"])
class HorseDetailAPIView(RetrieveUpdateDestroyAPIView):
    model = Horse
    permission_classes = [HorsePermission]
    serializer_class = HorseSerializer

    def get_queryset(self):
        return Horse.objects.all()

    @extend_schema(tags=["Лошади"], summary="Получение одной лошади")
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Horse.objects.get(pk=kwargs["pk"])
        except Horse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        has_moderate_access = (
            request.user.is_authenticated
            and get_has_horses_moderate_permission(request.user)
        )
        serializer = self.serializer_class(
            instance,
            context={"request": request, "has_moderate_access": has_moderate_access},
        )
        return Response(serializer.data)

    @extend_schema(tags=["Лошади"], summary="Изменение лошади")
    def patch(self, request, *args, **kwargs):
        try:
            instance = Horse.objects.get(pk=kwargs["pk"])
        except Horse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True,
            context={"request": request, "has_moderate_access": True},
        )
        if serializer.is_valid():
            horse = serializer.save()
            if request.data.get("breed") is not None:
                horse.set_breed(request.data.get("breed"))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Лошади"])
class HorsePedigreeAPIView(APIView):
    permission_classes = [HorsePermission]

    def get_parents_queryset(self, horse: Horse, parent: str = "M"):
        query_dict = dict()
        if parent == "M":
            query_dict["sex"] = 0
        else:
            query_dict["sex__in"] = [1, 2]

        if horse.bdate:
            query_dict["bdate__year__lte"] = horse.bdate.year

        return Horse.objects.filter(**query_dict).exclude(id=horse.pk)

    def get_children_queryset(self, horse: Horse):
        query_dict = dict()
        if horse.bdate:
            query_dict["bdate__year__gte"] = horse.bdate.year
        if horse.ddate:
            query_dict["bdate__year__lte"] = horse.ddate.year

        return Horse.objects.filter(**query_dict).exclude(id=horse.pk)

    def get(self, request, *args, **kwargs):
        mode = kwargs.get("mode")
        if mode not in ["mother", "father", "children"]:
            return Response(
                data={"error": "Режим может быть только mother, father, children"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            horse = Horse.objects.get(pk=kwargs["pk"])
        except Horse.DoesNotExist:
            return Response(
                data={"error": "Лошадь не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        if mode == "mother":
            queryset = self.get_parents_queryset(horse, "M")
        elif mode == "father":
            queryset = self.get_parents_queryset(horse, "F")
        elif mode == "children":
            queryset = self.get_children_queryset(horse)
        else:
            queryset = None
        return Response(
            data=HorseMainInfoSerializer(instance=queryset, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        mode = kwargs.get("mode")
        if mode not in ["sire", "dame", "children"]:
            return Response(
                data={"error": "Режим может быть только sire, dame, children"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            horse = Horse.objects.get(pk=kwargs["pk"])
        except Horse.DoesNotExist:
            return Response(
                data={"error": "Лошадь не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            ped_horses = request.POST.getlist("ped_horses")
            if not ped_horses:
                return Response(
                    data={
                        "error": "Отсутствуют лошади для родословной. "
                        "Используйте ped_horses в запросе"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ped_horses = [Horse.objects.get(id=int(horse)) for horse in ped_horses]
            if mode in ["sire", "dame"] and len(ped_horses) > 1:
                return Response(
                    data={"error": "Невозможно установить более 1 родителя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                data={"error": "Используйте только id лошади в ped_horses"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Horse.DoesNotExist:
            return Response(
                data={
                    "error": "Некоторые или все лошади для родословной "
                    "не были найдены"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            if mode == "sire":
                validate_sire(horse, ped_horses[0])
                ped_horses[0].children.add(horse)
                ped_horses[0].save()
            if mode == "dame":
                validate_dame(horse, ped_horses[0])
                ped_horses[0].children.add(horse)
                ped_horses[0].save()
            if mode == "children":
                for child in ped_horses:
                    validate_child(horse, child)
                horse.children.add(*ped_horses)
        except ValidationError as ex:
            return Response(
                data={"error": ex.message}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=HorseSerializer(
                instance=horse,
                context={"request": self.request, "has_moderate_access": True},
            ).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        mode = kwargs.get("mode")
        if mode not in ["sire", "dame", "children"]:
            return Response(
                data={"error": "Режим может быть только sire, dame, children"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            horse = Horse.objects.get(pk=kwargs["pk"])
        except Horse.DoesNotExist:
            return Response(
                data={"error": "Лошадь не найдена"}, status=status.HTTP_404_NOT_FOUND
            )
        if mode == "sire":
            sire = horse.get_sire()
            if sire is None:
                return Response(
                    data={"error": "У лошади отсутствует мать"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            sire.children.remove(horse)
            sire.save()
        elif mode == "dame":
            dame = horse.get_dame()
            if dame is None:
                return Response(
                    data={"error": "У лошади отсутствует отец"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            dame.children.remove(horse)
            dame.save()
        elif mode == "children":
            try:
                ped_horses = request.POST.getlist("ped_horses")
                if not ped_horses:
                    return Response(
                        data={
                            "error": "Отсутствуют дети для удаления. "
                            "Используйте ped_horses в запросе"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                ped_horses = [Horse.objects.get(id=int(horse)) for horse in ped_horses]
            except ValueError:
                return Response(
                    data={"error": "Используйте только id лошади в ped_horses"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Horse.DoesNotExist:
                return Response(
                    data={
                        "error": "Некоторые или все лошади для удаления "
                        "не были найдены"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            horse.children.remove(*ped_horses)
        return Response(
            data=HorseSerializer(
                horse, context={"request": self.request, "has_moderate_access": True}
            ).data,
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Лошади"])
class HorsePhotosAPIView(APIView):
    pass


@extend_schema(tags=["Породы лошадей"])
class BreedListCreateAPIView(ListCreateAPIView):
    model = Horse
    permission_classes = [HorsePermission]

    def get_serializer_class(self):
        if (
            self.request.query_params.get("full") == "true"
            or self.request.method == "POST"
        ):
            return BreedSerializer
        return BreedNameOnlySerializer

    def build_query_dict(self, *args, **kwargs):
        query_params = self.request.query_params

        name = query_params.get("name")
        description = query_params.get("description")

        query_dict = dict()

        if name is not None:
            query_dict["name__icontains"] = name

        if description:
            query_dict["description__icontains"] = description

        return query_dict

    def get_sort_list(self, *args, **kwargs):
        query_params = self.request.query_params

        sort_params = query_params.getlist("sort[]")
        sort_list = list()
        if sort_params:
            for param in sort_params:
                if param in ["name", "-name"]:
                    sort_list.append(param)
        return sort_list

    def get_queryset(self):
        queryset = Breed.objects.filter(**self.build_query_dict()).order_by(
            *self.get_sort_list()
        )
        return queryset

    def paginate_queryset(self, queryset):
        query_params = self.request.query_params
        qp_limit = query_params.get("limit")
        qp_offset = query_params.get("offset")

        try:
            qp_limit = int(qp_limit)
            if qp_limit < 1:
                qp_limit = 1
            elif qp_limit > 1000:
                qp_limit = 1000
        except (ValueError, TypeError):
            qp_limit = 200

        try:
            qp_offset = int(qp_offset)
            if qp_offset < 0:
                qp_offset = 0
        except (ValueError, TypeError):
            qp_offset = 0

        return queryset[qp_offset : qp_limit + qp_offset]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer_class()

        serializer_data = serializer(queryset, many=True).data
        return Response(
            data={"count": count, "items": serializer_data}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Породы лошадей"])
class BreedDetailAPIView(RetrieveUpdateDestroyAPIView):
    model = Horse
    permission_classes = [HorsePermission]
    serializer_class = BreedSerializer

    def get_queryset(self):
        return Breed.objects.all()


@extend_schema(tags=["Владельцы лошадей"])
class HorseOwnersListCreateAPIView(ListCreateAPIView):
    permission_classes = [HorsePermission]
    serializer_class = HorseOwnerSerializer

    def get_serializer_class(self):
        if (
            self.request.query_params.get("full") == "true"
            or self.request.method == "POST"
        ):
            return HorseOwnerSerializer
        return HorseOwnerNameOnlySerializer

    def build_query_dict(self, *args, **kwargs):
        query_params = self.request.query_params

        search_name = query_params.get("name")
        search_description = query_params.get("description")
        filter_type = query_params.getlist("type[]")
        search_address = query_params.get("address")

        query_dict = dict()

        if search_name is not None:
            query_dict["name__icontains"] = search_name

        if search_description:
            query_dict["description__icontains"] = search_description

        if filter_type:
            query_dict["type__in"] = filter_type

        if search_address:
            query_dict["address__icontains"] = search_address

        return query_dict

    def get_sort_list(self, *args, **kwargs):
        query_params = self.request.query_params

        sort_params = query_params.getlist("sort[]")
        sort_list = list()
        if sort_params:
            for param in sort_params:
                if param in ["name", "-name", "address", "-address"]:
                    sort_list.append(param)
        return sort_list

    def get_queryset(self):
        queryset = HorseOwner.objects.filter(**self.build_query_dict()).order_by(
            *self.get_sort_list()
        )
        return queryset

    def paginate_queryset(self, queryset):
        query_params = self.request.query_params
        qp_limit = query_params.get("limit")
        qp_offset = query_params.get("offset")

        try:
            qp_limit = int(qp_limit)
            if qp_limit < 1:
                qp_limit = 1
            elif qp_limit > 1000:
                qp_limit = 1000
        except (ValueError, TypeError):
            qp_limit = 200

        try:
            qp_offset = int(qp_offset)
            if qp_offset < 0:
                qp_offset = 0
        except (ValueError, TypeError):
            qp_offset = 0

        return queryset[qp_offset : qp_limit + qp_offset]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer_class()

        serializer_data = serializer(queryset, many=True).data
        return Response(
            data={"count": count, "items": serializer_data}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Владельцы лошадей"])
class HorseOwnersDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [HorsePermission]
    serializer_class = HorseOwnerSerializer

    def get_queryset(self):
        return HorseOwner.objects.all()
