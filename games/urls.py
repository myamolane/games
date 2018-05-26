# .. Imports
from rest_framework_nested import routers
from django.contrib import admin
from authentication.views import AccountViewSet, VerifiesViewSet
from django.conf.urls import url, include
from authentication.views import AccountViewSet, LoginView#, LogoutView
from authentication.views import LogoutView
from rest_framework_jwt.views import obtain_jwt_token
from owtd.views import AccountPlayerViewSet, PlayerViewSet, EquipRecordViewSet, EquipmentViewSet, PlayerEquipRecordViewSet
router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'verifies', VerifiesViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'equip-records', EquipRecordViewSet)
router.register(r'equipments', EquipmentViewSet)
accounts_router = routers.NestedSimpleRouter(
    router, r'accounts', lookup='account'
)
accounts_router.register(r'players', AccountPlayerViewSet)

players_router = routers.NestedSimpleRouter(
    router, r'players', lookup='player'
)
players_router.register(r'equip-records', PlayerEquipRecordViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(accounts_router.urls)),
    #url(r'^api/v1/auth/active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/auth/token/$', obtain_jwt_token),
    url(r'^api/v1/', include(players_router.urls)),
]
