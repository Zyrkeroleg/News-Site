from django.urls import path
from .views import *


urlpatterns = [
    path("register/", register, name='register'),
    path('login/', login, name='login'),
    path("", HomeNews.as_view(), name='home'),
    path("category/<int:category_id>", News_by_category.as_view(), name='category'),
    path('news/<int:pk>', ViewNews.as_view(), name='view_news'),
    path('news/add_news', CreateNews.as_view(), name='add_news')
]
