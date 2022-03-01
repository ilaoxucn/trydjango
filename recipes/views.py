from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from .models import Recipe,RecipeIngredient
from .forms import RecipeForm,RecipeIngredientForm
# CRUD Create Retrieve Update Delete
# LIST

@login_required
def recipe_detail_view(request,id=None):
    obj = get_object_or_404(Recipe,id=id,user=request.user)
    context = {
        'object':obj
    }
    return render(request,"recipes/detail.html",context)

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list':qs
    }
    return render(request,"recipes/list.html",context)

@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request,"recipes/create-update.html",context)

@login_required
def recipe_update_view(request,id=None):
    obj = get_object_or_404(Recipe,id=id,user=request.user)
    form = RecipeForm(request.POST or None,instance=obj)
    #Formset = modelformset_factory(Model,ModelForm,extra = 0)
    if request.method=='POST':
        print(request.POST)
    RecipeIngredientFormset = modelformset_factory(
        RecipeIngredient,
        form=RecipeIngredientForm,
        extra=0)
    qs = obj.get_ingredient_children()
    formset = RecipeIngredientFormset(request.POST or None,queryset=qs)
    context = {
        "form":form,
        "formset":formset,
        "object":obj 
    }
    if all([form.is_valid(),formset.is_valid()]):
        recipe = form.save(commit=False)
        recipe.save()
        #formset.save()   
        for ingredient_form in formset:
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe=recipe
            ingredient.save() 
        context['message']='数据已保存'
    return render(request,"recipes/create-update.html",context)

@login_required
def recipe_delete_view(request,id=None):
    obj = get_object_or_404(Recipe,id=id)
    obj.delete()
    


