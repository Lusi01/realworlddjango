from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce


class SubscriberQuerySet(models.QuerySet):
    def with_counts(self):
        return self.annotate(
            letter_count=Coalesce(models.Count('letters'), 0),
            sent_letter_count=Coalesce(models.Count('letters', Q(letters__is_sent=True)), 0),
        )

