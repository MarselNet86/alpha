from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    passport = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name
    

class Room(models.Model):
    floor = models.CharField(max_length=100)
    floor_number = models.IntegerField()
    category = models.CharField(max_length=100)
    status = models.CharField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    room_id = models.IntegerField()

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'Комната №{self.floor_number}'


class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    destroy = models.DateTimeField()

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'


    def __str__(self):
        return f'Карта №{self.id}'


class Role(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    password = models.CharField(max_length=128)
    last_login_date = models.DateTimeField()
    is_blocked = models.BooleanField(default=False)
    is_password_changed = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name
        


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_orders')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_orders')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_orders')

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'

    def __str__(self):
        return f'Ордер №{self.id}'