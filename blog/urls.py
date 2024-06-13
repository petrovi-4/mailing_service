from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogUpdateView, BlogDetailView, BlogDeleteView, BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('blogs_list', cache_page(60)(BlogListView.as_view()), name='blogs_list'),
    path('create_blog', BlogCreateView.as_view(), name='create_blog'),
    path('edit/<int:pk>', BlogUpdateView.as_view(), name='edit'),
    path('view/<int:pk>', BlogDetailView.as_view(), name='view'),
    path('delete/<int:pk>', BlogDeleteView.as_view(), name='delete'),
]
