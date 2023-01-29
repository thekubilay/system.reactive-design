from rest_framework.routers import DefaultRouter
from tasks.apis import views

router = DefaultRouter()
router.register(r"tasks", views.TasksViewSet, basename="tasks")

urlpatterns = router.urls
