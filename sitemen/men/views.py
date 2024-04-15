from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm, ContactForm
from .models import Men, Category, TagPost, UploadFiles
from .utils import DataMixin
from .utils import menu


class MenHome(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        m_lst = cache.get('men_posts')
        if not m_lst:
            m_lst = Men.published.all().select_related('cat', 'author')
            cache.set('men_posts', m_lst, 60)
        return m_lst

@login_required
def about(request):
    list_of_men = Men.published.all()
    paginator = Paginator(list_of_men, 3)
    page_number = request.GET.get('page')
    current_page = paginator.get_page(page_number)
    return render(request, 'men/about.html', {'title': 'О сайте', 'menu': menu, 'current_page': current_page})




class ShowPost(DataMixin, DetailView):
    # model = Men
    template_name = 'men/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Men.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Add post'
    permission_required = 'men.add_men'

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)

class UpdatePage(DataMixin, UpdateView):
    model = Men
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Update post'

class DeletePage(DataMixin, DeleteView):
    model = Men
    template_name = 'men/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Delete post'

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'men/contact.html'
    success_url = reverse_lazy('home')
    title_page = 'Contact'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

def login(request):
    # t = render_to_string('men/index.html')
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")

class MenCategory(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False
    def get_queryset(self):
        return Men.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat', 'author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


class TagPostList(DataMixin, ListView):
    template_name = 'men/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Men.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Tag - ' + tag.tag)

