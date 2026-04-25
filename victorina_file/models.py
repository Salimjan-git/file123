from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class  User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Муаллим'),
        ('student', 'Талаба'),
        ('group_leader', 'Сарвари гурӯҳ'),
    )
    email = models.EmailField(max_length=254,unique=True)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,default='student')
    created_at = models.DateTimeField(auto_now_add=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    

class Profile(models.Model):
    LEVEL_TYPE_CHOICES = (
        ('school', 'Мактаб'),
        ('university', 'Донишгоҳ'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile',verbose_name="Корбар")
    level_type = models.CharField(max_length=50,choices=LEVEL_TYPE_CHOICES,default='school',verbose_name="Навъи таҳсил")
    current_level = models.IntegerField(default=1,verbose_name="Синф/Курс")
    
    class Meta:
        verbose_name = "Профил"
        verbose_name_plural = "Профилҳо"
        
    def __str__(self):
        return f"{self.user.email} - {self.level_display}"
    
    def clean(self):
        if self.level_type == "school" and not (1 <= self.current_level <= 11):
            raise ValidationError("Синф бояд аз 1 то 11 бошад")
        if self.level_type == "university" and not (1 <= self.current_level <=4):
            raise ValidationError("Курс бояд аз 1 то 4 бошад")
        
    @property
    def level_display(self):
        if self.level_type == "school":
            return f"Синфи {self.current_level}"
        return f"Курси {self.current_level}" 
        
        
class Subject(models.Model):
    LEVEL_TYPE_CHOICES = (
        ('school', 'Мактаб'),
        ('university', 'Донишгоҳ'),
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20 , blank=True,null=True)
    grade_level = models.CharField(max_length=20,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    color = models.CharField(max_length=7,default="#0c0d14")
    icon = models.CharField(max_length=50 , default="fas fa-book")
    is_public = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    max_students = models.PositiveIntegerField(default=0)
    pass_percentage = models.PositiveIntegerField(default=60)
    prerequisites = models.TextField(blank=True,null=True)
    level_type = models.CharField( max_length=50,choices=LEVEL_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=False)
    
    class Meta:
        verbose_name = 'Фан'
        verbose_name_plural = 'Фанҳо'
        unique_together = ['name', 'level_type']
    
    def __str__(self):
        return f"{self.name} ({self.get_level_type_display()})"
    
    
