from django.urls import path
from . import views

urlpatterns = [
    path('movies', views.movies),
    path('users/logout', views.logout),
    path('movies/add', views.add_movie),
    path('movies/create', views.create_movie),
    path('movies/<int:movie_id>/confirm', views.confirm_delete),
    path('movies/<int:movie_id>/delete', views.delete_movie),
    path('movies/<int:movie_id>', views.movie_info),
    path('movies/<int:movie_id>/edit', views.edit_movie),
    path('movies/<int:movie_id>/update', views.update_movie),
    path('movies/search', views.search_movie),
    path('movies/search_bar', views.search_bar, name = "search_bar"),
    path('movies/<int:result_id>', views.movie_info)
]
