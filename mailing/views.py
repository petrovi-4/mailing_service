from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from mailing.services import homepage_cache

from mailing.models import Client, Message, Newsletter, Contact, Logs
from mailing.forms import ClientForm, MessageForm, NewsletterForm


class Homepage(TemplateView):
    """
    Представление для главной страницы.

    Отображает базовый шаблон 'mailing/base.html' с дополнительным контекстом:
    - title: Заголовок страницы ('Mailing')
    - filtred_list: Результат кеширования случайных статей блога, полученный с помощью homepage_cache
    """
    template_name = 'mailing/base.html'
    extra_context = {'title': 'Mailing', 'filttred_list': homepage_cache}


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового клиента.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'CreateView' для формы создания нового клиента.

    Атрибуты:
        model (Client): Модель клиента, с которой работает представление.
        form_class (ClientForm): Класс формы для создания клиента.
        success_url (str): URL для перенаправления после успешного создания клиента.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'users:login'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления информации о клиенте.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'UpdateView' для формы обновления информации о клиенте.

    Атрибуты:
        model (Client): Модель клиента, с которой работает представление.
        fields (tuple): Поля модели, которые будут доступны для обновления.
        success_url (str): URL для перенаправления после успешного обновления информации о клиенте.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Client
    fields = ('fio', 'email', 'comment',)
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'users:login'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class ClientListView(LoginRequiredMixin, ListView):
    """
    Представление для списка клиентов.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'ListView' для отображения списка клиентов.

    Атрибуты:
        model (Client): Модель клиента, с которой работает представление.
        success_url (str): URL для перенаправления после успешной операции.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'users:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['clients_list'] = Client.objects.all()
        return context_data


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детальной информации о клиенте.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'DetailView' для отображения детальной информации о клиенте.

    Атрибуты:
        model (Client): Модель клиента, с которой работает представление.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Client
    login_url = 'users:login'


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления клиента.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'DeleteView' для удаления клиента.

    Атрибуты:
        model (Client): Модель клиента, с которой работает представление.
        success_url (str): URL для перенаправления после успешного удаления клиента.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    login_url = 'users:login'


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового сообщения.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'CreateView' для формы создания нового сообщения.

    Атрибуты:
        model (Message): Модель сообщения, с которой работает представление.
        form_class (MessageForm): Класс формы для создания сообщения.
        success_url (str): URL для перенаправления после успешного создания сообщения.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:list_message')
    login_url = 'users:login'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления сообщения.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'UpdateView' для формы обновления сообщения.

    Атрибуты:
        model (Message): Модель сообщения, с которой работает представление.
        form_class (MessageForm): Класс формы для обновления сообщения.
        success_url (str): URL для перенаправления после успешного обновления сообщения.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:list_message')
    login_url = 'users:login'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MessageListView(LoginRequiredMixin, ListView):
    """
    Представление для списка сообщений.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'ListView' для отображения списка сообщений.

    Атрибуты:
        model (Message): Модель сообщения, с которой работает представление.
        success_url (str): URL для перенаправления после успешной операции.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Message
    success_url = reverse_lazy('mailing:list_message')
    login_url = 'users:login'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['messages_list'] = Message.objects.all()
        return context_data


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детальной информации о сообщении.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'DetailView' для отображения детальной информации о сообщении.

    Атрибуты:
        model (Message): Модель сообщения, с которой работает представление.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Message


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления сообщения.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'DeleteView' для удаления сообщения.

    Атрибуты:
        model (Message): Модель сообщения, с которой работает представление.
        success_url (str): URL для перенаправления после успешного удаления сообщения.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Message
    success_url = reverse_lazy('mailing:list_message')
    login_url = 'users:login'


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового информационного бюллетеня.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'CreateView' для формы создания нового информационного бюллетеня.

    Атрибуты:
        model (Newsletter): Модель информационного бюллетеня, с которой работает представление.
        form_class (NewsletterForm): Класс формы для создания информационного бюллетеня.
        success_url (str): URL для перенаправления после успешного создания информационного бюллетеня.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mailing:list_newsletter')
    login_url = 'users:login'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления информационного бюллетеня.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'UpdateView' для формы обновления информационного бюллетеня.

    Атрибуты:
        model (Newsletter): Модель информационного бюллетеня, с которой работает представление.
        fields (tuple): Поля модели, доступные для обновления.
        success_url (str): URL для перенаправления после успешного обновления информационного бюллетеня.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Newsletter
    fields = ('start_time', 'end_time', 'periodicity', 'status', 'client', 'message')
    success_url = reverse_lazy('mailing:list_newsletter')
    login_url = 'users:login'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class NewsletterListView(LoginRequiredMixin, ListView):
    """
    Представление для списка информационных бюллетеней.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'ListView' для отображения списка информационных бюллетеней.

    Атрибуты:
        model (Newsletter): Модель информационного бюллетеня, с которой работает представление.
        success_url (str): URL для перенаправления после успешной операции.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Newsletter
    success_url = reverse_lazy('mailing:list_newsletter')
    login_url = 'users:login'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['newsletters_list'] = Newsletter.objects.all()
        unique_clients = Client.objects.all().count()
        context_data['clients'] = unique_clients
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class NewsletterDetailView(DetailView):
    """
    Представление для детальной информации об информационном бюллетене.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'DetailView' для отображения детальной информации об информационном бюллетене.

    Атрибуты:
        model (Newsletter): Модель информационного бюллетеня, с которой работает представление.
    """
    model = Newsletter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления информационного бюллетеня.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'DeleteView' для удаления информационного бюллетеня.

    Атрибуты:
        model (Newsletter): Модель информационного бюллетеня, с которой работает представление.
        success_url (str): URL для перенаправления после успешного удаления информационного бюллетеня.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Newsletter
    success_url = reverse_lazy('mailing:list_newsletter')
    login_url = 'users:login'


class ContactTemplateView(TemplateView):
    """
    Представление для страницы контактов.

    Использует общее представление 'TemplateView' для отображения шаблона 'mailing/contacts.html'.
    Добавляет дополнительный контекст с информацией о контактах.

    Атрибуты:
        template_name (str): Имя шаблона для отображения ('mailing/contacts.html').
    """
    template_name = 'mailing/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        contact_info = Contact.objects.all()
        context_data['contact_book'] = contact_info
        return context_data

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, номер телефона: {phone}, сообщение: {message}')
        return render(request, self.template_name)


class LogsListView(LoginRequiredMixin, ListView):
    """
    Представление для списка логов.

    Требует, чтобы пользователь был авторизован для доступа.
    Использует общее представление 'ListView' для отображения списка логов.

    Атрибуты:
        model (Logs): Модель логов, с которой работает представление.
        success_url (str): URL для перенаправления после успешной операции.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Logs
    success_url = reverse_lazy('mailing:logs_list')
    login_url = 'users:login'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['total'] = Logs.objects.all()
        context_data['total_count'] = Logs.objects.all().count()
        context_data['successful_count'] = Logs.objects.filter(attempt=True).count()
        context_data['unsuccessful_count'] = Logs.objects.filter(attempt=False).count()
        return context_data
