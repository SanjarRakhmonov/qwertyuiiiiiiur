import os
from PIL import Image

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings as django_settings
from django.shortcuts import render, redirect, get_object_or_404

from core.forms import ProfileForm, ChangePasswordForm
from posts.models import Feed
from posts.views import FEEDS_NUM_PAGES
from posts.views import actions_list
from user.forms import UserEditForm
from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseForbidden


def home(request):
    if request.user.is_authenticated():
        return actions_list(request)
    else:
        return render(request, 'home.html')


@login_required
def network(request):
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'core/network.html', {'users': users})


def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, 10)
    page = request.GET.get('page')
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        feeds = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        feeds = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'feeds/partial_feed.html', {'page_user':page_user, 'feeds':feeds,})
    return render(request, 'core/profile.html', {
        'page_user': page_user,
        'feeds': feeds,
        })

		
def profile_images(request, username):
	page_user = get_object_or_404(User, username=username)
	return render(request, 'core/images.html', {'page_user': page_user, })

def profile_followers(request, username):
	page_user = get_object_or_404(User, username=username)
	return render(request, 'core/followers.html', {'page_user': page_user, })
	
def profile_following(request, username):
	page_user = get_object_or_404(User, username=username)
	return render(request, 'core/following.html', {'page_user': page_user, })

@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid() and user_form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.about = form.cleaned_data.get('about')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        user_form = UserEditForm(instance=request.user)
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'url': user.profile.url,
            'location': user.profile.location,
            'about': user.profile.about,
            })
    return render(request, 'core/settings.html', {'form': form})


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except:
        pass

    return render(request, 'core/picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form})


@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 550:
            new_width = 550
            new_height = (height * 550) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/settings/picture/?upload_picture=uploaded')

    except:
        return redirect('/settings/picture/')


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((300, 300), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except:
        pass

    return redirect('/settings/picture/')
