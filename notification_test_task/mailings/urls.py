from rest_framework import routers
from .api import MailingViewSet, ClientViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register('api/Mailing', MailingViewSet, 'Mailing')
router.register('api/Client', ClientViewSet, 'Client')
router.register('api/Message', MessageViewSet, 'Message')

urlpatterns = router.urls