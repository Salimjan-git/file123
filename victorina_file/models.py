from django.db import models
from django.contrib.auth.models import AbstractUser

class  User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Муаллим'),
        ('student', 'Талаба'),
        ('group_leader', 'Сарвари гурӯҳ'),
    )
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,default='student')
    created_at = models.DateTimeField(auto_now_add=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"