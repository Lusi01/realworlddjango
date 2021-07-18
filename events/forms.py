from django import forms
from events.models import Event, Enroll, Favorite, Category, Feature


class EventFilterForm(forms.Form):
    category = forms.ModelChoiceField(
                    label='Категория',
                    queryset=Category.objects.all(),
                    required=False,)
    features = forms.ModelMultipleChoiceField(
                    label='Свойства',
                    queryset=Feature.objects.all(),
                    required=False)
    date_start = forms.DateTimeField(
                    label='Дата начала',
                    widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
                    required=False)
    date_end = forms.DateTimeField(
                    label='Дата конца',
                    widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
                    required=False)
    is_private = forms.BooleanField(
                    label='Приватное',
                    widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                    required=False)
    is_available = forms.BooleanField(
                    label='Есть места',
                    widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                    required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['category'].widget.attrs.update({'class': 'form-control', 'selected': "selected", 'initial': self.fields['category'] })
        self.fields['features'].widget.attrs.update({'class': 'form-control', 'multiple': True, 'selected':
            "selected", 'initial': self.fields['features'] })
        self.fields['date_start'].widget.attrs.update({'class': 'form-control mx-1'})
        self.fields['date_end'].widget.attrs.update({'class': 'form-control mx-1'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-check', 'default': False })
        self.fields['is_available'].widget.attrs.update({'class': 'form-check ', 'default': False})




class EventCreateUpdateForm(forms.ModelForm):

    date_start = forms.DateTimeField(
                    label='Дата начала',
                    widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M",attrs={'type': 'datetime-local'}),)

    class Meta:
        model = Event
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['description'].widget.attrs.update({ 'rows': 3})
        self.fields['is_private'].widget.attrs.update({'class': 'custom_check'})



class EventCreationForm(EventCreateUpdateForm):
    class Meta:
        model = Event
        fields = '__all__'

    # запретить создание уже существующего события
    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if Event.objects.filter(title=title).exists():
            raise forms.ValidationError(f'Такое событие: {title} уже существует')

        return cleaned_data



class EventUpdateForm(EventCreateUpdateForm):
    class Meta:
        model = Event
        fields = '__all__' # если только 1 полое, то обязательно после него + запятую!



class EnrollCreationForm(forms.ModelForm):
    class Meta:
        model = Enroll
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    # запретить создание уже существующей записи
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if Enroll.objects.filter(user=cleaned_data['user'], event=cleaned_data['event']).exists():
            raise forms.ValidationError(f'Вы уже записаны на это событие: ')

        return cleaned_data



class FavoriteCreationForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    # запретить создание уже существующей записи
    def clean(self):
        cleaned_data = super().clean()

        if Favorite.objects.filter(user=cleaned_data['user'], event=cleaned_data['event']).exists():
            raise forms.ValidationError(f'Вы уже записали событие в избранное!')

        return cleaned_data
