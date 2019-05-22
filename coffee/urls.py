from django.urls import path, include
import coffee.views

urlpatterns = [
    path('content', coffee.views.article_content),
    path('index', coffee.views.get_index_page),
    path('detail/<int:article_id>', coffee.views.get_detail_page),
    path('products_display', coffee.views.products_display),
    path('barista', coffee.views.barista_page),
    path('register', coffee.views.register),
    path('active/(?P<token>.*)', coffee.views.active),
    path('login', coffee.views.login),
    path('staff', coffee.views.get_staff),
    path('completeorder', coffee.views.completeorder),
    path('removeorder', coffee.views.removeorder),
]