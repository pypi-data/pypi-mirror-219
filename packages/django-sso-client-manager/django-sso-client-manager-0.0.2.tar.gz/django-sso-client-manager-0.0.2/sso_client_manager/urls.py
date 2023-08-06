from django.urls import path

from .views import login, logout, profile, SetCodeView

urlpatterns = [
    path('admin/login/', login, name='login'),
    path('admin/logout/', logout, name='logout'),
    path('profile/', profile),
    path('set-code/', SetCodeView.as_view(), name='set-code'),
]
