from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest,\
                        HttpResponseForbidden
from posts.models import Feed
from actions.models import Activity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.template.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
import re
from ttp import ttp
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User


FEEDS_NUM_PAGES = 10

'''
@login_required
def posts(request, tag_slug=None):
    object_list = Feed.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 12) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'feeds/detail.html',
                      { 'posts': posts , 'tag':tag})

    return render(request, 'feeds/list.html', {'posts': posts, 'tag':tag})
'''
@login_required
def actions_list(request):
    actions = Action.objects.exclude(user=request.user, target_id=None)
    following_ids = request.user.following.values_list('id', flat=True)
    page = request.GET.get('page')
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    paginator = Paginator(actions, 12)
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        actions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'feeds/partial_action.html', {'actions': actions})
    return render(request, 'feeds/main.html', {'actions': actions})
    #from_feed = -1
    #if feeds:
    #    from_feed = feeds[0].id
    #return render(request, 'feeds/main.html', {
     #   'feeds': feeds,
      #  'from_feed': from_feed,
       # 'page': 1,
        #})


@login_required
@ajax_required
def post(request):
    last_feed = request.POST.get('last_feed')
    user = request.user
    csrf_token = str(csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    posted = request.POST['post']
    hashtag=re.compile( r'(^|[^#\w])#(\w{1,30})\b')
    hashtag = re.sub( r'(^|[^#\w])#(\w{1,15})\b', '\\1<a href="http://127.0.0.1:8000/hashtag/\\2">#\\2</a>', posted )
    post = re.sub( r'(^|[^@\w])@(\w{1,15})\b', '\\1<a href="http://127.0.0.1:8000/\\2">@\\2</a>', hashtag )
    post = post.strip()
    if len(post) > 0:
        feed.post = post[:255]
        feed.save()
        create_action(request.user, post, feed)
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)

	
@login_required
def feeds(request):
    all_feeds = Feed.get_feeds()
    paginator = Paginator(all_feeds, 8)
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
        return render(request, 'feeds/partial_feed.html', {'feeds':feeds})
    return render(request, 'feeds/feeds.html', {'feeds':feeds})

def feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    return render(request, 'feeds/feed.html', {'feed': feed})


@login_required
@ajax_required
def load(request):
    from_feed = request.GET.get('from_feed')
    page = request.GET.get('page')
    feed_source = request.GET.get('feed_source')
    all_feeds = Feed.get_feeds(from_feed)
    if feed_source != 'all':
        all_feeds = all_feeds.filter(user__id=feed_source)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
    html = u''
    csrf_token = str(csrf(request)['csrf_token'])
    for feed in feeds:
        html = u'{0}{1}'.format(html,
                                render_to_string('feeds/partial_feed.html',
                                                 {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token
                                                    }))

    return HttpResponse(html)


def _html_feeds(last_feed, user, csrf_token, feed_source='all'):
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    html = u''
    for feed in feeds:
        html = u'{0}{1}'.format(html,
                                render_to_string('feeds/partial_feed.html',
                                                 {
                                                    'feed': feed,
                                                    'user': user,
                                                    'csrf_token': csrf_token
                                                    }))

    return html


@login_required
@ajax_required
def load_new(request):
    last_feed = request.GET.get('last_feed')
    user = request.user
    csrf_token = str(csrf(request)['csrf_token'])
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)


@login_required
@ajax_required
def check(request):
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    count = feeds.count()
    return HttpResponse(count)

@login_required
@ajax_required
def like(request):
    feed_id = request.POST['feed']
    feed = Feed.objects.get(pk=feed_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id,
                                   user=user)
    if like:
        user.profile.unotify_liked(feed)
        like.delete()

    else:
        like = Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
        like.save()
        user.profile.notify_liked(feed)

    return HttpResponse(feed.calculate_likes())


@login_required
@ajax_required
def comment(request):
    if request.method == 'POST':
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            feed.comment(user=user, post=post)
            user.profile.notify_commented(feed)
            user.profile.notify_also_commented(feed)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})

    else:
        feed_id = request.GET.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})


@login_required
@ajax_required
def update(request):
    first_feed = request.GET.get('first_feed')
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    feeds = Feed.get_feeds().filter(id__range=(last_feed, first_feed))
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    dump = {}
    for feed in feeds:
        dump[feed.pk] = {'likes': feed.likes, 'comments': feed.comments}
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def track_comments(request):
    feed_id = request.GET.get('feed')
    feed = Feed.objects.get(pk=feed_id)
    return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})



@login_required
@ajax_required
def remove(request):
    try:
        feed_id = request.POST.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        action=Action.objects.get(target_id=feed_id)
        if feed.user == request.user:
            likes = feed.get_likes()
            parent = feed.parent
            for like in likes:
                like.delete()
            if action:
                action.delete()
            feed.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()

@login_required
@ajax_required
def remove_comment(request):
    try:
        feed_id = request.POST.get('feed')
        comment_id = request.POST.get('comment')
        feed = Feed.objects.get(pk=feed_id)
        comment = Feed.objects.get(pk=comment_id)
        if feed.user == request.user or comment.user==request.user:
            likes = comment.get_likes()
            parent = comment.parent
            for like in likes:
                like.delete()
            comment.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()
