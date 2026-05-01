from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from datetime import timezone

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
    
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='groups')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_groups')
    created_at = models.DateTimeField(auto_now_add=False)
    
    class Meta:
        erbose_name = 'Гурӯҳ'
        verbose_name_plural = 'Гурӯҳҳо'
        
    def __str__(self):
        return f'{self.name} ({self.subject.name})'
    
    

class GroupMember(models.Model):
    group = models.ForeignKey( Group, on_delete=models.CASCADE , related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='group_memberships')
    joined_at = models.DateTimeField(auto_now_add=False)
    
    
    class Meta:
        verbose_name = 'Аъзои гурӯҳ'
        verbose_name_plural = 'Аъзои гурӯҳҳо'
        unique_together = ['group', 'user']
        
    def __str__(self):
        return f'{self.user.username} in {self.group.name}'
    
class Quiz(models.Model):
    MODE_CHOICES = (
        ('individual', 'Индивидуалӣ'),
        ('group', 'Гурӯҳӣ'),
    )
    
    LEVEL_TYPE_CHOICES = (
        ('school', 'Мактаб'),
        ('university', 'Донишгоҳ'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Навишта'),
        ('published', 'Нашршуда'),
        ('active', 'Фаъол'),
        ('finished', 'Анҷомёфта'),
    )
    
    title = models.CharField(max_length=250,verbose_name="Сарлавҳа")
    description = models.TextField(blank=True,verbose_name='Тавсиф')
    subject = models.ForeignKey(Subject, verbose_name='Фан', on_delete=models.SET_NULL,related_name='quizzes',null=True,blank=True)
    qiuz_mode = models.CharField(max_length=50,choices=MODE_CHOICES , verbose_name='Реҷаи викторина')
    level_type = models.CharField(max_length=50 , choices=LEVEL_TYPE_CHOICES, verbose_name='Навъи сатҳ',default='school')
    end_level = models.IntegerField(verbose_name="Сатҳи анҷом")
    start_time = models.IntegerField(verbose_name="Вақти оғоз")
    end_time = models.IntegerField(verbose_name='Вақти анҷом')
    is_online = models.BooleanField(default=True,verbose_name='Онлайн')
    status = models.CharField(max_length=50 , choices=STATUS_CHOICES,verbose_name='Статус',default='draft')
    time_limit = models.IntegerField(default=30,verbose_name='Мӯҳлати вақт (дақиқа)',help_text='Дақиқаҳо')
    max_attempts = models.IntegerField(default=1,verbose_name='Максимум кӯшишҳо',help_text='Максимум кӯшишҳо')
    pass_percentage =  models.IntegerField(default=60,verbose_name='Фоиз барои гузарондан',help_text='Фоизи гузарондан')
    created_by = models.ForeignKey(User, verbose_name='Эҷодкунанда', on_delete=models.CASCADE , related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=False)
    
    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторинаҳо'
        ordering = ['-created_at']
    
    def __str__(self):
        subject_name = self.subject.name if self.subject else "Без предмета"
        return f"{self.title} ({subject_name})"
    
    def is_active(self):
        now = timezone.now()
        return self.status == 'active' and self.start_time <= now <= self.end_time