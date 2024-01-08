from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from random import random

import json

from .ai import minimax, alphabeta

DEPTH_EASY = 3
DEPTH_MEDIUM = 5
DEPTH_HARD = 6

@csrf_exempt
def make_move(request):
    state = json.loads(request.body)
    difficulty = state['difficulty']
    player = state['player']
    line_made = state['line_made']

    if difficulty == 'easy':
        _, move = minimax(state, DEPTH_EASY, player, line_made)
    elif difficulty == 'medium':
        _, move = alphabeta(state, DEPTH_MEDIUM, -100000, 100000, player, line_made)
    elif difficulty == 'hard':
        _, move = alphabeta(state, DEPTH_HARD, -100000, 100000, player, line_made)
    
    return JsonResponse({ 'move': move })