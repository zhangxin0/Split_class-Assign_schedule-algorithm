from django.contrib import admin
from django.urls import path, include
import algorithmapp.views as av

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schedule_course', views.schedule_course),
    path('moc/assign_course', views.moc_assign_course),
    path('moc/assign_class', views.moc_split_class),
    path('split_class', views.split_class),
]