from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class SchoolInfo(models.Model):
    name = models.CharField(max_length=200, default="9-sonli umumiy o‘rta ta‘lim maktabi")
    short_name = models.CharField(max_length=50, default="9-Maktab")
    region = models.CharField(max_length=100, default="Toshkent shahri")
    district = models.CharField(max_length=100, default="Yunusobod tumani")
    address = models.CharField(max_length=255, default="Amir Temur shox ko‘chasi, 45-uy")
    phone = models.CharField(max_length=30, default="+998 (71) 234-56-78")
    email = models.EmailField(default="info@9maktab.uz")
    director_name = models.CharField(max_length=100, default="Abdullayev Rustam Karimovich")
    founded_year = models.PositiveIntegerField(default=1984)
    hero_title = models.CharField(max_length=255, default="Kelajak yetakchilarini tarbiyalovchi zamonaviy taʼlim maskani")
    hero_subtitle = models.TextField(default="9-Maktab — raqamli texnologiyalar, chuqurlashtirilgan aniq fanlar va iqtidorli yoshlar akademiyasi.")
    mission = models.TextField(default="Har bir o‘quvchining individual qobiliyatlarini ro‘yobga chiqarish va milliy qadriyatlar asosida global raqobatbardosh bilim berish.")
    vision = models.TextField(default="O‘zbekistonning eng ilg‘or, raqamlashgan va xalqaro andozalarga javob beradigan yetakchi maktablaridan biriga aylanish.")

    class Meta:
        verbose_name = "Maktab ma'lumotlari"
        verbose_name_plural = "Maktab ma'lumotlari"

    def __str__(self):
        return self.name

class Announcement(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'Umumiy e’lon'),
        ('academic', 'O‘quv jarayoni'),
        ('exam', 'Imtihon va sinovlar'),
        ('holiday', 'Bayram va dam olish kunlari'),
        ('urgent', 'Shoshilinch xabar'),
    )

    TARGET_CHOICES = (
        ('all', 'Barchaga'),
        ('students', 'Faqat o‘quvchilarga'),
        ('teachers', 'Faqat o‘qituvchilarga'),
        ('guardians', 'Faqat ota-onalarga'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.TextField(help_text="Qisqacha mazmuni")
    content = models.TextField(help_text="To'liq xabar matni")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    target_role = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    cover_image = models.CharField(max_length=500, blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "E'lon va yangilik"
        verbose_name_plural = "E'lonlar va yangiliklar"
        ordering = ['-is_pinned', '-published_at']

    def __str__(self):
        return self.title

class SchoolEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, default="Maktab faollar zali")
    organizer = models.CharField(max_length=150, default="Maktab maʼmuriyati")
    is_public = models.BooleanField(default=True)
    cover_image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Maktab tadbiri"
        verbose_name_plural = "Maktab tadbirlari"
        ordering = ['event_date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.event_date})"

class Achievement(models.Model):
    CATEGORY_CHOICES = (
        ('olympiad', 'Fan olimpiadalari'),
        ('sports', 'Sport musobaqalari'),
        ('arts', 'San’at va ijodkorlik'),
        ('academic', 'Xalqaro sertifikatlar (IELTS/SAT/CEFR)'),
        ('award', 'Davlat mukofotlari'),
    )

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='olympiad')
    winner_name = models.CharField(max_length=150, help_text="G'olib o'quvchi yoki jamoa")
    grade_or_role = models.CharField(max_length=50, help_text="Masalan: 9-A sinf o'quvchisi")
    description = models.TextField()
    date = models.DateField()
    badge_icon = models.CharField(max_length=50, default="Trophy")

    class Meta:
        verbose_name = "Maktab yutug'i"
        verbose_name_plural = "Maktab yutuqlari"
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.winner_name}"

class GalleryItem(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="Maktab hayoti")
    media_url = models.CharField(max_length=500)
    caption = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Galereya fotosi"
        verbose_name_plural = "Galereya fotolari"
        ordering = ['-id']

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=50, default="Umumiy savollar")
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Ko'p beriladigan savol (FAQ)"
        verbose_name_plural = "FAQ savollari"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question

class PublicInquiry(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('in_progress', 'Ko‘rib chiqilmoqda'),
        ('resolved', 'Hal etildi'),
        ('closed', 'Yopildi'),
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Murojaat va taklif"
        verbose_name_plural = "Murojaatlar va takliflar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name}: {self.subject} ({self.get_status_display()})"
