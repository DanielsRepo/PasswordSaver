from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog_app.models import Post, Theme
from .forms import PostForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse, FileResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from bootstrap_modal_forms.generic import BSModalLoginView
from blog_app.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userobj = form.cleaned_data
            username = userobj['username']
            email = userobj['email']
            password = userobj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


class LoginView(BSModalLoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('blog_app/all_posts.html')
    authentication_form = LoginForm


def all_posts(request):
    themes = Theme.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog_app/all_posts.html', {'posts': posts, 'themes': themes})

# class AllPostsView(ArchiveIndexView):
#     model = Post
#     date_field = 'published_date'
#     template_name = 'blog_app/all_posts.html'
#     context_object_name = 'posts'

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['themes'] = Theme.objects.all()
#         # context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#         return context


class AllPostsView(ListView):
    model = Post
    template_name = 'blog_app/all_posts.html'
    paginate_by = 5
    context_object_name = 'posts'
    queryset = Post.objects.published()
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['themes'] = Theme.objects.all()
        context['users'] = User.objects.all()
        return context


def get_others_posts(request, username):
    user = User.objects.get(username=username)

    return render(request, 'blog_app/all_posts.html', {
        'posts': Post.objects.by_user(user),
        'themes': Theme.objects.all(),
        'users': User.objects.all()
    })


class MyPostsView(ListView):
    model = Post
    template_name = 'blog_app/user_posts.html'
    paginate_by = 5
    context_object_name = 'posts'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['themes'] = Theme.objects.all()
        context['posts'] = Post.objects.by_user(self.request.user)
        context['users'] = User.objects.all()
        return context


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    themes = Theme.objects.all()
    entries = post.theme.entries.all()
        
    return render(request, 'blog_app/post_detail.html', {'post': post, 'themes': themes, 'entries': entries})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        post = self.object
        context['post'] = post
        context['themes'] = Theme.objects.all()
        context['entries'] = post.theme.entries.published()
        context['users'] = User.objects.all()
        return context


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        themes = Theme.objects.all()
        users = User.objects.all()

        return render(request, 'blog_app/post_new.html', {'form': form, 'themes': themes, 'users': users})


class PostCreateView(CreateView):
    template_name = 'blog_app/post_new.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['themes'] = Theme.objects.all()
        context['users'] = User.objects.all()
        return context


class PostEditView(UpdateView):
    model = Post
    template_name = 'blog_app/post_edit.html'
    form_class = PostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['themes'] = Theme.objects.all()
        context['users'] = User.objects.all()
        return context


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull = True).order_by('-created_date')
    themes = Theme.objects.all()
    context = {'posts': posts, 'themes': themes}

    template = loader.get_template('blog_app/post_draft_list.html')

    # return HttpResponse(template.render(context, request))
    return HttpResponse(render_to_string('blog_app/post_draft_list.html', context, request))
    # return render(request, 'blog_app/post_draft_list.html', {'posts': posts})


class PostDraftView(ListView):
    model = Post
    template_name = 'blog_app/post_draft_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.drafts()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['themes'] = Theme.objects.all()
        context['drafts_count'] = Post.objects.drafts().count()
        context['users'] = User.objects.all()
        return context


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.author = request.user
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('all_posts')


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'


def by_theme(request, pk):
    try:
        posts = Post.objects.filter(theme=pk).order_by('-published_date')
        themes = Theme.objects.all()
        curr_theme = Theme.objects.get(pk=pk)
        context = {'posts': posts, 'themes': themes, 'curr_theme': curr_theme}

        print(request.is_secure())
        print(request.get_port())
        print(request.get_host())
        print(request.build_absolute_uri(request.get_full_path()))
    except Theme.DoesNotExist:
        # raise Http404('NO THIS PAGE!!!')
        return StreamingHttpResponse(('Oh', 'no', 'this', 'page', 'here!'), content_type='text/plain; charset=utf-8')

    return render(request, 'blog_app/by_themes.html', context)


class ThemeListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog_app/by_themes.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.by_theme(self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['themes'] = Theme.objects.all()
        context['curr_theme'] = Theme.objects.get(pk = self.kwargs['pk'])
        context['users'] = User.objects.all()
        return context
