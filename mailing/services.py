from blog.models import Blog
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail


def homepage_cache():
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
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
