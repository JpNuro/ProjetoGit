from celery import shared_task
from django.utils import timezone
import yfinance as yf
from .models import FinancialIndicator, APILog

@shared_task
def update_financial_indicators():
    # List of important financial indicators to track
    indicators = [
        {'symbol': '^BVSP', 'name': 'Ibovespa'},
        {'symbol': 'BRL=X', 'name': 'USD/BRL'},
        {'symbol': 'GC=F', 'name': 'Gold Futures'},
        {'symbol': 'CL=F', 'name': 'Crude Oil'},
        {'symbol': '^TNX', 'name': 'US 10Y Treasury Yield'}
    ]
    
    for indicator in indicators:
        try:
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(indicator['symbol'])
            history = ticker.history(period='1d')
            
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                previous_close = history['Open'].iloc[0]
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
                
                # Update or create the indicator in database
                FinancialIndicator.objects.update_or_create(
                    symbol=indicator['symbol'],
                    defaults={
                        'name': indicator['name'],
                        'current_value': current_price,
                        'change_value': change,
                        'change_percentage': change_percent,
                        'last_updated': timezone.now(),
                        'source': 'Yahoo Finance'
                    }
                )
                
                # Log successful API call
                APILog.objects.create(
                    endpoint=f"yfinance/{indicator['symbol']}",
                    response_data={'status': 'success'},
                    status_code=200
                )
                
        except Exception as e:
            # Log failed API call
            APILog.objects.create(
                endpoint=f"yfinance/{indicator['symbol']}",
                error_message=str(e),
                status_code=500
            )
            continue

@shared_task
def cleanup_old_logs():
    # Delete logs older than 30 days
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    APILog.objects.filter(timestamp__lt=thirty_days_ago).delete()
