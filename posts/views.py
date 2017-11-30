from django.shortcuts import render, redirect
from .models import Post, Like
from .forms import Postform, UserSignup, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

def home(request):
	context = {
		'title': "HOME BLOG"	
	}
	return render(request, 'home.html', context)

def posts_list(request):
	objects = Post.objects.all()
	#                           .order_by('title', 'id')  for ordering :)


	today = timezone.now().date()
	objects = Post.objects.filter(draft=False).filter(publish__lte=today)
	if request.user.is_staff or request.user.is_superuser:
		objects = Post.objects.all()

	query = request.GET.get("q")
	if query:
		objects = objects.filter(title__icontains=query)

	paginator = Paginator(objects, 3) # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		objects = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)
	
	context = {
		"objects": objects,
		"title": "List",
		"user": request.user,
		"today": today,
	}
	return render(request, 'posts_list.html', context)

def posts_detail(request, posts_slug):
	instance = Post.objects.get(slug = posts_slug)
	if instance.publish>timezone.now().date() or instance .draft:
		if not (request.user.is_staff or request.user.is_superuser):
			raise Http404

	if request.user.is_authenticated():
		if Like.objects.filter(post=instance, user=request.user).exists():
			liked = True
		else:
			liked = False
	post_like_count = instance.like_set.all().count()
	context = {
		"posts": instance,
		"instance": instance,
		#"share_string": quote(instance.content)
		"post_like_count":post_like_count,
		"liked":liked
	}
	return render(request, 'posts_detail.html', context)

def posts_create(request):
	if not request.user.is_staff:
		print("hehe xD")
		raise Http404
	form = Postform(request.POST or None, request.FILES or None)
	if form.is_valid():
		item = form.save(commit=False)
		item.author = request.user
		item.save()
		messages.success(request, 'Greate you just added a blog post :)')
		return redirect("more:list")
	context = {
		"form": form
	}
	return render(request, 'posts_create.html', context)


def posts_update(request, posts_slug):
	if not request.user.is_staff:
		raise Http404
	item = Post.objects.get(slug=posts_slug)

	form = Postform(request.POST or None, request.FILES or None, instance = item)
	if form.is_valid():
		form.save()
		messages.info(request, 'Update Done :)')
		return redirect("more:detail", posts_slug=item.slug)
	context = {
		"form": form,
		"item": item,
	}
	return render(request, 'posts_update.html', context)

def posts_delete (request, posts_slug):
	if not request.user.is_staff:
		raise Http404
	Post.objects.get(slug=posts_slug).delete()
	messages.warning(request, 'Deleteing Done :(')
	return redirect("more:list")

def ajax_like(request, post_id):
	post_object = Post.objects.get(id=post_id)
	new_like, created = Like.objects.get_or_create(user=request.user, post=post_object)

	if created:
		action="like"
	else:
		new_like.delete()
		action="unlike"

	post_like_count = post_object.like_set.all().count()

	response = {
		"action": action,
		"post_like_count": post_like_count,

	}
	return JsonResponse(response, safe=False)

def usersignup(request):
	context = {}
	form = UserSignup()
	context['form'] = form
	if request.method == 'POST':
		form = UserSignup(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("more:list")
		messages.error(request, form.errors)
		return redirect("more:signup")
	return render(request, 'signup.html', context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == 'POST':
		form = UserLogin(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('more:list')

			messages.error(request, "Wrong user/password combination. Please try again.")
			return redirect("more:login")
		messages.error(request, form.errors)
		return redirect("more:login")
	return render(request, 'login.html', context)


def userlogout(request):
	logout(request)
	return redirect('more:list')



