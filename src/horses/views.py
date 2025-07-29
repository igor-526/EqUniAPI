from django.core.exceptions import ValidationError

from gallery.models import Photo

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Horse
from .permissions import HorsePedigreePermission, HorsePermission
from .serializers import (HorseAdminSerializer,
                          HorseMainInfoSerializer,
                          HorseSerializer)
from .validators import validate_child, validate_father, validate_mother


class HorseListCreateAPIView(ListCreateAPIView):
    model = Horse
    permission_classes = [HorsePermission]

    def get_serializer_class(self):
        if (self.request.user.is_authenticated and
                bool('horses.change_horse' in
                     self.request.user.get_group_permissions())):
            return HorseAdminSerializer
        return HorseSerializer

    def get_queryset(self):
        return Horse.get_queryset(self.request.query_params)

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
        if (self.request.user.is_authenticated and
                bool('horses.change_horse' in
                     self.request.user.get_group_permissions())):
            return HorseAdminSerializer
        return HorseSerializer

    def patch(self, request, *args, **kwargs):
        try:
            instance = Horse.objects.get(pk=kwargs['pk'])
        except Horse.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            horse = serializer.save()
            if request.data.get("breed") is not None:
                horse.set_breed(request.data.get("breed"))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HorsePedigreeAPIView(APIView):
    permission_classes = [HorsePedigreePermission]

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
