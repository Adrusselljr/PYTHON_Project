from django.db import models
import re

class UserManager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name_length'] = "First name should be a minimum of 2 characters!"

        if len(post_data['last_name']) < 2:
            errors['last_name_length'] = "Last name should be a minimum of 2 characters!"

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_regex.match(post_data['email_address']):
            errors['email_address'] = "Invalid email address!"

        if len(post_data['password']) < 8:
            errors['password_length'] = "Password should be 8 characters or longer!"

        if post_data['password'] != post_data['confirm_password']:
            errors['password_match'] = "Please make sure 'Password' and 'Confirm Password' match!"

        try:
            User.objects.get(email_address = post_data['email_address'])
            errors['email_unique'] = "A user already exists with that email address!"
        except:
            pass

        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email_address = models.CharField(max_length = 255)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
