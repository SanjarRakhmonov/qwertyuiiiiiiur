from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateImageForm, UpdateImageForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action
from django.conf import settings
from actions.models import Activity
from braces import views
from django.views import generic
import re
from ajaxuploader.views import AjaxFileUploader
ajax_uploader = AjaxFileUploader()

def image_detail(request, id):
    image = get_object_or_404(Image, id=id)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image,})


class CreateImageView(
        views.LoginRequiredMixin,
        generic.CreateView
):
    model = Image
    form_class = CreateImageForm
    template_name = 'images/image/create.html'

    def form_valid(self, form):
        
        user = self.request.user
        image=Image()
        image.user=user
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        posted = self.request.POST['caption']
        hashtag=re.compile( r'(^|[^#\w])#(\w{1,30})\b')
        hashtag = re.sub( r'(^|[^#\w])#(\w{1,15})\b', '\\1<a href="http://127.0.0.1:8000/hashtag/\\2">#\\2</a>', posted )
        caption = re.sub( r'(^|[^@\w])@(\w{1,15})\b', '\\1<a href="http://127.0.0.1:8000/\\2">@\\2</a>', hashtag )
        caption = caption.strip()
        image.save()
        create_action(request.user, ' ', self.object)
        messages.success(request, 'Image added successfully')
        # redirect to new created item detail view
        return redirect(self.object.get_absolute_url())
        #return super(CreateImageView, self).form_valid(form)


class UpdatePostView(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.UpdateView
):
    model = Image
    form_valid_message = 'Successfully updated your post.'
    form_class = UpdateImageForm
    template_name = 'images/image/create.html'

    def get(self, request, *args, **kwargs):
        image = Image.objects.get(id=kwargs['id'])

        if (post.user != request.user):
            messages.warning(
                request,
                'You don\'t have permission to update this post.',
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    'posts:view',
                    kwargs={'id': kwargs['id']}
                )
            )
        else:
            return super(UpdateImageView, self).get(request, *args, **kwargs)


@login_required
@ajax_required
def track_comments(request):
    image_id = request.GET.get('image')
    image = Image.objects.get(pk=image_id)
    return render(request, 'feeds/partial_image_comments.html', {'image': image})
			
@login_required
@ajax_required
def remove(request):
    try:
        image_id = request.POST.get('image')
        image = Image.objects.get(pk=image_id)
        action=Action.objects.get(target_id=image_id)
        if image.user == request.user:
            likes = image.get_likes()
            parent = image.parent
            for like in likes:
                like.delete()
            action.delete()
            feed.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except:
        return HttpResponseBadRequest()

@login_required
def image_create(request):
    """
    View for creating an Image using the JavaScript Bookmarklet.
    """
    if request.method == 'POST':
        # form is sent
        form = CreateImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
			# form data is valid
            image = form.save(commit=False)
            image.user=request.user
            posted = image.caption
            hashtag=re.compile( r'(^|[^#\w])#(\w{1,30})\b')
            hashtag = re.sub( r'(^|[^#\w])#(\w{1,15})\b', '\\1<a href="http://127.0.0.1:8000/hashtag/\\2">#\\2</a>', posted )
            caption = re.sub( r'(^|[^@\w])@(\w{1,15})\b', '\\1<a href="http://127.0.0.1:8000/\\2">@\\2</a>', hashtag )
            caption = caption.strip()
            image.caption=caption
            image.save()
            #image = form.save()
            create_action(request.user, ' ', image)
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            return redirect(image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = CreateImageForm()

    return render(request, 'images/image/create.html', {'section': 'images',
                                                        'form': form})
														
														
'''														
@ajax_required														
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                #create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
'''	

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})

@login_required
@ajax_required
def like(request):
    image_id = request.POST['image']
    image = Image.objects.get(pk=image_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, image=image_id,
                                   user=user)
    if like:
        user.profile.unotify_image_liked(image)
        like.delete()

    else:
        like = Activity(activity_type=Activity.LIKE, image=image_id, user=user)
        like.save()
        user.profile.notify_image_liked(image)

    return HttpResponse(image.calculate_likes())


@login_required
@ajax_required
def comment(request):
    if request.method == 'POST':
        image_id = request.POST['image']
        image = Image.objects.get(pk=image_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            image.comment(user=user, post=post)
            user.profile.notify_image_commented(image)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'image': image})

    else:
        image_id = request.GET.get('image')
        image = Image.objects.get(pk=image_id)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'image': image})



@login_required
@ajax_required
def remove(request):
    try:
        image_id = request.POST.get('image')
        image = Image.objects.get(pk=image_id)
        if image.user == request.user:
            likes = image.get_likes()
            parent = image.parent
            for like in likes:
                like.delete()
            image.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except:
        return HttpResponseBadRequest()



				   
