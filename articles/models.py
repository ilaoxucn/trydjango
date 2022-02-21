import random
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from django.db.models import Q
from slugify import slugify
from django.db.models import Q

class ArticleManager(models.Manager):
    def search(self,query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.get_queryset().filter(lookups)

class Article(models.Model):
    user = models.ForeignKey("auth.User",blank=True,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)

    objects = ArticleManager()

    def save(self,*args,**kwargs):
        # if self.slug is None:
        #     self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('articles:article-detail',kwargs={'slug':self.slug})




def slugify_instance_title(instance,new_slug=None,save=False,):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    qs = Article.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(3000,5000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance,save=save,new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance

def article_pre_save_receiver(sender,instance,*args,**kwargs):
    if instance.slug is None:
        slugify_instance_title(instance)

pre_save.connect(article_pre_save_receiver,sender=Article)

def article_post_save_receiver(sender,instance,created,*args,**kwargs):
    if created:
        if instance.slug is None:
            slugify_instance_title(instance,save=True)

post_save.connect(article_post_save_receiver,sender=Article)
    
    
    


