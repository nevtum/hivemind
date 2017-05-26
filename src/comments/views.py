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
        return redirect(reverse('comments:list', kwargs={ 'pk': comment.defect.id }))

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'delete_comment.html', { 'comment': comment })
    
    defect_id = comment.defect.id
    comment.delete()
    return redirect(reverse('comments:list', kwargs={ 'pk': defect_id }))



    # if request.method == 'GET':
    #     return render(request, 'delete_confirmation.html', {'id': pk})

    # defect = Defect.objects.get(pk=pk)
    # defect_model = defect.as_domainmodel()
    # event = defect_model.soft_delete(request.user, timezone.now())
    # EventStore.append_next(event)
    # defect.delete()
    # return redirect('dirts-list')
