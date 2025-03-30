from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crawler/',include('crawler.urls')),
    path('drop_rate/',include('drop_rate.urls')),
]
