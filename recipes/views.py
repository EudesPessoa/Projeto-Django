from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination
from utils.recipes.factory import make_recipe

from .models import Recipe

# Create your views here.



def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    # recipes = get_list_or_404(
    #     Recipe.objects.filter(is_published=True).order_by('-id')
    #     )
    # return render(request, 'recipes/pages/home.html', context={'recipes':[make_recipe() for _ in range(11)],})

    page_obj, pagination_range = make_pagination(request, recipes, 9)

    return render(request,
                  'recipes/pages/home.html',
                  context={'recipes':page_obj,
                  'pagination_range': pagination_range},
                  )



def category(request, category_id):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id,
    #     is_published=True
    # ).order_by('-id')

    # if not recipes:
    #     return HttpResponse(content='Not found', status=404)
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, 9)

    return render(request, 'recipes/pages/category.html', context={
        'recipes' : page_obj,
        'pagination_range': pagination_range,
        'title' : f'{recipes[0].category.name} - Category |',
    })


# def recipe(request, id):
#     return render(request,
#                   'recipes/pages/recipe-view.html',
#                   context={'recipe' : make_recipe(), 'is_detail_page' : True,}
#                   )


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     id=id,
    #     is_published=True,
    # ).order_by('-id').first()
    recipe = get_object_or_404(Recipe, id=id, is_published=True)

    return render(request,
                  'recipes/pages/recipe-view.html',
                  context={'recipe' : recipe,
                           'is_detail_page' : True,
                           'title': f'{recipe.title} |'
                           })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains = search_term) | 
            Q(description__icontains = search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, 9)

    return render(request, 'recipes/pages/search.html',
                  {'page_title': f'Search for "{search_term}" | ',
                   'search_term': search_term,
                   'recipes': page_obj,
                   'pagination_range': pagination_range,
                   'additional_url_query': f'&q={search_term}'
    })


