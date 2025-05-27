from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'proposals', views.ProposalViewSet)

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('update/<int:pk>/', views.ad_update, name='ad_update'),
    path('delete/<int:pk>/', views.ad_delete, name='ad_delete'),
    path('proposal/', views.proposal_create, name='proposal_create'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposal/update/<int:pk>/', views.proposal_update, name='proposal_update'),
    path('api/', include(router.urls)),
]