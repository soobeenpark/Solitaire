from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from .fields import CardField


class User(AbstractUser):
    """Basic user of our app"""
    city = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.username


class KlondikeState(models.Model):
    """A state snapshot of an active/finished Klondyke game"""
    pile1 = ArrayField(CardField())
    pile2 = ArrayField(CardField())
    pile3 = ArrayField(CardField())
    pile4 = ArrayField(CardField())
    pile5 = ArrayField(CardField())
    pile6 = ArrayField(CardField())
    pile7 = ArrayField(CardField())
    stack1 = ArrayField(CardField())
    stack2 = ArrayField(CardField())
    stack3 = ArrayField(CardField())
    stack4 = ArrayField(CardField())
    discard = ArrayField(CardField())
    draw = ArrayField(CardField())


class Game(models.Model):
    """State of Solitaire game being played."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    state = models.OneToOneField(
        KlondikeState,
        on_delete=models.CASCADE)  # Store current state game
    active = models.BooleanField(default=True)
    color = models.CharField(max_length=50, default="red")
    draw_count = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    won = models.BooleanField(default=False)

    def __str__(self):
        return "Game number " + str(self.id)


class Move(models.Model):
    """Each move made by the client"""
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="moves")
    cards = ArrayField(CardField())
    src = models.CharField(max_length=100)
    dst = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        cards_in_move = ",".join(self.cards)
        return "[{cards}] from {self.src} to {self.dst}".format(
            cards=cards_in_move, self=self)


