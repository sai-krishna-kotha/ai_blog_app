from django.urls import path
from blog_generator import views


urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('generate-blog/',views.generate_blog,name='generate-blog'),
    path('blog-list/',views.blog_list,name="blog-list"),
    path('blog-details/<int:pk>/',views.blog_details,name="blog-details")
]
