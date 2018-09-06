from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from blog_app.forms import PostForm, CommentForm
from blog_app.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    #queryset pozwala filtrować pokazywane dane
    def get_queryset(self): #wez wszystkie posty i przefiltruj, lte=less_or_than_equals (exact= rowne),  - to descending
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post


#w widokach jako klasy nie dziala dekorator
#trzeba uzyc mixinow
class CreatePostView(LoginRequiredMixin, CreateView):
    #te dwa pola dla mixin
    login_url = '/login/' #jak nie zalogowany idz do login
    redirect_field_name = 'blog/post_detail.html'

    #create view polaczone z modelem i form
    form_class = PostForm
    model = Post

class UpdatePostView(LoginRequiredMixin, UpdateView):
    #te dwa pola dla mixin
    login_url = '/login/' #jak zalogowany idz do login
    redirect_field_name = 'blog/post_detail.html'

    #create view polaczone z modelem i form
    form_class = PostForm
    model = Post

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    
#draft to nieopublikowane posty
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/draft_list_view.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


####################################
####################################
@login_required
def post_publish(request,pk):
     post = get_object_or_404(Post,pk=pk)
     post.publish()
     return redirect('post_detail',pk=pk)


@login_required
def add_comment_to_post(request,pk): ##pk do komentarza
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':        #jak ktos wypelnia dokument i klika na submit to zapisz
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  #bo comment ma post jako fk
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm() #jak get to storz formularz
    return render(request, 'blog_app/comment_form.html', {'form':form}) # i przekaz do templatki

#zatwierdzanie komentarzt
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk) #wez komentarz
    comment.approve() #wywolaj na nim metode approve() z modelu Comment (comment jest objektem klasy Comment)
    return redirect('post_detail',pk=comment.post.pk) #wez z modelu comment pole post i wez jego pk

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk) #wez komentarz
    post_pk = comment.post.pk #zapisz pk bo potem bedzie usuniete
    comment.delete()
    return redirect('post_detail',pk=post_pk)