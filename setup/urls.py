from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from imoveis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('imovel/<int:pk>/', views.detalhe_imovel, name='detalhe_imovel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
