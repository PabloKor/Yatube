from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page


# Create your views here.
@cache_page(20, key_prefix="index_page")
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by("-pub_date")
    # posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "posts/group.html", {"group": group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None,
                        files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'posts/new.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.order_by('-pub_date')
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'author': author,
               'page': page,
               'paginator': paginator}
    return render(request, 'posts/profile.html', context=context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    author = post.author
    form = CommentForm()
    items = post.comments.all()
    return render(request, 'posts/post.html', {'post': post, 'author': author, 'form': form, 'items': items})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post', username=username, post_id=post_id)
    return render(request, 'posts/comments.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if post.author != request.user:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username=username, post_id=post_id)
    return render(request, 'posts/post_new.html', {'form': form,
                                                   'post': post})


# Обработка ошибок 404, 500
def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
