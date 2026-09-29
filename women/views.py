from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm, WomenUpdateForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixins


class WomenHome(DataMixins, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    title_page = "Main page"
    cat_selected = 0


    def get_queryset(self):
        return Women.published.all().select_related('cat')


def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "women/about.html", {'title': 'About us',  'page_obj': page_obj})


class ShowPost(DataMixins, DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixins, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    title_page = "Add post"
    success_url = reverse_lazy("home")
    permission_required = "women.add_women"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixins, UpdateView):
    model = Women
    form_class = WomenUpdateForm
    template_name = "women/addpage.html"
    title_page = "Update post"
    success_url = reverse_lazy("home")
    permission_required = "women.change_women"


@permission_required(perm="women.view_women", raise_exception=True)
def contact(request):
    return HttpResponse("Contact Us")


def login(request):
    return HttpResponse("Login page")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page Not Found</h1>")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Views by {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, "women/index.html", context=data)


class WomenCategory(DataMixins, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title="Category - " + cat.name, cat_selected=cat.pk)


class TagPostList(DataMixins, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title="Tag - " + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
