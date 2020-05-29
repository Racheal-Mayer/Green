from django.db import models
import re
import bcrypt

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address!"
        if len(postData['fname']) < 2:
            errors["fname"] = "First Name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be atleast 8 characters."
        if (postData['password']) != (postData['confirm']):
            errors ["pasword"] = "Passwords do not match."
        return errors

    def validator(self, postData):
        errors = {}
        user = Register.objects.filter(email=postData['email'])
        if len(user) ==0:
            errors ['email'] = "Email not registered"
        else:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['password'] = "Password not correct"
        return errors

class Register(models.Model):
	fname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ShowManager()

class Post(models.Model):
    message = models.CharField(max_length=255)
    register = models.ForeignKey(Register, related_name="posts", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete = models.CASCADE)
    register = models.ForeignKey(Register, related_name="comments", on_delete = models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    item = models.CharField(max_length=255)
    itemprice = models.DecimalField(decimal_places=2, max_digits=10)
    uploader = models.ForeignKey(Register, related_name="quotes_uploaded", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)