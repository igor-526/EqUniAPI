from gallery.models import Photo, PhotoCategory

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response

from .permissions import GalleryPermission, get_has_gallery_moderate_permission
from .serializers import PhotoListAdminSerializer, PhotoListSerializer


class PhotoListCreateAPIView(ListCreateAPIView):
    model = Photo
    permission_classes = [GalleryPermission]

    def get_serializer_class(self, *args, **kwargs):
        has_moderate_access = kwargs.get('has_moderate_access', False)
        if has_moderate_access:
            return PhotoListAdminSerializer
        return PhotoListSerializer

    def filter_queryset(self, queryset, *args, **kwargs):
        query_params = self.request.query_params
        has_moderate_access = kwargs.get('has_moderate_access', False)

        search_title = query_params.get('title')
        search_description = query_params.get('description')
        search_category = query_params.getlist('category_id[]')

        filter_query = dict()

        if search_title:
            filter_query['title__icontains'] = search_title
        if search_description:
            filter_query['description__icontains'] = search_description
        if search_category:
            queryset = queryset.filter(category__id__in=search_category)

        if has_moderate_access:
            search_created_at_start = query_params.get(
                'search_created_at_start')
            search_created_at_end = query_params.get('search_created_at_end')
            filter_created_by = query_params.getlist('created_by_id[]')

            if search_created_at_start:
                filter_query['created_at__gte'] = search_created_at_start
            if search_created_at_end:
                filter_query['created_at__lte'] = search_created_at_end
            if filter_created_by:
                filter_query['created_by__id'] = filter_created_by

        queryset = queryset.filter(**filter_query)
        return queryset

    def paginate_queryset(self, queryset, *args, **kwargs):
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

        return queryset[qp_offset:qp_limit+qp_offset]

    def get_queryset(self, *args, **kwargs):
        return Photo.objects.all()

    def list(self, request, *args, **kwargs):
        has_moderate_access = (
                request.user.is_authenticated and
                get_has_gallery_moderate_permission(request.user)
        )
        serializer = self.get_serializer_class(
            has_moderate_access=has_moderate_access)
        queryset = self.get_queryset(has_moderate_access=has_moderate_access)
        count = queryset.count()
        queryset = self.paginate_queryset(queryset)
        serializer_data = serializer(queryset, many=True).data
        return Response(data={"count": count, "items": serializer_data},
                        status=status.HTTP_200_OK)


class PhotoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    model = Photo
    permission_classes = [GalleryPermission]

    def get_queryset(self):
        return Photo.objects.all()

    def get_object(self):
        return Photo.objects.get(pk=self.kwargs['pk'])


class PhotoCategoryListCreateAPIView(ListCreateAPIView):
    model = PhotoCategory
    permission_classes = [GalleryPermission]

    def get_queryset(self):
        return PhotoCategory.objects.all()


class PhotoCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    model = PhotoCategory
    permission_classes = [GalleryPermission]

    def get_queryset(self):
        return PhotoCategory.objects.all()
