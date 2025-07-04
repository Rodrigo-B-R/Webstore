from django.urls import path
from . import  views


urlpatterns= [
    
    path('login/',views.login_view, name= 'login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name= "signup"),
    path('profile/', views.profile_view, name='profile'),
    path('shipping/' , views.shippingAddress_view, name='shipping'),
    path('shipping/edit/<int:id>', views.edit_adress_view,name='edit_address'),
    path('shipping/delete/<int:id>',views.delete_address_view,name='delete_address')
    


]


