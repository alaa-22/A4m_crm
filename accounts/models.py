from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from company.validator import validate_phone


def image_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_images/user-{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, validators=[validate_phone])
    address = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to=image_upload, blank=True, null=True)
    date_of_birth = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email,
                               full_name=instance.first_name + ' ' + instance.last_name
                               )


class SiteSettings(models.Model):
    key = models.SlugField(max_length=50, unique=True)
    value = models.CharField(max_length=50, null=True)


class Log(models.Model):
    choices = [
        ("add", "add"),
        ("edit", "edit"),
        ("delete", "delete"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    action = models.CharField(choices=choices,max_length=100)
    old_data = models.TextField(max_length=1000, null=True)
    new_data = models.TextField(max_length=1000)
    ip_address = models.GenericIPAddressField(null=True)
    record_id = models.CharField(max_length=1000,blank=True,null=True)
    model_name = models.CharField(max_length=100)
