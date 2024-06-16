from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового поста в блоге.

    Это представление требует, чтобы пользователь был авторизован.
    Оно использует общее представление 'CreateView' для предоставления формы
    для создания новой записи в блоге.

    Атрибуты:
        model (Blog): Модель, с которой будет работать это представление.
        fields (tuple): Поля модели, которые будут включены в форму.
        success_url (str): URL для перенаправления после успешного создания.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Blog
    fields = ('title', 'description', 'image',)
    success_url = reverse_lazy('blog:blogs_list')
    login_url = 'users:login'


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления существующего поста в блоге.

    Это представление требует, чтобы пользователь был авторизован,
    и проверяет, является ли пользователь владельцем поста или администратором,
    прежде чем разрешить обновление.

    Атрибуты:
        model (Blog): Модель, с которой будет работать это представление.
        fields (tuple): Поля модели, которые будут включены в форму.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Blog
    fields = ('title', 'description', 'image',)
    login_url = 'users:login'

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления.
        """
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """
        Возвращает объект для обновления, проверяя права доступа пользователя.

        Если пользователь не является владельцем поста и не администратор,
        выдается ошибка 404.
        """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class BlogListView(ListView):
    """
    Представление для отображения списка постов в блоге.

    Атрибуты:
        model (Blog): Модель, с которой будет работать это представление.
    """
    model = Blog

    def get_queryset(self, *args, **kwargs):
        """
        Возвращает набор данных для отображения списка постов.

        Может быть переопределено для добавления дополнительных фильтров или сортировки.
        """
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class BlogDetailView(DetailView):
    """
    Представление для отображения деталей поста в блоге.

    Атрибуты:
        model (Blog): Модель, с которой будет работать это представление.
    """
    model = Blog

    def get_object(self, queryset=None):
        """
        Возвращает объект для отображения, увеличивая счетчик просмотров.

        Счетчик просмотров увеличивается каждый раз, когда пост отображается.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    """
    Представление для удаления поста в блоге.

    Атрибуты:
        model (Blog): Модель, с которой будет работать это представление.
        success_url (str): URL для перенаправления после успешного удаления.
        login_url (str): URL для перенаправления на страницу входа, если пользователь не авторизован.
    """
    model = Blog
    success_url = reverse_lazy('blog:blogs_list')
    login_url = 'users:login'

    def test_func(self):
        """
        Проверяет, имеет ли пользователь право на удаление поста.

        Только администраторы могут удалять посты.
        """
        return self.request.user.is_staff
