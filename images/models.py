from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from actions.models import Activity
from django.utils.html import escape
import bleach
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ttp import ttp
from django.utils.timezone import now as timezone_now
import os

def upload_to(instance, filename):
	now = timezone_now()
	filename_base, filename_ext = os.path.splitext(filename)
	return "images/%s%s" % (
		now.strftime("%Y/%m/%Y%m%d%H%M%S"),
		filename_ext.lower(),)

class Image(models.Model):
    user = models.ForeignKey(User, related_name='images_created', blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, null=True)
    date = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(max_length=1000, blank=True, null=True)
    parent = models.ForeignKey('Image', null=True, blank=True, related_name='image_parent')
    #users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        #related_name='images_liked',
                                        #blank=True)
    #total_likes = models.PositiveIntegerField(db_index=True, default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)


		
		
		
    class Meta:
        verbose_name= 'Image'
        verbose_name_plural='Images'
        ordering = ('-date',)
		
    def __str__(self):
        return self.caption
		
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Image, self).save(*args, **kwargs)
        p = ttp.Parser()
        result = p.parse(self.caption)
        for tag in result.tags:
            self.tags.add(tag)
        super(Image, self).save(*args, **kwargs)

    
		
    def get_comments(self):
        return Image.objects.filter(parent=self).order_by('date')

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                        image=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                        image=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    def calculate_comments(self):
        self.comments = Image.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def comment(self, user, post):
        image_comment = Image(user=user, post=post, parent=self)
        image_comment.save()
        self.comments = Image.objects.filter(parent=self).count()
        self.save()
        return image_comment

    def linkfy_post(self):
        return bleach.linkify(escape(self.caption))
