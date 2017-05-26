from django.shortcuts import redirect, render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CommentEditForm
from .models import Comment


class CommentEditView(UpdateView):
    model = Comment
    template_name = 'edit_comment.html'
    context_object_name = 'comment'
    form_class = CommentEditForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        # set toggle that comment is edited
        comment.save()
        return redirect(reverse('comments:list', kwargs={'pk': comment.defect.id}))

def edit_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    return render(request, 'edit_comment.html', { 'comment': comment })

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    return render(request, 'delete_comment.html', { 'comment': comment })
