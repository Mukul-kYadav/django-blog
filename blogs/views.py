from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import posts
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    content = {'posts': posts.objects.all()}
    return render(request, 'blogs/index.html', content)

class PostListView(ListView):
    model = posts
    template_name = 'blogs/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = posts
    template_name = 'blogs/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return posts.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    


def about(request):
    content = {'posts':posts.objects.all()}
    return render(request, "blogs/about.html", content)