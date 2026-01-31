from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=20, choices=[
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('educator', 'Educator')
    ])
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    parent_pin = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, null=True, blank=True)
    grade_level = models.IntegerField(null=True, blank=True)
    preferences = models.JSONField(default=dict)
    timezone = models.CharField(max_length=50, default="UTC")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} Profile"

class SafetyLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_logs')
    session_id = models.UUIDField(null=True, blank=True)
    violation_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    original_input = models.TextField(null=True, blank=True)
    scrubbed_input = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict)
    parent_alerted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ConceptMastery(models.Model):
    mastery_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='concept_mastery')
    concept_name = models.CharField(max_length=100)
    mastery_level = models.CharField(max_length=20, choices=[
        ('exposure', 'Exposure'),
        ('understanding', 'Understanding'),
        ('mastery', 'Mastery')
    ], default='exposure')
    interaction_count = models.IntegerField(default=0)
    confidence_score = models.IntegerField(default=1)
    last_interaction = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'concept_name')

class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    message_count = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

class ParentSettings(models.Model):
    settings_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_settings')
    daily_time_limit_minutes = models.IntegerField(default=60)
    allowed_categories = models.JSONField(default=lambda: ["math", "science", "logic", "language", "general"])
    safety_alert_threshold = models.CharField(max_length=10, default="medium")
    weekly_report_enabled = models.BooleanField(default=True)
