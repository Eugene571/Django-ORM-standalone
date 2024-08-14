import os
import django
from django.utils import timezone
import math

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()


from datacenter.models import Passcard, Visit, get_duration, convert_seconds, is_visit_long  # noqa: E402


if __name__ == '__main__':

    all_passcards = Passcard.objects.all()
    print(all_passcards, '\n')

    example_passcard = Passcard.objects.all()[0]
    print(f'owner_name: {example_passcard.owner_name}\n'
          f'passcode: {example_passcard.passcode}\n'
          f'created_at: {example_passcard.created_at}\n'
          f'is_active: {example_passcard.is_active}\n'
          )

    active_passcards = Passcard.objects.filter(is_active=True)
    print('Всего пропусков: ',
          Passcard.objects.count(), '\n'
          'Активных пропусков: ',
          len(active_passcards), '\n'
          )

    all_visits = Visit.objects.all()
    print(all_visits)

    currently_in_storage = Visit.objects.filter(leaved_at=None)
    print(currently_in_storage, '\n')

    for visit in all_visits:
        if visit.leaved_at is None:
            current_duration = math.trunc(get_duration(visit))
            print(f'Зашёл в хранилище, время по Москве: \n{visit.entered_at}\n'
                  'Находится в хранилище:', '\n', convert_seconds(current_duration), '\n'
                  )
            print(visit.passcard, '\n')

    person_0_visits = all_visits[0].passcard
    all_passes_0 = Visit.objects.filter(passcard=person_0_visits)
    print(all_passes_0)

    current_year = timezone.now().year
    visits_current_year = Visit.objects.filter(entered_at__year=current_year).order_by('-entered_at')
    suspicious_visits_hour = is_visit_long(visits_current_year, 60, limit=10)
    print(f"Визиты дольше 1 часа: {suspicious_visits_hour}")
