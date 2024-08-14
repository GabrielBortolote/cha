from rest_framework import routers
from base.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = router.urls