# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView, DetailView
from django.db import models
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone




#overwriting the post.objects.all() by model manager to
#show only posts that are not drafts or not in future
#changed all to active so that detail can be seen,
#otherwise post_detail gives 404 for drafts sbecause all is filtered
class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())



def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)


class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

	title = models.CharField(max_length=140)
	slug = models.SlugField(unique=True)
	image= models.ImageField(upload_to = upload_location, null = True, blank=True, width_field="width_field", height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	draft= models.BooleanField(default=False)
	publish= models.DateField(auto_now=False, auto_now_add=False)
	
	body = models.TextField()
	date = models.DateTimeField()

	#linking post manager to posts 

	objects=PostManager()

# Create your models here.
 	def __str__(self):
 		return self.title     

 	

 	def get_absolute_url(self):
 		#return reverse("detail", kwargs={"id":self.id})
 		return "/blog/%s" %(self.id) 
 		#return HttpResponseRedirect(reverse('detail', args=[self.id]))

 	def get_contact_url():

 		return "/blog/contact"

 	class Meta:
 		ordering = ["-pk"]



def create_slug(instance, new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug

	qs= Post.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug= "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)

	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)
	




pre_save.connect(pre_save_post_receiver, sender=Post)








