from django.shortcuts import render,get_object_or_404
from .models import Post
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib.auth import authenticate, login
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
# Create your views here.


"""def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blogpost/index.html', {'posts' : posts})"""


"""def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogpost/post_detail.html', {'post': post})"""


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

class PostListView(ListView):
    model = Post
    template_name = 'blogpost/index.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blogpost/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post

    success_url ="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
