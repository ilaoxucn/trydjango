from django.db import models
from django.conf import settings
from django.urls import reverse
from .validators import validate_unit_of_measure
from .utils import number_str_to_float

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField()
    directions = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("recipes:detail",kwargs={"id":self.id})
    
    def get_edit_url(self):
        return reverse("recipes:update",kwargs={"id":self.id})

    def get_ingredient_children(self):
        return self.recipeingredient_set.all()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True,null=True)
    unit = models.CharField(max_length=50,validators=[validate_unit_of_measure,])

    def save(self,*args,**kwargs):
        qty = self.quantity
        qty_as_float,success = number_str_to_float(qty)
        if success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float=None
        super().save(*args,**kwargs)

