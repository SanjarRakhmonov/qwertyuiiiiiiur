from django.shortcuts import render
from .models import Notification
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required



@login_required
def actions(request):
    all_actions = Action.objects.exclude(target_id=None)                                      
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        all_actions = all_actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    paginator = Paginator(all_actions, 12) # 3 posts in each page
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        actions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'actions/detail.html',
                      { 'actions': actions ,})
    return render(request, 'feeds/feeds.html', {
        'actions': actions,
        })


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()

    return render(request, 'activities/notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()

    return render(request,
                  'activities/last_notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)
    return HttpResponse(len(notifications))
