import pathlib
import uuid
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from .validators import validate_unit_of_measure
from .utils import number_str_to_float

class RecipeManager(models.Manager):
    def search(self,query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        lookups = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(directions__icontains=query)
        )
         
        return self.get_queryset().filter(lookups)


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField()
    directions = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = RecipeManager()

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:detail",kwargs={"id":self.id})
    
    def get_edit_url(self):
        return reverse("recipes:update",kwargs={"id":self.id})

    def get_delete_url(self):
        return reverse("recipes:delete",kwargs={"id":self.id})

    def get_hx_url(self):
        return reverse("recipes:hx-detail",kwargs={"id":self.id})

    def get_ingredient_children(self):
        return self.recipeingredient_set.all()

def recipe_ingredient_image_upload_handler(instance,filename):
    fpath = pathlib.Path(filename)
    new_name = uuid.uuid1()
    return f"recipes/{new_name}{fpath.suffix}"

class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=recipe_ingredient_image_upload_handler)

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

    @property
    def title(self):
        return self.name
        
    def save(self,*args,**kwargs):
        qty = self.quantity
        qty_as_float,success = number_str_to_float(qty)
        if success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float=None
        super().save(*args,**kwargs)

    def get_hx_edit_url(self):
        kwargs = {
            "id":self.recipe.id,
            "ingredient_id":self.id
        }
        return reverse("recipes:hx-ingredient-detail",kwargs=kwargs)

    def get_delete_url(self):
        kwargs = {
            "parent_id":self.recipe.id,
            "id":self.id
            }
        return reverse('recipes:ingredient-delete',kwargs=kwargs)

