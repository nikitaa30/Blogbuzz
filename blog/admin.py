# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display=["title", "date"]
	list_display_links=["title"]

	search_fields = ["title","date"]

	class Meta:
		model=Post



admin.site.register(Post, PostModelAdmin)




# Register your models here.
