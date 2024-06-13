from django.db import models

from config.settings import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=15, verbose_name='заголовок')
    description = models.TextField(verbose_name='Содержимое статьи', **NULLABLE)
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    published_date = models.DateTimeField(verbose_name='дата публикации', auto_now_add=True)

    def __str__(self):
        return f'Название блога: {self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
