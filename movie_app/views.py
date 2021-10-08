from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from login_app.models import User
from .models import Movie

def movies(request):
    if not 'user_id' in request.session:
        messages.error(request, "Log in to view this page!")
    context = {
        "movies": Movie.objects.all(),
        "user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, "movies.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add_movie(request):
    return render(request, "add_movie.html")

def create_movie(request):
    user = User.objects.get(id=request.session['user_id'])
    movie = Movie.objects.get(id=movie_id)
    if user != movie.admin:
        messages.error(request, "Must be the Admin to delete this movie!")
        return redirect('/movies')

    errors = Movie.objects.basic_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/movies/add')

    Movie.objects.create(
        number = request.POST['movie_number'],
        title = request.POST['movie_title'],
        rating = request.POST['movie_rating'],
        genre = request.POST['movie_genre'],
        description = request.POST['movie_description'],
        leading_actor = request.POST['movie_leading_actor'],
        supporting_actor = request.POST['movie_supporting_actor'],
        duration = request.POST['movie_duration'],
        release_date = request.POST['movie_release_date'],
        director = request.POST['movie_director'],
        admin = User.objects.get(id = request.session['user_id'])
    )
    return redirect('/movies')

def confirm_delete(request, movie_id):
    user = User.objects.get(id = request.session['user_id'])
    movie = Movie.objects.get(id = movie_id)
    if user != movie.admin:
        messages.error(request, "Must be the Admin to delete this movie!")
        return redirect('/movies')

    context = {
        'movie': movie
    }
    return render(request, "confirm_delete.html", context)

def delete_movie(request, movie_id):
    user = User.objects.get(id = request.session['user_id'])
    movie = Movie.objects.get(id = movie_id)
    if user != movie.admin:
        messages.error(request, "Must be the Admin to delete this movie!")
        return redirect('/movies')

    movie = Movie.objects.get(id = movie_id).delete()
    messages.info(request, "You deleted the movie!")
    return redirect('/movies')

def movie_info(request, movie_id):
    user = User.objects.get(id = request.session['user_id'])
    movie = Movie.objects.get(id = movie_id)
    if user != movie.admin:
        messages.error(request, "Must be the Admin to delete this movie!")
        return redirect('/movies')

    context = {
        'movie': Movie.objects.get(id = movie_id),
        'user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, "movie_info.html", context)

def edit_movie(request, movie_id):
    user = User.objects.get(id = request.session['user_id'])
    movie = Movie.objects.get(id = movie_id)
    if user != movie.admin:
        messages.error(request, "Must be the Admin to edit this information!")
        return redirect('/movies')

    context = {
        'movie': movie
    }
    return render(request, "edit_movie.html", context)


def update_movie(request, movie_id):
    user = User.objects.get(id = request.session['user_id'])
    movie = Movie.objects.get(id = movie_id)
    if user != movie.admin:
        messages.error(request, "Must be the Admin to edit this information!")
        return redirect('/movies')

    errors = Movie.objects.basic_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/movies/{movie_id}/edit')

    movie.number = request.POST['movie_number']
    movie.title = request.POST['movie_title']
    movie.rating = request.POST['movie_rating']
    movie.genre = request.POST['movie_genre']
    movie.description = request.POST['movie_description']
    movie.leading_actor = request.POST['movie_leading_actor']
    movie.supporting_actor = request.POST['movie_supporting_actor']
    movie.duration = request.POST['movie_duration']
    movie.release_date = request.POST['movie_release_date']
    movie.director = request.POST['movie_director']
    movie.admin = User.objects.get(id = request.session['user_id'])
    movie.save()
    return redirect(f'/movies/{movie.id}')

def search_movie(request):
    return render(request, "search_movie.html")

def search_bar(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        if request.GET['title_search'] != '':
            movies = movies.filter(title__contains = request.GET['title_search'])
        if request.GET['rating_search'] != '':
            movies = movies.filter(rating = request.GET['rating_search'])
        if request.GET['genre_search'] != '':
            movies = movies.filter(genre__contains = request.GET['genre_search'])
        actor = request.GET['actor_search']
        if request.GET['actor_search'] != '':
            movies = Movie.objects.filter(leading_actor__icontains = actor) | Movie.objects.filter(supporting_actor__icontains = actor)
        if request.GET['director_search'] != '':
            movies = movies.filter(director__contains = request.GET['director_search'])
        return render(request, "search_results.html", {'post': movies})