
import random
from django.http import HttpResponse
from django.template.loader import render_to_string
from articles.models import Article

def home_view(request,*args,**kwargs):    
    article_queryset = Article.objects.all()
    context = {
        'object_list':article_queryset,
    }
    # html_string = """
    #     <h1>{article.title}</h1><p>{article.content}</p>
    # """.format(**context)

    template_string = render_to_string("home-view.html",context=context)

    return HttpResponse(template_string)