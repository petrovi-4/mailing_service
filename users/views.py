import secrets
from random import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from users.forms import UserRegisterForm, UserProfileForm

from mailing.services import send_newpassword
from users.models import User


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Позволяет создать нового пользователя с отправкой письма для подтверждения регистрации.

    Атрибуты:
        model (User): Модель пользователя для создания нового пользователя.
        form_class (UserRegisterForm): Класс формы для регистрации пользователя.
        template_name (str): Имя шаблона для формы регистрации.
        success_url (str): URL для перенаправления после успешной регистрации.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Обработка валидности формы для регистрации пользователя.

        Генерирует токен регистрации, устанавливает пользователя как неактивного,
        отправляет электронное письмо со ссылкой для подтверждения.
        """
        new_user = form.save()
        new_user.is_active = False
        token = secrets.token_hex(8)
        new_user.toke = token
        new_user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/confirm/{token}'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Перейдите по ссылке для подтверждения регистрации {url}!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Подтверждение адреса электронной почты для пользователя.

    Устанавливает пользователя как активного на основе предоставленного токена.
    Перенаправляет на страницу входа после подтверждения.
    """
    new_user = get_object_or_404(User, token=token)
    new_user.is_active = True
    new_user.save()
    return redirect(reverse_lazy('users:login'))


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Представление для обновления профиля пользователя.

    Требует, чтобы пользователь был авторизован и имел необходимые права доступа.
    Использует общее представление 'UpdateView' для обновления профиля пользователя.

    Атрибуты:
        model (User): Модель пользователя, с которой работает представление.
        form_class (UserProfileForm): Класс формы для обновления профиля пользователя.
        success_url (str): URL для перенаправления после успешного обновления.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
        permission_required (str): Необходимое разрешение для доступа к представлению.
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user_list')
    login_url = 'users:login'
    permission_required = 'users.change_user'

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    """
    Генерация и отправка нового пароля пользователю.

    Генерирует новый случайный пароль, устанавливает его для текущего пользователя
    и отправляет на зарегистрированный адрес электронной почты.
    Перенаправляет на главную страницу после успешной операции.
    """
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    request.user.set_password(new_password)
    request.user.save()
    send_newpassword(request.user.email, new_password)
    return redirect(reverse('mailing:home'))


class UserListView(PermissionRequiredMixin, ListView):
    """
    Представление для списка пользователей.

    Требует, чтобы пользователь имел необходимое разрешение для доступа.
    Использует общее представление 'ListView' для отображения списка пользователей.

    Атрибуты:
        model (User): Модель пользователя, с которой работает представление.
        permission_required (str): Необходимое разрешение для доступа к представлению.
    """
    model = User
    permission_required = 'users.view_user'

    def get_context_data(self, *args, **kwargs):
        """
        Получение контекста данных для представления.

        Добавляет в контекст список всех пользователей.
        """
        context_data = super().get_context_data(*args, **kwargs)
        context_data['users_list'] = User.objects.all()
        return context_data


class UserDetailView(PermissionRequiredMixin, DetailView):
    """
    Представление для детальной информации о пользователе.

    Требует, чтобы пользователь имел необходимое разрешение для доступа.
    Использует общее представление 'DetailView' для отображения детальной информации о пользователе.

    Атрибуты:
        model (User): Модель пользователя, с которой работает представление.
        permission_required (str): Необходимое разрешение для доступа к представлению.
    """
    model = User
    permission_required = 'users.view_user'


class UserDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления пользователя.

    Требует, чтобы пользователь прошел проверку теста (is_staff) и имел необходимое разрешение.
    Использует общее представление 'DeleteView' для удаления пользователя.

    Атрибуты:
        model (User): Модель пользователя, с которой работает представление.
        permission_required (str): Необходимое разрешение для доступа к представлению.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
        success_url (str): URL для перенаправления после успешного удаления пользователя.
    """
    model = User
    permission_required = 'users.delete_user'
    login_url = 'users:login'
    success_url = reverse_lazy('users:user_list')

    def test_func(self):
        return self.request.user.is_staff
