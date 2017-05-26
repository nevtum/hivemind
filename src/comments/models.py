from dirts.models import Defect
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE)
    author = models.ForeignKey(User)
    timestamp = models.DateTimeField()
    content = models.TextField(blank=False)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('comment-detail', kwargs={'pk': self.id})
