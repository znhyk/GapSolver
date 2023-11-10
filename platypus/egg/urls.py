"""egg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('backplate',views.backplate, name='backplate'),
    path('testbank', views.testbank, name='testbank'),
    path('scanner', views.scanner, name='scanner'),
    path('book_info', views.book_info, name='book_info'),
    path('justsolve_1', views.justsolve_1, name='justsolve_1'),
    path('justsolve_2', views.justsolve_2, name='justsolve_2'),
    path('justsolve_3', views.justsolve_3, name='justsolve_3'),
    path('testbank_detail', views.testbank_detail, name='testbank_detail'),#testbank_detail/?pk=
    path('create_testbank', views.create_testbank, name='create_testbank'),
    path('justsolve', views.justsolve, name='justsolve'),
    path('api', views.api, name='api'),
    path('api2', views.api2, name='api2'),
    path('api_get_db', views.api_get_db, name='api_get_db'),
    path('api_update_db', views.api_update_db, name='api_update_db'),
    path('api_make_testbank', views.api_make_testbank, name='make_test_bank'),
    path('api_make_test', views.api_make_test, name='api_make_test'),
    path('api_end_test', views.api_end_test, name='api_end_test'),
    path('api_search_testbank_by_genre', views.api_search_testbank_by_genre, name='api_search_testbank_by_genre'),
    path('api_search_testbank_by_ISBN', views.api_search_testbank_by_ISBN, name='api_search_testbank_by_ISBN'),
    path('api_barcode_reader', views.api_barcode_reader, name='barcode'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)