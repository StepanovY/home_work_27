import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category


class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        cat = self.object_list.order_by('name')

        response = []
        for category in cat:
            response.append(
                {
                    'id': category.id,
                    'name': category.name,
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse(
            {
                'id': category.pk,
                'name': category.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data['name'],
        )
        return JsonResponse(
            {
                'name': category.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data['name']

        self.object.save()

        return JsonResponse(
            {
                'name': self.object.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'}, status=200)
