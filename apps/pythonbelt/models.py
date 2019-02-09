from __future__ import unicode_literals
from django.db import models
import re, bcrypt


class Validator(models.Manager):
    def registrator_validator(self, postData):
        errors = {}
        regex_email_valid = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        emailCheckTable = []
        for user in User.objects.all():
            emailCheckTable.append(user.email)
        
        if len(postData['first_name'])==False:
            errors['first_name_null'] = "'First Name' field is required"
        elif len(postData['first_name']) < 3:
            errors['first_name_len'] = 'Name must be 3 letters or more' 
        if len(postData['last_name'])==False:
            errors['last_name_null'] = "'Last Name' field is required"
        elif len(postData['last_name']) < 3:
            errors['last_name_len'] = 'Name must be 3 letters or more'
        elif postData['last_name'].isalpha() == False or postData['first_name'].isalpha() == False:
            errors['name_alpha'] = "'Name' fields can only contain letters"
        if len(postData['email'])==False:
            errors['email_null'] = "'Email' field is required"
        elif postData['email'] in emailCheckTable:
            errors['dup_email'] = "Email already in use"
        elif regex_email_valid.match(postData['email']) == None:
            errors['invalid_email'] = "Email format invalid"
        if len(postData['password'])==False:
            errors['password_null'] = "'Password' field is required"
        elif len(postData['password']) < 8:
            errors['password_len'] = "Choose a password at elast 8 characters in length"
        if 'password_confirm' not in postData:
            errors['password_confirm_null'] = "confirm password"
        elif postData['password'] != postData['password_confirm']:
            errors['password_confirm_mismatch'] = "'Password' and 'Confirm Password' must match"
        return errors
        
    def login_validator(self, postData):
        errors = {}
        if len(postData['loginEmail'])==False:
            errors['email_null'] = "'Email' field required"
        elif not User.objects.filter(email=postData['loginEmail']).exists():
                errors['Null_user'] = "Please register"

        elif len(postData['loginPassword'])==False:
            errors['password_null'] = "Please enter Password"
        elif not bcrypt.checkpw(postData['loginPassword'].encode(), User.objects.get(email=postData['loginEmail']).password.encode()):
            errors['bad_pw']="Incorrect Password"
        return errors
    
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoteText'])==False:
            errors['quoteText_null'] = "Type something"
        elif len(postData['quoteText']) < 10:
            errors['quoteText_short'] = "Type some more"
        if len(postData['quoteauthor'])==False:
            errors['author_null'] = "'Author' field must not be blank"
        elif len(postData['quoteauthor']) < 3:
            errors['author_short'] = "Author name must be at least 2 characters"
        return errors

    def updator_validator(self, postData):
        regex_email_valid = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        emailCheckTable = []
        for user in User.objects.all():
            emailCheckTable.append(user.email)
        errors ={}
        if len(postData['first_name'])==False:
            errors['first_name_null'] = "'First Name' field is required"
        elif len(postData['first_name']) < 3:
            errors['first_name_len'] = 'Name must be 3 letters or more' 
        if len(postData['last_name'])==False:
            errors['last_name_null'] = "'Last Name' field is required"
        elif len(postData['last_name']) < 3:
            errors['last_name_len'] = 'Name must be 3 letters or more'
        elif postData['last_name'].isalpha() == False or postData['first_name'].isalpha() == False:
            errors['name_alpha'] = "'Name' fields can only contain letters"
        if len(postData['email'])==False:
            errors['email_null'] = "'Email' field is required"
        elif postData['email'] in emailCheckTable:
            errors['dup_email'] = "Email already in use"
        elif regex_email_valid.match(postData['email']) == None:
            errors['invalid_email'] = "Email format invalid"
        if len(postData['password'])==False:
            errors['password_null'] = "'Password' field is required"
        elif len(postData['password']) < 8:
            errors['password_len'] = "Choose a password at elast 8 characters in length"
        if 'password_confirm' not in postData:
            errors['password_confirm_null'] = "confirm password"
        elif postData['password'] != postData['password_confirm']:
            errors['password_confirm_mismatch'] = "'Password' and 'Confirm Password' must match"
        return errors







class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Validator()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    text = models.TextField(default = "")
    likes = models.PositiveSmallIntegerField( default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    liked_by_user=models.ManyToManyField(User, related_name="liked_quotes")
    added_by_id=models.ForeignKey(User, related_name="quote_added", on_delete=models.CASCADE)
    liked_by_user=models.ManyToManyField(User, related_name="liked_quotes")
    objects = Validator()