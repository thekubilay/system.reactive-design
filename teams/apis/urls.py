from rest_framework.routers import DefaultRouter
from teams.apis import views

router = DefaultRouter()
router.register(r"teams", views.TeamsViewSet, basename="teams")

urlpatterns = router.urls
