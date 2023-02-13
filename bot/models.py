from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    class Meta:
        verbose_name = "Telegram profil"
        verbose_name_plural = "Telegram profillar"

    tg_id = models.CharField(max_length=16, unique=True, verbose_name="ID")
    tg_username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Telegram nomi (@username)")
    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Ismi")
    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Familiyasi")
    phone = models.CharField(max_length=25, default="-")
    step = models.CharField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tg_id or ""

    def save(self, *args, **kwargs):
        if self.phone and self.phone != "-" and self.phone[1] != "+":
            self.phone = "+{}".format(self.phone)
        super(Profile, self).save(*args, **kwargs)


class FAQ(models.Model):
    question = models.TextField(verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")

    class Meta:
        verbose_name = "Savol-javob"
        verbose_name_plural = "Savol-javoblar"

    def __str__(self) -> str:
        return self.question


class Info(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nomi")
    text = models.TextField(verbose_name="Matn")
    location_url = models.TextField(default=None, verbose_name="Google maps manzili")
    longitude = models.FloatField(default=None, null=True)
    latitude = models.FloatField(default=None, null=True)
    slug = models.SlugField(editable=False)

    class Meta:
        verbose_name = "Ma'lumotlar"
        verbose_name_plural = "Ma'lumotlar"

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        if self.location_url is not None:
            try:
                parts = self.location_url.split("@")[-1].split(",")
                self.latitude, self.longitude = float(parts[0]), float(parts[1])
            except Exception:
                pass
        return super(Info, self).save(*args, **kwargs)