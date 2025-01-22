from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import News, NewsCategory, FinancialIndicator, APILog
from .tasks import update_financial_indicators

# Create your views here.

class NewsListView(ListView):
    model = News
    template_name = 'newsfinance/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.filter(
            is_published=True,
            published_at__lte=timezone.now()
        ).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'newsfinance/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True)

class NewsByCategoryView(ListView):
    model = News
    template_name = 'newsfinance/news_by_category.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            published_at__lte=timezone.now()
        ).order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(NewsCategory, slug=self.kwargs['category_slug'])
        return context

@login_required
def financial_dashboard(request):
    indicators = FinancialIndicator.objects.all().order_by('name')
    context = {
        'indicators': indicators,
        'last_update': indicators.first().last_updated if indicators.exists() else None
    }
    return render(request, 'newsfinance/financial_dashboard.html', context)

class FinancialIndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FinancialIndicator.objects.all()
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        update_financial_indicators.delay()
        return Response({'status': 'refresh task started'})

@login_required
def admin_dashboard(request):
    context = {
        'total_news': News.objects.count(),
        'published_news': News.objects.filter(is_published=True).count(),
        'categories': NewsCategory.objects.all(),
        'recent_api_logs': APILog.objects.order_by('-timestamp')[:10]
    }
    return render(request, 'newsfinance/admin_dashboard.html', context)
