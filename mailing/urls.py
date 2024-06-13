from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (
    Homepage, ContactTemplateView, ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView,
    ClientDeleteView, MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView,
    NewsletterCreateView, NewsletterUpdateView, NewsletterListView, NewsletterDetailView, NewsletterDeleteView, LogsListView
)

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(Homepage.as_view()), name='home'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('view_client/<int:pk>', ClientDetailView.as_view(), name='view_client'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('message/create', MessageCreateView.as_view(), name='create_message'),
    path('message/list', MessageListView.as_view(), name='list_message'),
    path('message/view/<int:pk>', MessageDetailView.as_view(), name='view_message'),
    path('message/edit/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('newsletter/create', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('newsletter/edit/<int:pk>', NewsletterUpdateView.as_view(), name='edit_newsletter'),
    path('newsletter/list', NewsletterListView.as_view(), name='list_newsletter'),
    path('newsletter/view/<int:pk>', NewsletterDetailView.as_view(), name='view_newsletter'),
    path('newsletter/delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),

    path('logs/', LogsListView.as_view(), name='logs_list'),
]
