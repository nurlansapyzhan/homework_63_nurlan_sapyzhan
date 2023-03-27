from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView

from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm
from accounts.models import Account
from posts.models import Post


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        form = self.form()
        posts = Post.objects.all()
        context = {'form': form, 'posts': posts}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, "Некорректные данные")
            return redirect('index')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.warning(request, "Пользователь не найден")
            return redirect('index')
        login(request, user)
        messages.success(request, 'Добро пожаловать')
        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        return self.form_invalid(form)

    def form_valid(self, form, request):
        response = super().form_valid(form)
        user = form.save()
        login(request, user)
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return UserChangeForm(**form_kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class SubscribeView(View):
    def post(self, request, pk):
        user = get_object_or_404(Account, pk=pk)
        if user != request.user:
            if request.user in user.subscriptions.all():
                user.subscriptions.remove(request.user)
                request.user.subscribers.remove(user)
            else:
                user.subscriptions.add(request.user)
                request.user.subscribers.add(user)
        return redirect('index')
