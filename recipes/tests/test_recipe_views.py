from django.urls import reverse, resolve
from recipes import views
from .test_tecipe_base import RecipeTestBase

# Create your tests here.



class RecipeViewsTest(RecipeTestBase):
    
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

        self.assertEqual(response_recipes.first().title, 'Recipe Title')
        response_context = response.content.decode('utf-8')
        self.assertIn('Recipe Title', response_context)
        self.assertIn('10 Minutos', response_context)
        self.assertIn('5 Porções', response_context)
        self.assertIn('Café da Manhã', response_context)


    # RECIPE CATEGORY

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)


    # RECIPE DETAIL

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

