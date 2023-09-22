import time
from functools import wraps, partial

from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Max
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from extra_views import CreateWithInlinesView, InlineFormSetFactory
from tickets.forms import MatchClubForm, AddMatchForm, TicketsForm
from tickets.models import Match, MatchClub, Place, Ticket, Sector, Tournament, Club, Stadium
from django_filters import FilterSet, OrderingFilter, CharFilter, RangeFilter, ModelMultipleChoiceFilter
from django_filters.views import FilterView


# def home(request):
#     matches = Match.objects.all()
#     return render(request, 'tickets/index.html', {'matches': matches})


class MatchFilter(FilterSet):
    order = OrderingFilter(
        fields=(
            ('datetime_match', 'datetime_match'),
        ),

        field_labels={
            'datetime_match': 'Дата и время',
        },
        label="Сортировать"
    )
    tournaments = ModelMultipleChoiceFilter(field_name='tournament', queryset=Tournament.objects.all(),
                                            widget=forms.CheckboxSelectMultiple(), label="Турниры")
    clubs = ModelMultipleChoiceFilter(field_name='clubs', queryset=Club.objects.all(),
                                      widget=forms.CheckboxSelectMultiple(), label="Клубы")
    stadiums = ModelMultipleChoiceFilter(field_name='stadium', queryset=Stadium.objects.all(),
                                         widget=forms.CheckboxSelectMultiple(), label="Стадионы")

    class Meta:
        model = Match
        fields = [
            'order',
            'tournaments',
            'clubs',
            'stadiums',
        ]


class MatchList(FilterView):
    model = Match
    template_name = 'tickets/index.html'
    context_object_name = 'match_list'
    filterset_class = MatchFilter


class MatchClubInline(InlineFormSetFactory):
    model = MatchClub
    form_class = MatchClubForm
    factory_kwargs = {'extra': 2, 'max_num': 2, 'min_num': 2, 'can_delete': False}


class AddMatch(PermissionRequiredMixin, CreateWithInlinesView):
    permission_required = 'tickets.add_match'
    model = Match
    inlines = [MatchClubInline]
    form_class = AddMatchForm
    template_name = 'tickets/add_match.html'
    success_url = reverse_lazy('tickets:add_tickets')
    login_url = reverse_lazy('tickets:home')
    raise_exception = True

    def get_success_url(self):
        return reverse('tickets:add_tickets', kwargs={'match': self.object.slug})

    # def form_valid(self, form):
    #     """If the form is valid, redirect to the supplied URL."""
    #     self.form = form
    #     return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     add_tick = self.form.cleaned_data['add_tickets']
    #     if add_tick:
    #         return reverse('add_tickets', kwargs={'match': self.object.slug})
    #     else:
    #         return reverse('home')


# @login_required
@permission_required('tickets.add_ticket', raise_exception=True)
def add_tickets(request, match):
    tickets_form_set = formset_factory(wraps(TicketsForm)(partial(TicketsForm, match=match)))
    if request.method == 'POST':
        formset = tickets_form_set(request.POST, prefix='tickets')
        if formset.is_valid():
            # start_time = time.time()
            match_form = formset[0].cleaned_data.get('match')
            print(match_form)
            tickets_list = []
            for form in formset:
                cd = form.cleaned_data
                price = cd.get('price')
                sectors = cd.get('sectors')
                data_places = Place.objects.filter(p_sector__in=sectors)
                # Такой способ долго работает #
                # ticket_part = [Ticket(price=price, t_place=place, t_match=match_form) for place in data_places]
                # print(ticket_part)
                # tickets_list.extend(ticket_part)
                for place in data_places:
                    ticket = Ticket(price=price, t_place=place, t_match=match_form)
                    tickets_list.append(ticket)
                # print("Время выполнения:", time.time() - start_time)
            Ticket.objects.bulk_create(tickets_list)
    else:
        formset = tickets_form_set(prefix='tickets')
    return render(request, 'tickets/add_tickets.html', {'formset': formset, 'match': match})


class ShowMatch(DetailView):
    model = Match
    template_name = 'tickets/stadium.html'
    slug_url_kwarg = 'match_slug'
    context_object_name = 'match'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        sectors = Sector.objects.filter(sec_stadium=obj.stadium).order_by('name').all()
        context['sectors'] = sectors
        return context


@login_required
def show_sector(request, match_slug, sector_slug):
    if request.method == 'POST':
        tickets = request.POST.getlist('ticket[]')

        tickets_list = []
        current_user = request.user
        for ticket_id in tickets:
            ticket_query = Ticket.objects.get(id=ticket_id)
            ticket_query.on_sale = False
            ticket_query.owner = current_user
            tickets_list.append(ticket_query)
        Ticket.objects.bulk_update(tickets_list, ['on_sale', 'owner'])
        return redirect('userapp:profile')
    match = Match.objects.get(slug=match_slug)
    tickets = Ticket.objects.filter(t_place__p_sector__slug=sector_slug, t_match__slug=match_slug).\
        order_by('t_place__place').prefetch_related('t_place', 't_match').all()
    max_row = tickets.aggregate(Max('t_place__row'))['t_place__row__max']
    price = tickets.first()

    return render(request, 'tickets/sector.html', {'sector_slug': sector_slug, 'match_slug': match_slug,
                                                   'max_row': range(max_row, 0, -1),
                                                   'sector': Sector.objects.filter(slug=sector_slug).first().name,
                                                   'match': match,
                                                   'tickets': tickets, 'price': price.price,
                                                   # 'places': places
                                                   })
