from django.urls import path,include
from .import views

urlpatterns = [

    path('login',views.loginpage,name='loginpage'),
    path('page3',views.page3,name='page3'),
    path('',views.home,name='home'),
    path('register',views.signuppage,name='signuppage'),
    path('add_details',views.add_details,name='add_details'),
    path('log',views.log,name='log'),
    path('adminmod',views.adminmod,name='adminmod'),
    path('usermod/<int:id>',views.usermod,name='usermod'),
    path('lgout',views.lgout,name='lgout'),
    path('add_category', views.add_category, name='add_category'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('add_product', views.add_product, name='add_product'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('list_products', views.list_products, name='list_products'),
    path('edit_product/<int:product_id>', views.edit_product, name='edit_product'),
    path('editproduct/<int:product_id>', views.editproduct, name='editproduct'),
    path('deleteproduct/<int:product_id>', views.deleteproduct, name='deleteproduct'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('edituser/<int:id>', views.edituser, name='edituser'),
    path('list_users',views.list_users, name='list_users'),
    path('delete_user/<int:user_id>/',views.delete_user, name='delete_user'),
    path('category/<int:category_id>', views.category, name='category'),
    path('page2', views.page2, name='page2'),
    # path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    # path('cart', views.cart_view, name='cart'),
    # path('update-cart-quantity', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart', views.cart, name='cart'),
    path('increase_quantity/<int:id>', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>', views.decrease_quantity, name='decrease_quantity'),
    path('cart_details/<int:id>', views.cart_details, name='cart_details'),
    path('remove_cart/<int:id>', views.remove_cart, name='remove_cart'),



]