from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class CustomeUser(AbstractUser):
    TYPE_CHOICES = (
        ("HEAD", "head"),
        ("MEMBER", "member")

    )
    user_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=1
    )
    is_head = models.BooleanField(default=False)


class family(models.Model):
    name = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name="rel_user")


class Material(models.Model):
    material_name = models.CharField(max_length=40,
                                     null=False,
                                     blank=False,
                                     unique=True)
    is_service = models.BooleanField(default=False)
    user_id =  models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name="material_user")


    description = models.CharField(max_length=50,
                                   null=False,
                                   blank=False) 

    

    def __str__(self):
        return self.material_name


class outlayType(models.Model):
    outlay_name = models.CharField(max_length=50,
                                   null=False,
                                   blank=False)
    outlay_description = models.CharField(max_length=100,
                                          null=False,
                                          blank=False) 
    user_id =  models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name="outlaytype_user")

    def __str__(self):
        return self.outlay_name


class outlay(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="rel_material")
    outlay_type = models.ForeignKey(outlayType, on_delete=models.CASCADE, related_name="rel_outlay")
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name="outlay_user")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=100,
                                   null=False,
                                   blank=False)
   
