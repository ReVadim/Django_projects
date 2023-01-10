from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag

from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery


def post_list(request, tag_slug=None):
    """ Display posts by tags
    """
    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    # pagination
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


class PostListView(ListView):
    """ Class-based view to list posts
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3


def post_detail(request, year, month, day, post):
    """ Detail information about post
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
    }

    return render(request, 'blog/post/detail.html', context=context)


def post_share(request, post_id):
    """ Published post by id
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{data['name']}\'s comments: {data['comments']}"
            send_mail(subject, message, 'revani.web@gmail.com', [data['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


# for POST method only
@require_POST
def post_comment(request, post_id):
    """ add comment to post and render than
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create comment object without saving it in the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save to the database
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }

    return render(request, 'blog/post/comment.html', context=context)


def post_search(request):
    """ Search view
    """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:  # look for the query parameter in the request.GET dictionary
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
            # search for published posts with a custom SearchVector instance

    context = {
        'form': form,
        'query': query,
        'results': results
    }

    return render(request, 'blog/post/search.html', context=context)
