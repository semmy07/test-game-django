# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View

from .forms import GameForm
from .models import GameResult


class GameView(View):
    form_class = GameForm
    template_name = 'test_game.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            board = ' '.join(board for board in request.POST.get('board', '')).split(' ')
            cards = request.POST.get('cards', '')
            cards = cards.replace(' ', '')
            cards = ' '.join(c.replace('\u200b', '').replace('\u200b', '') for c in cards.split(',')).split(' ')

            players = request.POST.get('players', '')
            end_game = len(board)

            d_players = {}
            for player in range(int(players)):
                d_players[int(player) + 1] = 0

            count = 0

            player = 1
            for card in cards:
                if player > int(players):
                    player = 1
                count += 1
                try:
                    player_position = d_players[player]

                    if len(str(card)) == 2:
                        index = board[player_position::].index(card[0]) + player_position
                        index += board[index+1::].index(card[0]) + 1 + player_position
                    else:
                        index = board[player_position::].index(card) + 1 + player_position
                    d_players[player] = index

                    if d_players[player] >= end_game:
                        self.add_to_db(request.POST.get('board', ''), request.POST.get('cards', ''),
                                       request.POST.get('players', ''), player, count)
                        return render(request, self.template_name, {'message':
                                                                    f'Player {player} won after {count} cards'})
                    player += 1
                except ValueError:
                    self.add_to_db(request.POST.get('board', ''), request.POST.get('cards', ''),
                                   request.POST.get('players', ''), player, count)
                    return render(request, self.template_name, {'message':
                                                                f'Player {player} won after {count} cards WITH ERROR'})

            self.add_to_db(request.POST.get('board', ''), request.POST.get('cards', ''),
                           request.POST.get('players', ''), 0, count)
            return render(request, self.template_name, {'message': f'No one won after {count} cards'})

        return render(request, self.template_name, {'message': 'Form is invalid!'})

    def add_to_db(self, board, cards, players, winner, count_cards_to_win):
        result = GameResult(board=board, cards=str(cards), players=int(players), winner=winner,
                            count_cards_to_win=count_cards_to_win)
        result.save()
