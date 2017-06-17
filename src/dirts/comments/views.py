from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404, redirect, render

from comments.forms import CommentEditForm
from comments.models import Comment

from ..models import Defect


def comments_for_defect(request, pk):
    comments = Comment.objects.filter(defect__id=pk)
    comments = comments.select_related('author')
    res = {
        'pk': pk,
        'comments': comments,
        'form': CommentEditForm()
    }
    return render(request, 'defects/comments.html', res)

def add_comment_for_defect(request, pk):
    form = CommentEditForm(request.POST or None)
    if form.is_valid() and pk:
        form.instance.author = get_user(request)
        form.instance.defect = Defect.objects.get(pk=pk)
        form.save()
    return redirect('defects:defect-comments:list', pk)
