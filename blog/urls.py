from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='psot_list'),
    path('<int:id>/',views.post_detail,name="post_detail")
]