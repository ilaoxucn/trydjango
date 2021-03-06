from django.contrib import admin
from .models import Recipe,RecipeIngredient
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    #fields = ['name','quantity','unit','description']
    extra = 0
    readonly_fields = ['quantity_as_float',]


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name','user']
    readonly_fields = ['timestamp','updated']
    raw_id_fields = ['user']
    inlines = [RecipeIngredientInline,]

class RecipeInline(admin.StackedInline):
    model = Recipe

class UserAdmin(admin.ModelAdmin):
    inlines = [RecipeInline]
    list_display = ['username']

admin.site.unregister(User)
admin.site.register(User,UserAdmin)



admin.site.register(Recipe,RecipeAdmin)