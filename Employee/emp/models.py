from django.db import models


# Create your models here.
class employees(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


    def __str__ (self):
        return self.firstname


from django.db import models

# Create your models here.
