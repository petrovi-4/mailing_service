from blog.models import Blog
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail


def homepage_cache():
    """
    Функция кеширования случайных статей блога для главной страницы.

    Если кэширование включено в настройках проекта (settings.CACHE_ENABLED),
    функция пытается получить случайные статьи из кэша. Если статьи отсутствуют
    в кэше, функция извлекает случайные статьи из базы данных, сохраняет их
    в кэше и возвращает их.

    Returns:
        QuerySet: Список случайных статей блога.
    """
    if settings.CACHE_ENABLED:
        key = 'random_article'
        random_article = cache.get(key)
        if random_article is None:
            random_article = Blog.objects.order_by('?')[:3]
            cache.set(key, random_article)
        else:
            random_article = Blog.objects.order_by('?')[:3]

        return random_article


def send_newpassword(email, new_password):
    """
    Функция для отправки нового пароля на указанный email.

    Args:
        email (str): Email адрес получателя.
        new_password (str): Новый сгенерированный пароль.

    Отправляет email с уведомлением о смене пароля и новым паролем,
    используя функцию send_mail Django.
    """
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
