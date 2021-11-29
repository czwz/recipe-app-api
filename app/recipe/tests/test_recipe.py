from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse("recipe:recipe-list")


def sample_recipe(user, **kwargs):
    """create and return a sample recipe"""
    default = {
        "title": "sampel recipe",
        "time_minute": 10,
        "price": 5
    }
    default.update(kwargs)
    return Recipe.objects.create(user=user, **default)


class PublicRecipeApiTests(TestCase):
    """test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_autho_required(self):
        """test that authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """test authenticated recipe api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@dummy.com",
            "dummy123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """test retrieving a list of recipe"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipe = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            "test2@dummy.com",
            "dummy123"
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
