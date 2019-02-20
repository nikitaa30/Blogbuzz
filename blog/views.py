# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404 

from django.db.models import Q 
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView, DetailView
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from urllib import quote_plus





class FileExamListView(ListView):
	model = Post
	template_name = "blog/post_list.html"
	paginate_by = 5

def contact(request):
	return render(request, 'personal/contact.html')

	
def post_list(request):
	queryset_list= Post.objects.active()#.filter(draft=False).filter(publish__lte=timezone.now())#
	if request.user.is_staff or request.user.is_superuser:
		queryset_list= Post.objects.all()

	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(Q(title__icontains=query) | 
			Q(body__icontains=query)).distinct()

	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)

	except PageNotAnInteger:

		queryset = paginator.page(1)

	except EmptyPage:

		queryset = paginator.page(paginator.num_pages)


	context = {
	"object_list": queryset,
	"title":"List"
	}
	return render(request, "blog/post_list.html", context)

def post_detail(request, id=None):
	instance= get_object_or_404(Post, id=id)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	
	share_string = quote_plus(instance.body)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request,"blog/blog_view.html", context)

def post_create(request):

	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form= PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user=request.user
		print form.cleaned_data.get("title")
		instance.save()
		messages.success(request, "SUccessfully Created!")
		return HttpResponseRedirect(reverse('detail',args=(instance.id,)))
	else:
		messages.error(request, "Not Quite Right")
	context = {
	"form": form,
	}
	return render(request, "blog/forma.html", context)


def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post, id=id)
	form= PostForm(request.POST or None , request.FILES or None, instance= instance)
	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.save()
		messages.success(request, "SUccessfully Updated!")
		return HttpResponseRedirect(reverse('detail',args=(instance.id,)))

	context = {
	"title": instance.title,
	"instance": instance,
	"form": form,
	}
	return render(request, "blog/forma.html", context)

def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "SUccessfully Deleted!")
	return redirect('http://127.0.0.1:8000/blog/')








# Create your views here.
