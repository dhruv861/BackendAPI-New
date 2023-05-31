from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None,password2=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password=None ):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
           name= name,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    bodyPart = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    gifUrl = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    subscription_choices = [
        ("Free", "Free"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum")
    ]
    gender_choices = [("M","Male"),("F","Female"),("O","Others")]
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(choices=gender_choices, max_length=50)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    subscription = models.CharField(choices=subscription_choices, max_length=100)
    address = models.TextField()
    City = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    favourites= models.ManyToManyField(Exercise)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name"]

    # session_token = models.CharField(max_length=10, default=0)

    active = models.BooleanField(default=True)
    # a admin user; non super-user
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # a superuser

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Favourite(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.PROTECT,unique=True)
    exercise=models.ManyToManyField(Exercise)

    def __str__(self):
        return self.user.email

class Gym(models.Model):
    Name = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Address = models.TextField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class RecentlySelectedExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class ExercisePlan(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.PROTECT,unique=True)
    plan = models.TextField()
# for ex in data:
#     Exercises.objects.create(name=ex["name"], bodyPart=ex["bodyPart"], target=ex["target"], equipment=ex["equipment"],
#                              gifUrl=ex["gifUrl"])
