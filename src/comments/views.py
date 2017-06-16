from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .forms import CommentEditForm
from .models import Comment

class OwnerOr403Mixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerOr403Mixin, self).dispatch(request, *args, **kwargs)

class CommentEditView(OwnerOr403Mixin, UpdateView):
    model = Comment
    template_name = 'comments/edit_comment.html'
    context_object_name = 'comment'
    form_class = CommentEditForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        # set toggle that comment is edited
        comment.save()
        return redirect(reverse('defects:defect-comments:list', kwargs={ 'pk': comment.defect.id }))

class CommentDeleteView(OwnerOr403Mixin, DeleteView):
    model = Comment
    template_name = 'comments/delete_comment.html'
    context_object_name = 'comment'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.defect.id
        success_url = reverse('defects:defect-comments:list', kwargs={ 'pk': pk })
        self.object.delete()
        return redirect(success_url)
