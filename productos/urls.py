from django.urls import path
from . import  views


urlpatterns=[
    path('',views.main_page_view,name='main_page'),
    path('product/<int:id>/',views.product_view,name='product')
]


