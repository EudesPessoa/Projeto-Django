from django.urls import reverse, resolve
from recipes import views
from .test_tecipe_base import RecipeTestBase
from unittest.mock import patch

# Create your tests here.



class RecipeViewsHome(RecipeTestBase):
    
    # RECIPE HOME

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Não temos receitas no momento',
            response.content.decode('utf-8'))
        
    def test_recipe_home_template_load_recipes(self):
        self.make_recipe(category_data={
            'name': 'Café da Manhã'
        })
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        self.assertEqual(len(response_recipes), 1)

        self.assertEqual(response_recipes.object_list[0].title, 'Recipe Title')
        response_context = response.content.decode('utf-8')
        self.assertIn('Recipe Title', response_context)
        self.assertIn('10 Minutos', response_context)
        self.assertIn('5 Porções', response_context)
        self.assertIn('Café da Manhã', response_context)
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'Não temos receitas no momento',
            response.content.decode('utf-8'))
    
    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'author_data':{'username': f'u{i}'}, 'slug': f'f{i}'}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
