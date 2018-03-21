# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
from datetime import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManage(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["First name field can be left blank"]="first_name"

        if len(postData['last_name']) < 2:
            errors["Last name cannot be left blank"]="last_name"

        if len(postData['email']) < 1:
            errors["Email cannot be left blank"]="email"

        elif not EMAIL_REGEX.match(postData['email']):
            errors["this is not a valid email try again"]="email"

        if (User.objects.filter(email=postData['email'])):
            errors['Email already in use']="email"
        print postData["email"]

        
        if len(postData['password']) < 8:
            errors["Passwords must at least 8 characters"]="password"

        if postData["password"] != postData["cpassword"]:
            errors["Passwords do not match"]="cpassword"
        return errors

    def loginvalidate(self, postData):
        errors = {}
        if len(postData['email'])<1:
            errors["Email field can not be blank"] = "email"

        if len(postData["password"])<8:
            errors["Password must be at least 8 characters" ] = "password"

        if len(self.filter(email=postData['email']))>0:
            #print 'TRUE for emails'
            currentuser =self.filter(email=postData['email'])[0]
            existingpwd = currentuser.password
        
            if not bcrypt.checkpw(postData["password"].encode(), existingpwd.encode()):
                    errors["Password does not match"] = "password"
        else:
            errors["Email does not match"] = "email" 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    birthdate = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManage()