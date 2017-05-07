from django.conf.urls import url
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index),
    url(r'^document_list/$', views.document_list),
    url(r'^documents_per_user/(?P<pk_user>[0-9]+)/$', views.documents_per_user),
    url(r'^documents_per_category/(?P<category>[0-9a-zA-Z]+)/$', views.documents_per_category),
    url(r'^documents_with_errors_per_user/(?P<pk_user>[0-9]+)/$', views.documents_with_errors_per_user),
    url(r'^analyze/(?P<pk_user>[0-9]+)/(?P<doc_path>[.0-9a-zA-Z]+)/(?P<user_selected_document_type>[\s0-9a-zA-Z]+)'
        r'/(?P<document_name>[0-9a-zA-Z]+)/$', views.analyze),
    # url(r'^analyze/(?P<pk_user>[0-9]+)/(?P<doc_path>[.0-9a-zA-Z]+)/(?P<user_defined_doc_type>[\s0-9a-zA-Z]+)$',
    #         views.analyze),
]
# TODO: UPDATE REGEX IN DOCUMENTS_PER_CATEGORY TO INCLUDE SPECIAL CHARACTERS AND FILTER OUT HACKER ATTACKS
urlpatterns = format_suffix_patterns(urlpatterns)
