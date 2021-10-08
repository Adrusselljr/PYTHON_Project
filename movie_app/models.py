from django.db import models
from login_app.models import User
from datetime import datetime

class MovieManager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['movie_number']) <= 0:
            errors['movie_number'] = "Please provide a Movie ID Number!"

        if len(post_data['movie_title']) <= 0:
            errors['movie_title'] = "Please provide a Movie Title!"

        if len(post_data['movie_title']) > 100:
            errors['movie_title'] = "Movie Title is too long!"

        if len(post_data['movie_rating']) <= 0:
            errors['movie_rating'] = "Please provide a Movie Rating!  If unknown please input N/A."

        if len(post_data['movie_rating']) > 10:
            errors['movie_rating'] = "Movie Rating is too long!"

        if len(post_data['movie_genre']) <= 0:
            errors['movie_genre'] = "Please provide a Movie Genre!  If unknown please input N/A."

        if len(post_data['movie_genre']) > 100:
            errors['movie_genre'] = "Movie Genre is too long!"

        if len(post_data['movie_description']) <= 0:
            errors['movie_description'] = "Please provide a Movie Description!  If unknown please input N/A."

        if len(post_data['movie_description']) > 1000:
            errors['movie_description'] = "Movie Description is too long!"

        if len(post_data['movie_duration']) <= 0:
            errors['movie_duration'] = "Please provide a Movie Duration!  If unknown please input N/A."

        if len(post_data['movie_duration']) > 10:
            errors['movie_duration'] = "Movie Duration is too long!"

        if len(post_data['movie_leading_actor']) <= 0:
            errors['movie_leading_actor'] = "Please provide a Leading Actor / Actress name!  If unknown please input N/A."

        if len(post_data['movie_leading_actor']) > 100:
            errors['movie_leading_actor'] = "Leading Actor / Actress name is too long!"

        if len(post_data['movie_supporting_actor']) <= 0:
            errors['movie_supporting_actor'] = "Please provide a Supporting Actor / Actress name!  If unknown please input N/A."

        if len(post_data['movie_supporting_actor']) > 200:
            errors['movie_supporting_actor'] = "Supporting Actor / Actress name is too long!"

        if len(post_data['movie_director']) <= 0:
            errors['movie_director'] = "Please provide a Movie Director name!  If unknown please input N/A."

        if len(post_data['movie_director']) > 200:
            errors['movie_director'] = "Movie Director name is too long!"

        if len(post_data['movie_release_date']) != 10:
            errors['movie_release_date'] = "Please provide a valid date!"
        else:
            form_date = datetime.strptime(
                post_data['movie_release_date'], "%Y-%m-%d")

        return errors

class Movie(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length = 100)
    rating = models.CharField(max_length = 10)
    genre = models.CharField(max_length = 100)
    description = models.TextField(max_length = 1000)
    duration = models.CharField(max_length = 10)
    leading_actor = models.CharField(max_length = 100)
    supporting_actor = models.CharField(max_length = 200)
    director = models.CharField(max_length = 200)
    release_date = models.DateTimeField()
    admin = models.ForeignKey(
        User, related_name = "movies_created", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MovieManager()
