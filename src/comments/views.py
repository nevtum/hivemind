from .models import Comment
from django.shortcuts import render, redirect

def comments_for_defect(request, pk):
    comments = Comment.objects.filter(defect__id=pk)
    res = {
        'pk': pk,
        'comments': comments
    }
    return render(request, 'defect_comments.html', res)

def add_comment_for_defect(request, pk):
    content = request.POST.get('newcomment')
    import pdb; pdb.set_trace()
    return redirect('comments:list', pk)