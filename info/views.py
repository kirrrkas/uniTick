from django.db.models import Q
from django.views.generic import DetailView, ListView
from info.models import Article, ClubInfo, TournamentInfo
from django import forms
from django_filters import FilterSet, OrderingFilter, CharFilter, ModelMultipleChoiceFilter
from django_filters.views import FilterView


class ArticleFilter(FilterSet):
    search = CharFilter(method='filter_by_title_content', label='Поиск')
    order = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('title', 'title'),
            ('time_create', 'time_create'),
        ),

        # labels do not need to retain order
        field_labels={
            'title': 'Заголовок',
            'time_create': 'Время публикации',
        },
        label="Сортировать"
    )
    clubs = ModelMultipleChoiceFilter(field_name='clubs', queryset=ClubInfo.objects.all(),
                                      widget=forms.CheckboxSelectMultiple(), label='Клубы')
    tournaments = ModelMultipleChoiceFilter(field_name='tournaments', queryset=TournamentInfo.objects.all(),
                                            widget=forms.CheckboxSelectMultiple(), label='Турниры')

    class Meta:
        model = Article
        exclude = [
            'title',
            'slug',
            'content',
            'is_published',
            'image',
            'time_create'
        ]

    @property
    def qs(self):
        parent = super(ArticleFilter, self).qs

        return parent.filter(is_published=True)

    def filter_by_title_content(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )


class ArticleList(FilterView):
    model = Article
    template_name = 'info/index.html'
    context_object_name = 'article_list'
    filterset_class = ArticleFilter


class ShowArticle(DetailView):
    model = Article
    template_name = 'info/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'


class ShowClubInfo(DetailView):
    model = ClubInfo
    template_name = 'info/about.html'
    slug_url_kwarg = 'club_slug'
    context_object_name = 'info'

    def get_object(self, queryset=None):
        slug = self.kwargs['club_slug']
        obj = ClubInfo.objects.get(tickets_key__slug=slug)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['articles'] = obj.article_set.all()
        return context


class ShowTournamentInfo(DetailView):
    model = TournamentInfo
    template_name = 'info/about.html'
    slug_url_kwarg = 'tournament_slug'
    context_object_name = 'info'

    def get_object(self, queryset=None):
        slug = self.kwargs['tournament_slug']
        obj = TournamentInfo.objects.get(tickets_key__slug=slug)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['articles'] = obj.article_set.all()
        return context


class ClubList(ListView):
    model = ClubInfo
    template_name = 'info/about_list.html'


class TournamentList(ListView):
    model = TournamentInfo
    template_name = 'info/about_list.html'

