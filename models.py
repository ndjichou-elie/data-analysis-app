from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
import pyotp

class CustomUser(AbstractUser):
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def generate_otp_secret(self):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()
        return self.otp_secret

    def verify_otp(self, otp):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp)

    def __str__(self):
        return self.username

class UploadedFile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField(
        upload_to='uploads/',
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'xlsx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="uploaded_files")

    def __str__(self):
        return self.name

class AnalysisReport(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='reports')
    report_name = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        unique_together = ('file', 'report_name')

    def __str__(self):
        return f"{self.report_name} - {self.file.name}"

class FinancialStatement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='financial_statements')
    statement_name = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.statement_name} - {self.user.username}"

class KPI(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='kpis')
    name = models.CharField(max_length=255)
    value = models.FloatField(validators=[MinValueValidator(0)])
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.value}"
