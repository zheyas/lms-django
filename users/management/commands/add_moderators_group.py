from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создает группу модераторов, если её нет'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модераторы')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" создана'))
        else:
            self.stdout.write('Группа "Модераторы" уже существует')
