from django.test import TestCase

from .models import Recipe,RecipeIngredient
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('laoxu',password="abc123")

    def test_user_pw(self):
        checked = self.user_a.check_password("abc123")
        self.assertTrue(checked)
        
    
class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('laoxu',password="abc123")
        self.recipe_a = Recipe.objects.create(name="宫保鸡丁",user=self.user_a)
        self.recipe_b = Recipe.objects.create(name="鱼香肉丝",user=self.user_a)
        self.recipe_ingredient_a = RecipeIngredient.objects.create(recipe=self.recipe_a,name="西红柿",quantity="3.5",unit="个")
        self.recipe_ingredient_b = RecipeIngredient.objects.create(recipe=self.recipe_a,name='鸡蛋',quantity="abc",unit="个")

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(),1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(),2)
    
    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(),2)

    def test_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(),2)
    
    def test_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(),2)

    def test_unit_messure_validation(self):

        invalid_units = ['窗户','咖啡']
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredient(
                    name='鸡蛋',
                    quantity='2',
                    recipe = self.recipe_a,
                    unit = unit,
                )
                ingredient.full_clean()
        
    def test_valid_unit_messure_validation(self):

        invalid_units = ['个','克']
        for unit in invalid_units:
            ingredient = RecipeIngredient(
                name='鸡蛋',
                quantity='2',
                recipe = self.recipe_a,
                unit = unit,
            )
            ingredient.full_clean()

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)


    
        
