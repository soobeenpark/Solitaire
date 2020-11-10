from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Basic user of our app"""
    city = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.username


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
    moves = models.IntegerField(default=0)  # Num moves made so far in game

    def __str__(self):
        return "Game number " + str(self.id)


class Move(models.Model):
    """Each move made by the client"""
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="moves")
    cards = models.ArrayField(CardField)
    src = models.CharField(max_length=100)
    dst = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        cards_in_move = ",".join(self.cards)
        return "[{cards}] from {self.src} to {self.dst}".format(
            cards=cards_in_move, self=self)


class KlondikeState(models.Model):
    """A state snapshot of an active/finished Klondyke game"""
    pile1 = models.ArrayField(CardField)
    pile2 = models.ArrayField(CardField)
    pile3 = models.ArrayField(CardField)
    pile4 = models.ArrayField(CardField)
    pile5 = models.ArrayField(CardField)
    pile6 = models.ArrayField(CardField)
    pile7 = models.ArrayField(CardField)
    stack1 = models.ArrayField(CardField)
    stack2 = models.ArrayField(CardField)
    stack3 = models.ArrayField(CardField)
    stack4 = models.ArrayField(CardField)
    discard = models.ArrayField(CardField)
    draw = models.ArrayField(CardField)


######################## Custom Fields ########################
class Card:
    """Card class that will be used for CardField"""

    def __init__(self, suit, value, up):
        self.suit = suit
        self.value = value
        self.up = up

    def __str__(self):
        up_str = "up" if self.up else "down"
        return "{self.suit} of {self.value} facing {up_str}".format(
            self=self, up_str=up_str)


def parse_card(card_str):
    """Takes a string representing a full card and returns a Card object.
    suit: A character representing the suit of the card
    card_str[1]: A character representing the value of the card
    card_str[2]: A character representing whether the card is face up or down"""

    if len(card_str) != 3:
        raise ValidationError(_("Invalid input for a for a Card instance"))

    # Get suit
    suit_char = card_str[0]
    if suit_char == 'c':
        suit = "Clubs"
    elif suit_char == 's':
        suit = "Spades"
    elif suit_char == 'd':
        suit = "Diamonds"
    else:
        if suit_char != 'h':
            raise ValidationError(
                _("Invalid input for a Card instance - no matching suit"))
        suit = "Hearts"

    # Get value
    value_char = card_str[1]
    if value_char == 'a':
        value = 1  # Ace
    elif value_char == 'j':
        value = 11  # Jack
    elif value_char == 'q':
        value = 12  # Queen
    elif value_char == 'k':
        value = 13  # King
    else:
        try:
            value = int(value_char)
        except ValueError:
            raise ValidationError(
                _("Invalid input for a Card instance - no matching value"))

    # Get up status
    up_char = card_str[2]
    if up_char != 'u' and up_char != 'd':
        raise ValidationError(
            _("Invalid input for a Card instance - not an appropriate up/down status"))
    up = up_char == 'u'  # True if 'u' (up), False if 'd' (down)

    return Card(suit=suit, value=value, up=up)


class CardField(models.Field):
    description = "A card used in the game of Solitaire"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 3
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]  # For readability
        return name, path, args, kwargs

    def get_interal_type(self):
        return "CharField"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return parse_card(value)

    def to_python(self, value):
        if isinstance(value, Card):
            return value
        if value is None:
            return value
        return parse_card(value)

    def get_prep_value(self, value):
        # Prepare suit
        ret_str = ""
        if value.suit == "Clubs":
            ret_str += "c"
        elif value.suit == "Spades":
            ret_str += "s"
        elif value.suit == "Diamonds":
            ret_str += "d"
        else:
            assert(value.suit == "Hearts")
            ret_str += "h"

        # Prepare value
        if value.value == 1:
            ret_str += "a"  # Ace
        elif value.value == 11:
            ret_str += "j"  # Jack
        elif value.value == 12:
            ret_str += "q"  # Queen
        elif value.value == 13:
            ret_str += "k"  # King
        else:
            ret_str += str(value.value)

        # Prepare up/down status
        if value.up:
            ret_str += "u"
        else:
            ret_str += "d"

        return ret_str

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
