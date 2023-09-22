from django import forms
from django.core import validators
from tickets.models import Match, MatchClub, Sector


class TicketsForm(forms.Form):

    def __init__(self, match, *args, **kwargs):
        super(TicketsForm, self).__init__(*args, **kwargs)
        self.matches = Match.objects.all()
        self.this_match = self.matches.get(slug=match)
        self.stadium = self.this_match.stadium
        self.fields['match'] = forms.ModelChoiceField(queryset=self.matches, initial=self.this_match, label='Матч',
                                                      widget=forms.Select(attrs={'class': "form-select"}))
        self.fields['price'] = forms.IntegerField(label='Цена',
                                                  widget=forms.NumberInput(attrs={'class': "form-control"}))
        price = self.fields['price']
        price.validators.append(validators.MinValueValidator(0))
        price.widget.attrs['min'] = price.min_value = 0
        self.fields['sectors'] = forms.ModelMultipleChoiceField(
            queryset=Sector.objects.filter(sec_stadium=self.stadium), label='Секторы',
            widget=forms.SelectMultiple(attrs={'class': "form-select"})
        )

    class Meta:
        widgets = {
            'match': forms.Select(attrs={'class': "form-select"}),
            'price': forms.NumberInput(attrs={'class': "form-control"}),
            'sectors': forms.SelectMultiple(attrs={'class': "form-select"}),
        }


class AddMatchForm(forms.ModelForm):
    add_tickets = forms.BooleanField(label='Сгенерировать билеты', required=False,
                                     widget=forms.CheckboxInput())  # initial=True

    class Meta:
        model = Match
        fields = ['tournament', 'datetime_match', 'stadium']


class MatchClubForm(forms.ModelForm):

    class Meta:
        model = MatchClub
        fields = ['club', 'is_home']
