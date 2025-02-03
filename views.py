
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache
from .serializers import FileUploadSerializer, StockSymbolSerializer
from .services import FinancialAPIService
from .forms import CustomUserCreationForm
from .models import UploadedFile, AnalysisReport
from .utils import send_notification_email
import pandas as pd
import pyotp
import magic
import logging

# Logger configuration
logger = logging.getLogger(__name__)

ALPHA_VANTAGE_API_KEY = settings.ALPHA_VANTAGE_API_KEY
ALLOWED_MIME_TYPES = {"text/csv", "application/vnd.ms-excel", "application/json"}

def validate_file(uploaded_file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(uploaded_file.read(1024))
    uploaded_file.seek(0)

    if file_mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Unsupported file type!")

class UploadFileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Limit requests per user

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]

            try:
                validate_file(uploaded_file)
                cache.set(f"uploaded_file_{request.user.id}", uploaded_file, timeout=3600)
                return Response({"message": "File uploaded successfully!"}, status=201)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)

        return Response(serializer.errors, status=400)

class StockDataAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = {"message": "Stock data fetched successfully!"}
        return Response(data)

@login_required
def reports_view(request):
    cached_reports = cache.get(f"user_reports_{request.user.id}")
    if cached_reports:
        return render(request, 'reports.html', {'reports': cached_reports})

    reports = AnalysisReport.objects.select_related('file').filter(file__user=request.user)
    cache.set(f"user_reports_{request.user.id}", reports, timeout=300)

    return render(request, 'reports.html', {'reports': reports})

@login_required
def enable_2fa_view(request):
    if request.method == "POST":
        auth_method = request.POST.get("auth_method")
        user = request.user

        if auth_method == "app":
            secret = user.generate_otp_secret()
            messages.success(request, "Scan this QR code in your authenticator app.")
            return render(request, "enable_2fa.html", {"otp_uri": user.get_totp_uri()})

        elif auth_method == "email":
            otp = pyotp.TOTP(user.otp_secret).now()
            send_notification_email(
                "Your 2FA Verification Code",
                f"Use this OTP: {otp}",
                user.email
            )
            messages.success(request, "Check your email for the 2FA code.")
            return redirect("login")

        else:
            messages.error(request, "Invalid authentication method.")
    return render(request, "enable_2fa.html")

@login_required
def upload_file_view(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        try:
            validate_file(uploaded_file)
            messages.success(request, "File uploaded successfully!")
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, "upload_file.html")

    return render(request, "upload_file.html")

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def data_analysis_view(request):
    return render(request, 'data_analysis.html')

@login_required
def preprocess_data_view(request):
    return render(request, 'preprocess_data.html')

@login_required
def analysis_tools_view(request):
    return render(request, 'analysis_tools.html')

@login_required
def visualization_view(request):
    return render(request, 'visualization.html')

@login_required
def predictive_modeling_view(request):
    return render(request, 'predictive_modeling.html')

@login_required
def classification_view(request):
    return render(request, 'classification.html')

@login_required
def clustering_view(request):
    return render(request, 'clustering.html')

@login_required
def download_results(request, result_type):
    return HttpResponse(f"Downloading results for {result_type}")

@login_required
def feature_engineering_view(request):
    return render(request, 'feature_engineering.html')

@login_required
def time_series_analysis_view(request):
    return render(request, 'time_series.html')

@login_required
def financial_analysis_view(request):
    return render(request, 'financial_analysis.html')

@login_required
def profit_loss_view(request):
    return render(request, 'profit_loss.html')

@login_required
def budget_analysis_view(request):
    return render(request, 'budget_analysis.html')

@login_required
def financial_kpis_view(request):
    return render(request, 'financial_kpis.html')

@login_required
def financial_statements_view(request):
    return render(request, 'financial_statements.html')

@login_required
def faq_view(request):
    return render(request, 'faq.html')

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    return render(request, 'signup.html')
