from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import reverse
from django.http import HttpResponse,Http404
from .models import Recipe,RecipeIngredient
from .forms import RecipeForm,RecipeIngredientForm,RecipeIngredientImageForm
# CRUD Create Retrieve Update Delete
# LIST

@login_required
def recipe_detail_view(request,id=None):
    hx_url = reverse('recipes:hx-detail',kwargs={"id":id})
    context = {
        'hx_url':hx_url
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
        if request.htmx:
            headers ={
                "HX-Redirect":obj.get_absolute_url()
            }
            return HttpResponse("菜谱已创建",headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request,"recipes/create-update.html",context)

@login_required
def recipe_update_view(request,id=None):
    obj = get_object_or_404(Recipe,id=id,user=request.user)
    form = RecipeForm(request.POST or None,instance=obj)
    new_ingredient_url = reverse("recipes:hx-ingredient-create",kwargs={'id':obj.id})
    context = {
        'new_ingredient_url':new_ingredient_url,
        "form":form,
        "object":obj 
    }
    if form.is_valid():
        form.save()
        context['message']='数据已保存'    
        
    if request.htmx:
        return render(request,'recipes/partials/forms.html',context)
    return render(request,"recipes/create-update.html",context)

@login_required
def recipe_delete_view(request,id=None):
    try:
        obj = Recipe.objects.get(id=id,user=request.user)
    except:
        obj = None

    if obj is None:
        if request.htmx:
            return HttpResponse("未找到")
        raise Http404
    
    if request.method=='POST':
        obj.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            headers = {
                'HX-Redirect':success_url
            }
            return HttpResponse("删除成功",headers=headers)
        return redirect(success_url)
    context = {
        'object':obj
    }
    return render(request,'recipes/delete.html',context)

@login_required
def recipe_ingredient_delete_view(request,parent_id=None,id=None):
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id,id=id,recipe__user=request.user)
    except:
        obj = None

    if obj is None:
        if request.htmx:
            return HttpResponse("未找到")
        raise Http404
    
    if request.method=='POST':
        name = obj.name
        obj.delete()
        success_url = reverse('recipes:detail',kwargs={'id':parent_id})
        if request.htmx:        
            # return HttpResponse("<span style='color:#ccc;'>材料已删除</span>")
            return render(request,'recipes/partials/ingredient-inline-delete-response.html',{"name":name})
        return redirect(success_url)
    context = {
        'object':obj
    }
    return render(request,'recipes/delete.html',context)
    
@login_required
def recipe_detail_hx_view(request,id=None):
    if not request.htmx:
        return Http404
    try:
        obj = Recipe.objects.get(id=id,user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse("未找到")
        #raise Http404
    context = {
        'object':obj
    }
    return render(request,"recipes/partials/detail.html",context)

@login_required
def recipe_ingredient_detail_hx_view(request,id=None,ingredient_id=None):
    if not request.htmx:
        return Http404
    try:
        parent_obj = Recipe.objects.get(id=id,user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("未找到")
        #raise Http404
    instance=None
    if ingredient_id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj,id=ingredient_id)
        except:
            instance = None
    
    form = RecipeIngredientForm(request.POST or None,instance=instance)
    url = instance.get_hx_edit_url() if instance else reverse("recipes:hx-ingredient-create",kwargs={'id':parent_obj.id})
    context = {
        'url':url,
        'form':form,
        'object':instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request,"recipes/partials/ingredient-inline.html",context)
   
    return render(request,"recipes/partials/ingredient-form.html",context)


def recipe_ingredient_image_upload_view(request,parent_id=None):
    print(request.FILES.get('image'))
    try:
        parent_obj = Recipe.objects.get(id=parent_id,user=request.user)
    except:
        parent_obj = None
    
    if parent_obj is None:
        raise Http404
    
    form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        obj.save()

    return render(request,"image-form.html",{"form":form})