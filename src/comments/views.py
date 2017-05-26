from .models import Comment
from dirts.models import Defect
from django.shortcuts import render, redirect


def edit_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    return render(request, 'edit_comment.html', { 'comment': comment })

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    return render(request, 'delete_comment.html', { 'comment': comment })