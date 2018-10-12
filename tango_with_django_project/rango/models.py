from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


    class Meta:
	    verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128 )
    url = models.URLField()
    views = models.IntegerField(default=0)
    txt = models.TextField(blank=True)
    file = models.FileField(upload_to='upload_file_from_page', max_length=100, blank=True)
    slug = models.SlugField(blank=True)


    def save(self, *args, **kwargs):
         self.slug = slugify(self.title)
         super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):

    user= models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username