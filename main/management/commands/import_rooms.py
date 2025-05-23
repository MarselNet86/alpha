import pandas as pd
from django.core.management.base import BaseCommand
from main.models import Room  # замени на свой app и модель

class Command(BaseCommand):
    help = 'Импортирует номера из Excel-файла'

    def handle(self, *args, **kwargs):
        filepath = 'main/management/commands/rooms.xlsx'
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при чтении файла: {e}'))
            return

        count = 0
        for _, row in df.iterrows():
            Room.objects.create(
                floor=row['floor'],
                floor_number=row['floor_number'],
                category=row['category'],
                status=row['status'],
                price=row['price'],
                room_id=row['room_id']
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Импортировано {count} записей из {filepath}'))
