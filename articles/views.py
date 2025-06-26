
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from accounts.models import UserRate
from .models import Article, Comment
from accounts.forms import CommentForm

#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    page = Article.objects.all() 
    paginate_by = 2

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    #form_class = CommentForm


    
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title','summary', 'body','photo',)
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(CreateView,LoginRequiredMixin, UserPassesTestMixin,):
    model = Article
    template_name = 'article_new.html'
    fields = ('title','summary','body','photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class AddCommentView(CreateView):
    model = Comment
    forms_class = CommentForm
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        comment_text = request.POST.get('comment')
        parent_id = request.POST.get('parent')
        article_id = kwargs.get('pk')
        print(parent_id)
        article = Article.objects.get(id=article_id)
        comment = Comment.objects.create(
            parent_id=parent_id,
            article_id=article_id,
            comment=comment_text,
            author=request.user
        )
        print(comment)
        return redirect('article_detail', pk=article_id)

#like     
def rate_article(request, artc_id, ):
    article_query = Article.objects.filter(id=artc_id)
    if article_query.exists:
        article = article_query.first()
        if article.rates.filter(user=request.user).count():
            article.rates.filter(user=request.user).delete()
        else:
             UserRate.objects.create(
                user=request.user,
                article=article, 
            )
        return redirect('article_list')

