from django.db import models
from django.utils import timezone
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    if visit.leaved_at:
        return (visit.leaved_at - visit.entered_at).total_seconds()
    else:
        return (timezone.now() - visit.entered_at).total_seconds()


def convert_seconds(seconds):
    return str(datetime.timedelta(seconds=seconds))


def is_visit_long(visits, minutes=60, limit=None):
    suspicious_visits = []
    for visit in visits:
        visit_duration = get_duration(visit)
        if visit_duration >= minutes * 60:
            suspicious_visits.append(visit)
        if limit and len(suspicious_visits) >= limit:
            break
    return suspicious_visits
