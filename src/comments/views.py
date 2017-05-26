from .models import Comment
from dirts.models import Defect
from django.shortcuts import render, redirect

def comments_for_defect(request, pk):
    comments = Comment.objects.filter(defect__id=pk)
    res = {
        'pk': pk,
        'comments': comments
    }
    return render(request, 'defect_comments.html', res)

def add_comment_for_defect(request, pk):
    comment = Comment()
    comment.content = request.POST.get('newcomment')
    comment.author = request.user
    comment.defect = Defect.objects.get(pk=pk)
    comment.save()
    return redirect('comments:list', pk)