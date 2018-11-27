# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View

from .forms import GameForm


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
            print(cards)
            cards = cards.replace(' ', '')
            print(cards)
            cards = ' '.join(c.replace('\u200b', '').replace('\u200b', '') for c in cards.split(',')).split(' ')
            print(cards)

            players = request.POST.get('players', '')
            end_game = len(board)

            d_players = {}
            for player in range(int(players)):
                d_players[int(player) + 1] = 0

            count = 0

            player = 1
            for card in cards:
                # for player in range(int(players)):
                if player > int(players):
                    player = 1
                count += 1
                # try:
                player_position = d_players[player]

                if len(str(card)) == 2:
                    index = board[player_position::].index(card[0])
                    index += board[index::].index(card[0])
                else:
                    index = board[player_position::].index(card)
                d_players[player] = index

                if d_players[player] >= end_game:
                    return render(request, self.template_name, {'message': f'Player {player} wins after {count} cards'})
                player += 1
                # except ValueError:
                #     print("")
                #     return render(request, self.template_name, {'message': f'Player {player} wins after {count} cards WITH ERROR'})

            return render(request, self.template_name, {'message': f'No one wins after {count} cards'})

        return render(request, self.template_name, {'message': 'Form is invalid!'})

    def add_to_db(self):
        pass
