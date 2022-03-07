from django.shortcuts import render
from recipes.models import Recipe
from articles.models import Article

SEARCH_MAPPING={
    'article':Article,
    'articles':Article,
    'recipe':Recipe,
    'recipes':Recipe,
}

def search_view(request):
    query = request.GET.get('query')
    search_type = request.GET.get('search_type')
    Klass = Recipe
    if search_type in SEARCH_MAPPING.keys():
        Klass = SEARCH_MAPPING[search_type]

    qs = Klass.objects.search(query=query)
    context = {
        'queryset':qs,
    }
    template = "search/results-view.html"
    if request.htmx:
        context['queryset'] = qs[:5]
        template = "search/partials/results.html"
    return render(request,template,context)
