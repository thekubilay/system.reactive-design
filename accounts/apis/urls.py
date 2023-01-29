from rest_framework.routers import DefaultRouter
from accounts.apis import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = router.urls
