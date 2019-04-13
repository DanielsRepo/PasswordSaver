from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from page1.models import Post, Theme
from .forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse, FileResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

def all_posts(request):
    themes = Theme.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'page1/all_posts.html', {'posts': posts, 'themes': themes})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    themes = Theme.objects.all()
    entries = post.theme.entries.all()
        
    return render(request, 'page1/post_detail.html', {'post': post, 'themes': themes, 'entries': entries})

    filename = 'C:\Django\img.png'
    return FileResponse(open(filename, 'rb'), as_attachment=True)

    data = {'A': [{'a':'aa', 'aa':'aaa'}], 'B':'b',}
    return JsonResponse(data)

class PostDetailView(DetailView):
    model = Post
    template_name = 'page1/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        post = self.object
        context['post'] = post
        context['entries'] = post.theme.entries.all()

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
            # return HttpResponseRedirect(reverse('post_detail', kwargs = {'pk' : 'post.pk'})) не пашит
    else:
        form = PostForm()
        themes = Theme.objects.all()
        return render(request, 'page1/post_edit.html', {'form': form, 'themes': themes})

class PostCreateView(CreateView):
    template_name = 'page1/post_edit.html'
    form_class = PostForm
    success_url = reverse_lazy('post_detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull = True).order_by('-created_date')
    themes = Theme.objects.all()
    context = {'posts': posts, 'themes': themes}

    template = loader.get_template('page1/post_draft_list.html')

    # return HttpResponse(template.render(context, request))
    return HttpResponse(render_to_string('page1/post_draft_list.html', context, request))
    # return render(request, 'page1/post_draft_list.html', {'posts': posts})

class PostDraftView(ListView):
    model = Post
    template_name = 'page1/post_draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('-created_date')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('all_posts')

def by_theme(request, pk):
    try:
        posts = Post.objects.filter(theme = pk).order_by('-published_date')
        themes = Theme.objects.all()
        curr_theme = Theme.objects.get(pk = pk)
        context = {'posts': posts, 'themes': themes, 'curr_theme': curr_theme}

        print(request.is_secure())
        print(request.get_port())
        print(request.get_host())
        print(request.build_absolute_uri(request.get_full_path()))
    except Theme.DoesNotExist:
        # raise Http404('NO THIS PAGE!!!')
        return StreamingHttpResponse(('Oh', 'no', 'this', 'page', 'here!'), content_type='text/plain; charset=utf-8')


    return render(request, 'page1/by_themes.html', context)

class ThemeListView(ListView):
    model = Post
    template_name = 'page1/by_themes.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(theme = self.kwargs['pk']).order_by('-published_date')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['themes'] = Theme.objects.all()
        context['curr_theme'] = Theme.objects.get(pk = self.kwargs['pk'])

        return context
