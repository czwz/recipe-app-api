from django.urls import path, include
from rest_framework.routers import SimpleRouter

from recipe import views


router = SimpleRouter()
router.register("tags", views.TagViewSet, "tag")
router.register("ingredients", views.IngredientViewSet, "ingredient")
router.register("recipes", views.RecipeViewSet, "recipe")

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
