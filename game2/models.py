from django.db import models
from django.utils import timezone
import csv
class Player(models.Model):
    player_id = models.CharField(max_length=100)
    def take_a_prize(self, prize):
        print( f"Player with id {self.player_id} take a {prize.title}")
    def csv_dump(self):
        headers = ["ID", "level_title", "is_completed", "prize"]
        with open(f"{self.player_id}_stats.csv", mode='w', encoding='utf-8') as file:
            file_writer = csv.DictWriter(file, delimiter=",", fieldnames=headers)
            file_writer.writeheader()
            for player_level in self.player.all().select_related('level'):
                for prize in player_level.level.prize_level.all().select_related('prize'):
                    file_writer.writerow({"ID": self.player_id,
                                          "level_title": player_level.level.title,
                                         "is_completed": player_level.is_completed,
                                          "prize": prize.prize.title})
class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

class Prize(models.Model):
    title = models.CharField(max_length=30)

class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='player_level')
    completed = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    def complete_level(self):
        self.completed = timezone.now()
        self.is_completed = True
        level_prize = self.level.prize_level.all()
        for entry in level_prize:
            self.player.take_a_prize(entry.prize)
            entry.received = timezone.now()
            entry.save()
        self.save()

class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='prize_level')
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, related_name='prize')
    received = models.DateField(blank=True, null=True)




