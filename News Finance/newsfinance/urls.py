from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'indicators', views.FinancialIndicatorViewSet, basename='indicator')

app_name = 'newsfinance'

urlpatterns = [
    # News URLs
    path('', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('category/<slug:category_slug>/', views.NewsByCategoryView.as_view(), name='news_by_category'),
    
    # Financial Dashboard
    path('financial/', views.financial_dashboard, name='financial_dashboard'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
