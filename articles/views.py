from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from .models import Article
from .forms import ArticleForm

# Create your views here.

def article_search_view(request):
    #print(dir(request))
    query = request.GET.get('query')
    #lookups = Q(title__icontains=query) | Q(content__icontains=query)
    qs = Article.objects.search(query=query)
    
    context = {
        'object_list':qs
    }
    return render(request,"articles/search.html",context)





def article_detail_view(request,slug = None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except Exception as e:
            pass

    context = {
        'object':article_obj
    }
    return render(request,'articles/article_detail.html',context=context)

@login_required
def article_create_view(request):
    form = ArticleForm()
    if request.method=="POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_obj = form.save()
            #return redirect('article-detail',slug=article_obj.slug)
            return redirect(article_obj.get_absolute_url())
            # title = form.cleaned_data.get('title')            
            # content = form.cleaned_data.get('content')
            # Article.objects.create(title=title,content=content)
    context = {
        "form":form
    }
    return render(request,'articles/create.html',context=context)