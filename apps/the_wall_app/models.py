from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

# Create your models here.

# This class handles all of the validation for our forms on submit
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        #validate length of first name field
        if len(postData['input_first_name']) < 2:
            errors["input_first_name"] = "First name should be at least 2 letters"
        #validate first name field doesn't contain numbers
        if postData['input_first_name'].isalpha() == False:
            errors["input_first_name"] = "First name cannot contain numbers"
        #validate length of last name field
        if len(postData['input_last_name']) < 2:
            errors["input_last_name"] = "Last name should be at least 2 letters"
        #validate last name field doesn't contain numbers
        if postData['input_last_name'].isalpha() == False:
            errors["input_last_name"] = "Last name cannot contain numbers"
        # query the list of all emails to verify the desired address is not registered yet
        query = User.objects.all().values('email')
        for row in query:
            for key in row:
                if row[key] == postData['input_email']:
                    errors["input_email"] = "Email is taken"
        # validate that the email supplied by the user is of a valid format
        try:
            validate_email(postData["input_email"])
        except ValidationError:
            errors['input_email'] = "Enter a valid email"

        if len(postData['input_password']) < 8:
            errors["input_password"] = "Password should be at least 8 characters"
        if postData['input_confirm_password'] != postData["input_password"]:
            errors["input_confirm_password"] = "Passwords must match"
        return errors

# This is our table
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {}>".format(self.first_name, self.last_name, self.email)

class Message(models.Model):
    message = models.CharField(max_length=255)
    messages_user = models.ForeignKey(User, related_name="users_messages")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<Message object: {} {}>".format(self.message, self.messages_user)

class Comment(models.Model):
    comment = models.CharField(max_length = 255)
    comments_message = models.ForeignKey(Message, related_name="messages_comment")
    comments_user = models.ForeignKey(User, related_name="users_comment")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<Comment object: {} {} {}>".format(self.comment, self.comments_message, self.comments_user)