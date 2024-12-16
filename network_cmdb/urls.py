from django.urls import path
from network_cmdb import views

urlpatterns = [
        path('index/', views.index, name='cmdb_index'),
]
