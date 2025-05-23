from django.core.management.base import BaseCommand
from main.models import Room

class Command(BaseCommand):
    help = 'Выводит процент занятых номеров'

    def handle(self, *args, **kwargs):
        total_rooms = Room.objects.count()
        occupied_rooms = Room.objects.filter(status='занят').count()

        if total_rooms == 0:
            self.stdout.write(self.style.WARNING('⚠️ Нет ни одного номера в базе данных.'))
            return

        percent = (occupied_rooms / total_rooms) * 100
        self.stdout.write(self.style.SUCCESS(f'✅ Процент занятых номеров: {percent:.2f}%'))
