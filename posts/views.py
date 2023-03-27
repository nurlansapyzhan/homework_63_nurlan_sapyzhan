from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views.generic import CreateView, ListView

from accounts.models import Account
from posts.forms import SearchForm
from posts.models import Post

User = get_user_model()


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            self.form = self.get_search_form()
            self.search_value = self.get_search_value()
            return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(username__icontains=self.search_value) | Q(email__icontains=self.search_value) | Q(
                first_name__icontains=self.search_value) | Q(last_name__icontains=self.search_value)
            user = User.objects.filter(query).first()
            if user:
                queryset = queryset.filter(author=user)
            else:
                queryset = queryset.none()
        else:
            subscriptions = self.request.user.subscriptions.all()
            queryset = queryset.filter(author__in=subscriptions) | queryset.filter(author=self.request.user)
        return queryset.order_by('-created_at')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class AddPostView(CreateView):
    model = Post
    fields = ['description', 'image']
    template_name = 'add_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
