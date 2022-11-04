from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ads.models import Ad
from ads.permissions import AdUpdatePermission
from ads.serializers import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.order_by('-price')
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category = request.GET.getlist('cat_id', [])

        if category:
            self.queryset = self.queryset.filter(category_id__in=category)

        text = request.GET.get('text')

        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        price_from = request.GET.get('price_from')  # от

        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')  # до

        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        location = request.GET.get('location')

        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        return super().list(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [AdUpdatePermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [AdUpdatePermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image')
        self.object.save()

        return JsonResponse(
            {
                'id': self.object.pk,
                'name': self.object.name,
                'image': self.object.image.url if self.object.image else None,

            }, safe=False
        )
