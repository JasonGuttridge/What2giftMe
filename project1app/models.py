from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        if len(postData['firstName']) < 2:
            errors['firstName'] = 'Name should be more than 2 characters'
        if len(postData['lastName']) < 2:
            errors['lastName'] = 'Name should be more than 2 characters'
        if User.objects.filter(userName=postData['userName']).exists():
            errors['userName'] = 'Username already exists'
        elif len(postData['userName']) < 2:
            errors['userName'] = 'Username should be at least 2 characters'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = 'Email already exists'
        elif not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        if postData['confirm'] != postData['password']:
            errors['confirm'] = 'Password is not confirmed'
        return errors

    def loginValidator(self, postData):
        errors = {}
        user = User.objects.filter(userName=postData['userName'])
        if len(postData['userName']) == 0:
            errors['userName'] = 'Username is required'
        elif len(user) == 0:
            errors['userName'] = 'Username not found'
        else:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                print('Password matches')
            else:
                errors['passwordfailed'] = "Incorrect Password. Please try again."
        return errors

# class ItemManager(models.Manager):
#     def itemValidator(self, postData):
#         errors = {}
#         if len(postData['item']) == 0:
#             errors['item'] = 'Item cannot be empty'
#         elif len(postData['item']) < 2:
#             errors['item'] = 'Item name should be more than 2 characters'
#         return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    # birthday = birthday.fields.BirthdayField()
    userName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Gift(models.Model):
    gift = models.TextField()
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, related_name='giftUploaded', on_delete = models.CASCADE)
#     favorites = models.ManyToManyField(User, related_name='itemsFavorited')
    
    # objects = ItemManager()