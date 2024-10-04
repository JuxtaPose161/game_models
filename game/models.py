from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

POINTS_FOR_JOIN = 100

class Boost(models.Model):
    title = models.CharField(max_length=30, db_index=True, unique=True)
    factor = models.FloatField()
def get_default_boost():
    # Выдача базового множителя опыта
    boost, created = Boost.objects.get_or_create(title='Default', factor=1.0)
    return boost
class Player(models.Model):


    username = models.CharField(max_length=30, db_index=True, unique=True)
    date_created = models.DateTimeField(default=timezone.localtime)
    date_joined = models.DateTimeField(default=timezone.now)
    is_joined_today = models.BooleanField(default=False)

    points = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    boost = models.ForeignKey('Boost', on_delete=models.SET_DEFAULT,
                              default=get_default_boost, related_name='boost')
    def new_day_start(self):
        self.is_joined_today = False
    def give_points_for_joining(self):
        # Начисление очков за регулярные посещения
        if self.is_joined_today is False:
            without_active = timezone.now() - self.date_joined
            if without_active.days < 2:
                self.points += int(POINTS_FOR_JOIN * self.boost.factor)
            self.is_joined_today = True

    def update_level(self):
        # В этом примере за каждые 1000 очков даётся уровень
        self.level = self.points//1000 + 1
        self.update_boost_for_level()

    def update_boost_for_level(self):
        # Обновление бустера с увеличением уровня
        if self.level >= 100:
            boost, created = Boost.objects.get_or_create(title='Legend', factor=2.0)
        elif self.level >= 25:
            boost, created = Boost.objects.get_or_create(title='Ultra', factor=1.5)
        elif self.level >= 10:
            boost, created = Boost.objects.get_or_create(title='Super', factor=1.25)
        else:
            boost = get_default_boost()
        self.boost = boost