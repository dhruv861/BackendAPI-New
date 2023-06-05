from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    # subscription = models.CharField(choices=subscription_choices, max_length=100)
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


class RecentlySelectedExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserPlan(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.PROTECT,unique=True)
    exercise_plan = models.TextField()
    meal_plan = models.TextField()
# for ex in data:
#     Exercises.objects.create(name=ex["name"], bodyPart=ex["bodyPart"], target=ex["target"], equipment=ex["equipment"],
#                              gifUrl=ex["gifUrl"])
class Queries(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100,default="Anonymous")
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    message = models.TextField()
