from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('addGift', views.addGift),
    path('share', views.share),
    # path('add/<idItem>', views.add2list),
    # path('remove/<idItem>', views.removeItem),
    # path('itemInfo/<idItem>', views.itemInfo),
    path('delete/<idGift>', views.delete)
]
