from django.db import models

PROPERTY_TYPE_CHOICES = [
    ('studio', 'Студия'),
    ('1_room', '1-комнатная'),
    ('2_room', '2-комнатная'),
    ('3_room', '3-комнатная'),
    ('4_room', '4-комнатная'),
    ('5_plus', '5+ комнат'),
]

class Property(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    location = models.CharField("Местоположение", max_length=200)
    bedrooms = models.IntegerField("Количество спален", blank=True, null=True)
    bathrooms = models.IntegerField("Количество ванных комнат")
    area = models.IntegerField("Площадь (м²)")
    property_type = models.CharField(
        "Тип недвижимости",
        max_length=10,
        choices=PROPERTY_TYPE_CHOICES,
        default='1_room'
    )
    image = models.ImageField("Фото", upload_to='properties/', blank=True, null=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_property_type_display()} — {self.location}"

    class Meta:
        verbose_name = "Недвижимость"
        verbose_name_plural = "Недвижимость"


class Employee(models.Model):
    name = models.CharField("Имя", max_length=100)
    position = models.CharField("Должность", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    image = models.ImageField("Фото", upload_to='team/', blank=True, null=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"