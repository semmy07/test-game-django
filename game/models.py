# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class GameResult(models.Model):
    board = models.CharField(max_length=128, default='')
    cards = models.CharField(max_length=1024, default='')
    players = models.IntegerField()
    winner = models.IntegerField()
    count_cards_to_win = models.IntegerField()
