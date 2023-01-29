from rest_framework.routers import DefaultRouter
from projects.apis import views

router = DefaultRouter()
router.register(r"projects", views.ProjectsViewSet, basename="projects")
router.register(r"reorders", views.ProjectsReordersViewSet, basename="reorders")

urlpatterns = router.urls
