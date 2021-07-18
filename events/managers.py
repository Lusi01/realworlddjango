from django.db import models
from django.db.models import Q, Prefetch
from django.db.models.functions import Coalesce



class EventQuerySet(models.QuerySet):
    def with_counts(self):
        return self.annotate(
            count=Coalesce(models.Count('enrolls'), 0),
            #available=models.F('participants_number') - self.count,
            #available=models.F('participants_number')-models.F('count'),
            available=models.F('participants_number') - models.Count('enrolls')
            #available = models.F('participants_number') - models.Max(display_enroll_count())
        )

    def EvQuSet(self):
        return self.select_related('category').prefetch_related('enrolls__user', 'features',
                    'reviews__user').with_counts()



