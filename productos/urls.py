from django.urls import path
from . import  views


urlpatterns=[
    path('',views.main_page_view,name='main_page'),
    path('product/<int:product_id>/', views.product_router_view, name='product')

]


