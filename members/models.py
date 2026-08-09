from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Member(models.Model):
    GENDER_CHOICES = [('male','Male'),('female','Female'),('other','Other'),('prefer_not','Prefer not to say')]
    MARITAL_STATUS_CHOICES = [('single','Single'),('married','Married'),('divorced','Divorced'),('widowed','Widowed')]
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?[1-9]\d{7,14}$', message='Phone must be E.164 format')
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='single')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
