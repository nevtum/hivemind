from .models import Comment
from django.shortcuts import render

def comments_for_defect(request, pk):
    comments = Comment.objects.filter(defect__id=pk)
    return render(request, 'defect_comments.html', {'comments': comments})