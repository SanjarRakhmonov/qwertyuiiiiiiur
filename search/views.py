from django.shortcuts import render
from .forms import SearchForm
from haystack.query import SearchQuerySet
from django.contrib.auth.models import User

def search(request):
    form = SearchForm()
    cd = None
    results = None
    total_results = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(User).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
    return render(request, 'search/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results})

