from django.contrib import admin
from . import models


class Fullness(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'fullness'

    def lookups(self, request, model_admin):
        filter_list = (
            ('1', 'sold-out'),
            ('2', '>50%'),
            ('3', '<= 50%'),
        )
        return filter_list

    def queryset(self, request, queryset):
        events_id = []
        rez = ''
        for el in self.lookup_choices:
            if self.value() in el:
                rez = el[1]

        for event in queryset:
            sampling_principle =  (str(event.display_places_left()).find(rez) >= 0)
            if sampling_principle == True:
                events_id.append(event.id)

        return queryset.filter(id__in=events_id)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_event_count', ]
    list_display_links = ['id', 'title', ]


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    list_display_links = ['id', 'title', ]


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', ]
    list_display_links = ['id', 'user', 'event', ]


@admin.register(models.Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created', ]
    list_display_links = ['id', 'user', 'event', ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'rate', 'created', 'updated']
    list_display_links = ['id', 'user', 'event', ]
    fields = [ 'user', 'event', 'rate', 'text', ('created', 'updated'), 'id']
    readonly_fields = ['id', 'created', 'updated']
    list_filter = ['created', 'event',]


class ReviewInstanceInline(admin.TabularInline):
    model = models.Review
    fields = ['id', 'user', 'event', 'rate', 'text', 'created', 'updated', ]
    readonly_fields = ['id', 'user', 'event', 'rate', 'text', 'created', 'updated', ]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'date_start', 'is_private', 'participants_number',
                    'display_enroll_count', 'display_places_left', 'count_rate',]  #'count_rate',  'display_enroll_count',
    list_select_related = ['category', ]
    list_display_links = ['id', 'title' ]
    inlines = [ ReviewInstanceInline]
    fields = ['title', 'description', 'date_start', 'participants_number', 'is_private', 'category',
               'features', 'display_enroll_count', 'display_places_left', 'count_rate', 'logo', ] #'count_rate',
    filter_horizontal = ['features']
    readonly_fields = ['display_enroll_count', 'display_places_left', 'count_rate', ] #'count_rate'
    ordering= ['date_start']
    search_fields = ['title']
    list_filter = [Fullness, 'category', 'features', ]


