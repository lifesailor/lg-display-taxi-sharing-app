from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Idea
from .forms import IdeaForm, CommentForm

# Create your views here.
@login_required
def idea_list(request):
    notices = Idea.objects.filter(author = 1)
    ideas = Idea.objects.filter(~Q(author = 1))
    return render(request, 'idea/list.html', {'notices': notices, 'ideas': ideas})

@login_required
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'idea/detail.html', {'idea': idea })

@login_required
def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user
            idea.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'idea/edit.html', {'form': form})

@login_required
def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user
            idea.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'idea/edit.html', {'form': form})

@login_required
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea_list')

@login_required
def add_comment_to_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.idea = idea
            comment.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = CommentForm()
    return render(request, 'idea/add_comment_to_idea.html', {'form': form, 'idea': idea })
