import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad
from home_work_27.settings import TOTAL_ON_PAGE
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('username')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        users = paginator.get_page(page)
        response = {}
        items_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.location.all())),
            'total_ads': user.ads.filter(is_published=True).count()
        } for user in users]
        response['items'] = items_list
        response['total'] = self.object_list.count()
        response['nam_pages'] = paginator.num_pages
        response['page'] = page

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse(
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'role': user.role,
                'age': user.age,
                'locations': list(map(str, user.location.all())),
                'total_ads': user.ads.filter(is_published=True).count()
            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
        )

        if 'locations' in user_data:
            for loc_data in user_data['locations']:
                loc, _ = Location.objects.get_or_create(name=loc_data)
                user.location.add(loc)

        return JsonResponse(
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'role': user.role,
                'age': user.age,
                'locations': list(map(str, user.location.all())),
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'role', 'age', 'location']

    def patch(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)

        user_data = json.loads(request.body)

        if 'first_name' in user_data:
            self.object.first_name = user_data['first_name']

        if 'last_name' in user_data:
            self.object.last_name = user_data['last_name']

        if 'username' in user_data:
            self.object.username = user_data['username']

        if 'role' in user_data:
            self.object.role = user_data['role']

        if 'age' in user_data:
            self.object.age = user_data['age']

        if 'locations' in user_data:
            for loc_data in user_data['locations']:
                loc, _ = Location.objects.get_or_create(name=loc_data)
                self.object.location.add(loc)

        self.object.save()

        return JsonResponse(
            {
                'id': self.object.id,
                'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'username': self.object.username,
                'role': self.object.role,
                'age': self.object.age,
                'locations': list(map(str, self.object.location.all())),
                'total_ads': self.object.ads.filter(is_published=True).count()
            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'}, status=204)