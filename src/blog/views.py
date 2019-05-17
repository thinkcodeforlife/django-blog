from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm

# DB Methods:
# get -> 1 object (record) from database
# filter -> multiple objects (a list of records) from database

# @login_required decorator is one line code to check whether user is authenticated or not
@login_required
def blog_post_detail_page_oldest(request):
    obj = BlogPost.objects.get(id=1)
    # template_name = 'blog_post_detail.html'
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


@login_required
def blog_post_detail_page_older(request, post_id):
    # Old version (even if you make urls like <str:post_id> it tries to look up and query)
    # try:
    #     obj = BlogPost.objects.get(id=post_id)
    # except BlogPost.DoesNotExist:
    #     raise Http404
    # except ValueError:
    #     raise Http404
    # ======================================
    # New One
    obj = get_object_or_404(BlogPost, id=post_id)
    # template_name = 'blog_post_detail.html'
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


@login_required
def blog_post_detail_page(request, slug):
    # Phase 1
    # obj = get_object_or_404(BlogPost, slug=slug) # We got multiple objects error at first
    # ===============================================
    # Phase 2
    # queryset = BlogPost.objects.filter(slug=slug)
    # if queryset.count() != 1:
    #     raise Http404
    # obj = queryset.first()
    # We can't reach blogs with same slug
    # ===============================================
    # Phase 3
    # We change slug field adding unique=True
    obj = get_object_or_404(BlogPost, slug=slug)
    # template_name = 'blog_post_detail.html'
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


# CRUD
#
# GET -> Retrieve / List
#
# POST -> Create (Add) / Update (Edit) / Delete (Remove)
#
# Create Retrieve Update Delete
# =========================================

@staff_member_required
def blog_post_create_view(request):
    # create objects
    # ? use a form
    # template_name = "blog_post_create.html"
    # form = BlogPostForm(request.POST or None)
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # print(form.cleaned_data)

        # Django way
        # obj = BlogPost.objects.create(title=title)
        # title = form.cleaned_data['title']

        # Pythonic way
        # obj = BlogPost()
        # obj.title = title
        # obj.save()

        # Faster way
        # obj = BlogPost.objects.create(**form.cleaned_data)
        # form = BlogPostForm()

        # Fastest way A
        # form.save()
        # form = BlogPostModelForm()

        # Fastest way B
        obj = form.save(commit=False)
        obj.user = request.user # This is newer line for associating blog posts with users
        obj.save()
        form = BlogPostModelForm()

    # template_name = "blog/create.html"
    template_name = "blog/form.html"
    context = {"form": form}
    return render(request, template_name, context)


@login_required
def blog_post_retrieve_view(request, slug):
    # 1 object -> detail view
    head_title = "Details"
    obj = get_object_or_404(BlogPost, slug=slug)
    # template_name = "blog_post_retrieve.html"
    template_name = "blog/retrieve.html"
    context = {"object": obj, "title": "Post Details", "head_title": head_title}
    return render(request, template_name, context)


# @login_required
def blog_post_list_view(request):
    # list out objects
    # could be search
    head_title = "Blog"
    # qs = BlogPost.objects.all() # Oldest version (without filtering any pos)
    # qs = BlogPost.objects.published() # Old BlogPostManager.published method
    # qs = BlogPost.objects.all().published() # This one and below one are both same
    qs = BlogPost.objects.published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    # template_name = "blog_post_list.html" # This is old template name which is still kept
    template_name = "blog/list.html"
    context = {"object_list": qs, "head_title": head_title}
    return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
    head_title = "Edit"
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    # template_name = "blog_post_update.html" # Oldest
    # template_name = "blog/update.html" # Older
    template_name = "blog/form.html"
    context = {"form": form, "title": f"Update {obj.title}", "head_title": head_title}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    head_title = "Delete"
    obj = get_object_or_404(BlogPost, slug=slug)
    # template_name = "blog_post_delete.html"
    template_name = "blog/delete.html"
    if request.method == 'POST':
        obj.delete()
        return redirect('/blog')
    context = {"object": obj, "head_title": head_title}
    return render(request, template_name, context)

