from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost


def hello_page(request):
    my_title = "Hello there..."
    # return HttpResponse("<h1>Hello</h1>")
    return render(request, "hello.html", {"title": my_title})


# def home_page(request): # Old Home Page
#     context = {"title": "this is HOME page", "li": [1,2,3,4]}
#     return render(request, "home.html", context)


def home_page(request):
    qs = BlogPost.objects.all().published()[:5]
    head_title = "Home"
    context = {"title": "Welcome to Try Django", "li": qs, "head_title": head_title}
    return render(request, "home.html", context)


def better_page(request):
    normal_var = "Normal Title"
    context = {"title": normal_var}
    if request.user.is_authenticated:
        context = {"title": "Welcome " + request.user.first_name, "li": [1,2,3,4]}
    return render(request, "better.html", context)


def about_page(request):
    return render(request, "about.html", {"title": "about us"})


def contact_page(request):
    head_title = "Contact"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact Us",
        "form": form,
        "head_title": head_title
    }
    return render(request, "form.html", context)


def example_page(request):
    context     = {"title": "Example"}
    template    = "example.html"
    return render(request, template, context)


def convention_page(request):
    context             = {"title": "Convention"}
    template_name       = "example.txt"
    template_obj        = get_template(template_name)
    return HttpResponse(template_obj.render(context))


def login_page(request):
    context     = {"title": "Login"}
    template    = "example.html"
    return render(request, template, context)
