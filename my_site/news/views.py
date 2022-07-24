from django.shortcuts import render, redirect
from .models import News, Category
from .forms import NewsForm
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("login")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserCreationForm()
    return render(request, "news/register.html", {"form": form})


def login(request):
    return render(request, "news/login.html")


class HomeNews(MyMixin, ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная"
        context["mixin_prop"] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related("category")


class News_by_category(MyMixin, ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news"
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(
            category_id=self.kwargs["category_id"], is_published=True
        ).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(
        request,
        "news/category.html",
        {
            "news": news,
            "category": category,
        },
    )


class ViewNews(DetailView):
    model = News
    template_name = "news/view_news.html"
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.filter()

    context_object_name = "news_item"


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
