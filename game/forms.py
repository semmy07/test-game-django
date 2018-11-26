from django import forms


class GameForm(forms.Form):
    board = forms.CharField(label='Board', max_length=128)
    cards = forms.CharField(label='Cards', max_length=1024)
    players = forms.IntegerField()
