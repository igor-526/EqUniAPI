from django.core.exceptions import ValidationError
from django.db.models import Count

from gallery.models import Photo

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Horse
from .permissions import HorsePermission, get_has_horses_moderate_permission
from .serializers import (HorseAdminSerializer,
                          HorseMainInfoSerializer,
                          HorseSerializer)
from .validators import validate_child, validate_father, validate_mother


class HorseListCreateAPIView(ListCreateAPIView):
    model = Horse
    permission_classes = [HorsePermission]

    def get_serializer_class(self, *args, **kwargs):
        has_moderate_access = kwargs.get("has_moderate_access", False)

        if has_moderate_access:
            return HorseAdminSerializer
        return HorseSerializer

    def get_queryset(self, *args, **kwargs):
        query_params = self.request.query_params

        name = query_params.get('name')
        sex = query_params.getlist('sex[]')
        bdate_year_start = query_params.get('bdate_year_start')
        bdate_year_end = query_params.get('bdate_year_end')
        ddate_year_start = query_params.get('ddate_year_start')
        ddate_year_end = query_params.get('ddate_year_end')
        breeds = query_params.getlist('breed[]')
        description = query_params.get('description')
        has_photo = query_params.get('has_photo')
        children_count = query_params.get('children_count')
        sort_params = query_params.getlist('sort[]')
        query_dict = dict()
        sort_list = list()

        if bdate_year_start:
            try:
                bdys = int(bdate_year_start)
                if bdys > 0:
                    query_dict['bdate__year__gte'] = bdys
            except ValueError:
                pass

        if bdate_year_end:
            try:
                bdye = int(bdate_year_end)
                if bdye > 0:
                    query_dict['bdate__year__lte'] = bdye
            except ValueError:
                pass

        if ddate_year_start:
            try:
                ddys = int(ddate_year_start)
                if ddys > 0:
                    query_dict['ddate__year__gte'] = ddys
            except ValueError:
                pass

        if ddate_year_end:
            try:
                ddye = int(ddate_year_end)
                if ddye > 0:
                    query_dict['bdate__year__lte'] = ddye
            except ValueError:
                pass

        if name is not None:
            query_dict['name__icontains'] = name

        if sex:
            query_dict['sex__in'] = sex

        if breeds:
            breeds_ids = []
            breeds_names = []
            for breed in breeds:
                try:
                    breeds_ids.append(int(breed))
                except ValueError:
                    breeds_names.append(breed)
            if breeds_ids:
                query_dict['breed__id__in'] = breeds_ids
            else:
                query_dict['breed__name__in'] = breeds_names

        if description:
            query_dict['description__icontains'] = description

        if has_photo == "true":
            query_dict['photos_c__gte'] = 1
        elif has_photo == "false":
            query_dict['photos_c'] = 0

        if children_count:
            try:
                cc = int(children_count)
                if cc == -1:
                    query_dict['children_c__gte'] = 1
                if cc >= 0:
                    query_dict['children_c'] = cc
            except ValueError:
                pass

        if sort_params:
            for param in sort_params:
                if param == "breed":
                    sort_list.append("breed__name")
                elif param == "-breed":
                    sort_list.append("-breed__name")
                elif param in ["name", "-name", "sex", "-sex",
                               "bdate", "-bdate", "ddate", "-ddate",
                               "created_at", "-created_at"]:
                    sort_list.append(param)

        return Horse.objects.annotate(
            children_c=Count("children"),
            photos_c=Count("photos")
        ).filter(**query_dict).order_by(
            *sort_list
        )

    def paginate_queryset(self, queryset):
        query_params = self.request.query_params
        qp_limit = query_params.get('limit')
        qp_offset = query_params.get('offset')

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

        return queryset[qp_offset:qp_limit + qp_offset]

    def list(self, request, *args, **kwargs):
        has_moderate_access = (
                request.user.is_authenticated and
                get_has_horses_moderate_permission(request.user)
        )
        serializer = self.get_serializer_class(
            has_moderate_access=has_moderate_access)
        queryset = self.get_queryset(has_moderate_access=has_moderate_access)
        count = queryset.count()
        queryset = self.paginate_queryset(queryset)

        serializer_data = serializer(queryset, many=True,
                                     context={"request": request}).data
        return Response(data={"count": count, "items": serializer_data},
                        status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horse = serializer.save()
        horse.created_by = request.user
        horse.save()
        try:
            if request.data.get("breed") is not None:
                horse.set_breed(request.data.get("breed"))
            if request.data.getlist("photo"):
                photos = Photo.get_photos(
                    request=request,
                    description=f'Фотография {horse.name}',
                    categories=["Фотографии лошадей"]
                )
                horse.set_photos(photos)
        except Exception as ex:
            horse.delete()
            return Response(data={"error": str(ex)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)


class HorseDetailAPIView(RetrieveUpdateDestroyAPIView):
    model = Horse
    permission_classes = [HorsePermission]

    def get_queryset(self):
        return Horse.objects.all()

    def get_serializer_class(self):
        has_moderate_access = (
                self.request.user.is_authenticated and
                get_has_horses_moderate_permission(self.request.user)
        )
        if has_moderate_access:
            return HorseAdminSerializer
        return HorseSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Horse.objects.get(pk=kwargs['pk'])
        except Horse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance,
                                         context={"request": request})
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            instance = Horse.objects.get(pk=kwargs['pk'])
        except Horse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(
            instance, data=request.data,
            partial=True, context={"request": request}
        )
        if serializer.is_valid():
            horse = serializer.save()
            if request.data.get("breed") is not None:
                horse.set_breed(request.data.get("breed"))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        mode = kwargs.get('mode')
        if mode not in ["mother", "father", "children"]:
            return Response(
                data={
                    "error": "Режим может быть только mother, father, children"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            horse = Horse.objects.get(pk=kwargs['pk'])
        except Horse.DoesNotExist:
            return Response(data={"error": "Лошадь не найдена"},
                            status=status.HTTP_404_NOT_FOUND)
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
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        mode = kwargs.get('mode')
        if mode not in ["mother", "father", "children"]:
            return Response(
                data={
                    "error": "Режим может быть только mother, father, children"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            horse = Horse.objects.get(pk=kwargs['pk'])
        except Horse.DoesNotExist:
            return Response(
                data={"error": "Лошадь не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            ped_horses = request.POST.getlist("ped_horses")
            if not ped_horses:
                return Response(
                    data={"error": "Отсутствуют лошади для родословной. "
                                   "Используйте ped_horses в запросе"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ped_horses = [Horse.objects.get(id=int(horse)) for
                          horse in ped_horses]
            if mode in ['mother', 'father'] and len(ped_horses) > 1:
                return Response(
                    data={"error": "Невозможно установить более 1 родителя"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                data={"error": "Используйте только id лошади в ped_horses"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Horse.DoesNotExist:
            return Response(
                data={"error": "Некоторые или все лошади для родословной "
                               "не были найдены"},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            if mode == "mother":
                validate_mother(horse, ped_horses[0])
                ped_horses[0].children.add(horse)
                ped_horses[0].save()
            if mode == "father":
                validate_father(horse, ped_horses[0])
                ped_horses[0].children.add(horse)
                ped_horses[0].save()
            if mode == 'children':
                for child in ped_horses:
                    validate_child(horse, child)
                horse.children.add(*ped_horses)
        except ValidationError as ex:
            return Response(data={"error": ex.message},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data=HorseAdminSerializer(instance=horse).data,
                        status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        mode = kwargs.get('mode')
        if mode not in ["mother", "father", "children"]:
            return Response(
                data={
                    "error": "Режим может быть только mother, father, children"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            horse = Horse.objects.get(pk=kwargs['pk'])
        except Horse.DoesNotExist:
            return Response(data={"error": "Лошадь не найдена"},
                            status=status.HTTP_404_NOT_FOUND)
        if mode == "mother":
            mother = horse.mother
            if mother is None:
                return Response(data={"error": "У лошади отсутствует мать"})
            mother.children.remove(horse)
            mother.save()
        elif mode == "father":
            father = horse.father
            if father is None:
                return Response(data={"error": "У лошади отсутствует отец"})
            father.children.remove(horse)
            father.save()
        elif mode == 'children':
            try:
                ped_horses = request.POST.getlist("ped_horses")
                if not ped_horses:
                    return Response(
                        data={"error": "Отсутствуют дети для удаления. "
                                       "Используйте ped_horses в запросе"},
                        status=status.HTTP_400_BAD_REQUEST)
                ped_horses = [
                    Horse.objects.get(id=int(horse)) for horse in ped_horses
                ]
            except ValueError:
                return Response(
                    data={
                        "error": "Используйте только id лошади в ped_horses"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Horse.DoesNotExist:
                return Response(
                    data={"error": "Некоторые или все лошади для удаления "
                                   "не были найдены"},
                    status=status.HTTP_404_NOT_FOUND
                )
            horse.children.remove(*ped_horses)
        return Response(data=HorseAdminSerializer(horse).data,
                        status=status.HTTP_200_OK)
