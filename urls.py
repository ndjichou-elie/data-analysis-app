from django.urls import path
from .views import UploadFileAPIView, StockDataAPIView, home_view, login_view, logout_view, signup_view, enable_2fa_view, \
    data_analysis_view, upload_file_view, preprocess_data_view, analysis_tools_view, reports_view, \
    visualization_view, predictive_modeling_view, classification_view, clustering_view, download_results, \
    feature_engineering_view, time_series_analysis_view, financial_analysis_view, profit_loss_view, \
    budget_analysis_view, financial_kpis_view, financial_statements_view, faq_view

urlpatterns = [
    # Home and Authentication
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('enable-2fa/', enable_2fa_view, name='enable-2fa'),

    # FAQ
    path('faq/', faq_view, name='faq'),

    # API Endpoints
    path('api/upload-file/', UploadFileAPIView.as_view(), name='api-upload-file'),
    path('api/stock-data/', StockDataAPIView.as_view(), name='api-stock-data'),

    # Data Analysis Section
    path('data/analysis/', data_analysis_view, name='data-analysis'),
    path('data/upload/', upload_file_view, name='upload-file'),
    path('data/preprocess/', preprocess_data_view, name='preprocess-data'),
    path('data/tools/', analysis_tools_view, name='analysis-tools'),
    path('data/reports/', reports_view, name='reports'),
    path('data/visualization/', visualization_view, name='visualization'),
    path('predictive-modeling/', predictive_modeling_view, name='predictive-modeling'),
    path('classification/', classification_view, name='classification'),
    path('clustering/', clustering_view, name='clustering'),
    path('download/<str:result_type>/', download_results, name='download-results'),
    path('data/feature-engineering/', feature_engineering_view, name='feature-engineering'),
    path('time-series/', time_series_analysis_view, name='time-series'),

    # Financial Analysis Section
    path('finance/analysis/', financial_analysis_view, name='financial-analysis'),
    path('finance/profit-loss/', profit_loss_view, name='profit-loss'),
    path('finance/budget/', budget_analysis_view, name='budget-analysis'),
    path('finance/kpis/', financial_kpis_view, name='financial-kpis'),
    path('finance/statements/', financial_statements_view, name='financial-statements'),
    path('api/upload-file/', UploadFileAPIView.as_view(), name='api-upload-file'),
]
