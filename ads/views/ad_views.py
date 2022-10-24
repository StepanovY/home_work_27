import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category
from users.models import User


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ads = self.object_list.all()

        response = []
        for ad in ads:
            response.append(
                {
                    'id': ad.id,
                    'name': ad.name,
                    'author': ad.author.first_name,
                    'price': ad.price,
                    'description': ad.description,
                    'image': ad.image.url if ad.image else None,
                    'category': ad.category.name,
                }
            )
        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse(
            {
                'id': ad.pk,
                'name': ad.name,
                'author_id': ad.author.first_name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url if ad.image else None,
                'category_id': ad.category.name,

            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'images', 'category']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = get_object_or_404(User, first_name=ad_data['author'])
        category = get_object_or_404(Category, name=ad_data['category'])

        ad = Ad.objects.create(
            name=ad_data['name'],
            author=author,
            price=ad_data['price'],
            description=ad_data['description'],
            category=category,
        )
        return JsonResponse(
            {
                'name': ad.name,
                'author': ad.author.first_name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'category': ad.category.name

            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'image', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)

        ad_data = json.loads(request.body)

        if 'name' in ad_data:
            self.object.name = ad_data['name']

        if 'price' in ad_data:
            self.object.price = ad_data['price']

        if 'description' in ad_data:
            self.object.description = ad_data['description']

        self.object.save()

        return JsonResponse(
            {
                'name': self.object.name,
                'author': self.object.author.first_name,
                'price': self.object.price,
                'description': self.object.description,
                'category': self.object.category.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'}, status=204)
