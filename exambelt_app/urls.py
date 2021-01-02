from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('create_trip', views.create_trip),
    path('new_trip', views.new_trip),
    path('edit/<int:id>', views.edit_trip),
    path('remove/<int:id>', views.remove),
    path('trips/<int:id>', views.show_trip),
    path('join/<int:id>', views.join_trip),
    path('cancel/<int:id>', views.cancel_trip)
]