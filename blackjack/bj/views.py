from django.shortcuts import render

from . import bj

# Create your views here.

def card_path(cards):
    path = []
    for card in cards:
        path.append(str(card[1]) + str(card[0]) + '.png')
    return path


def game(request):
    
    if request.method == 'GET' or 'restart' in request.POST:
        game_flag = False
        player_turn = True
        deck = bj.Deck()
        player = bj.Player()
        dealer = bj.Player()
        
        player.cards = [deck.emission(), deck.emission()]
        dealer.cards = [deck.emission(), deck.emission()]
        
        request.session['deck'] = deck
        request.session['player'] = player
        request.session['dealer'] = dealer
        request.session['player_turn'] = player_turn
        request.session['game_flag'] = game_flag
        
        d = {
            'message':'はじめましょう',
            'dealer_card':['u0.png','u0.png'],
            'player_card':['u0.png','u0.png'],
            'dealer_point':0,
            'player_point':0,
        }
        
        return render(request, 'game.html', d)
    
    elif request.method == 'POST':
        game_flag = request.session['game_flag']
        player_turn = request.session['player_turn']
        
        deck = request.session['deck']
        player = request.session['player']
        dealer = request.session['dealer']
        
        if 'hit' in request.POST:
            player.draw(deck.emission())
        elif 'stand' in request.POST:
            player_turn = False
        
        if bj.count_card(player.cards) > 21:
            game_flag = True
        
        elif bj.count_card(dealer.cards) > 16 and player_turn == False:
            game_flag = True
        
        if not game_flag:
            if player_turn:
                player_point = bj.count_card(player.cards)
                dealer_point = bj.str_point(dealer.cards[0])
                
                dealer_close = [[''], ['0','u']]
                dealer_close[0] = dealer.cards[0]
                
                if player_point ==21:
                    player_turn = False
                    
                    request.session['deck'] = deck
                    request.session['player'] = player
                    request.session['dealer'] = dealer
                    request.session['player_turn'] = player_turn
                    request.session['game_flag'] = game_flag
                    
                    d = {
                        'message':'BJ!',
                        'dealer_card':card_path(dealer_close),
                        'player_card':card_path(player.cards),
                        'dealer_point':dealer_point,
                        'player_point':player_point,
                        'turn':player_turn,
                        'flag':game_flag,
                    }
                    
                    return render(request, 'game.html', d)
                    
                else:
                    
                    request.session['deck'] = deck
                    request.session['player'] = player
                    request.session['dealer'] = dealer
                    request.session['player_turn'] = player_turn
                    request.session['game_flag'] = game_flag
                    
                    d = {
                        'message':'カードを引きますか？',
                        'dealer_card':card_path(dealer_close),
                        'player_card':card_path(player.cards),
                        'dealer_point':dealer_point,
                        'player_point':player_point,
                        'turn':player_turn,
                        'flag':game_flag,
                    }
                    
                    return render(request, 'game.html', d)
                
            else:
                player_point = bj.count_card(player.cards)
                dealer_point = bj.count_card(dealer.cards)
                
                dealer.draw(deck.emission())
                
                request.session['deck'] = deck
                request.session['player'] = player
                request.session['dealer'] = dealer
                request.session['player_turn'] = player_turn
                request.session['game_flag'] = game_flag
                    
                d = {
                    'message':'ディーラーがカードを引きました',
                    'dealer_card':card_path(dealer.cards),
                    'player_card':card_path(player.cards),
                    'dealer_point':dealer_point,
                    'player_point':player_point,
                    'turn':player_turn,
                    'flag':game_flag,
                }
                
                return render(request, 'game.html', d)
        
        else:
            player_point = bj.count_card(player.cards)
            dealer_point = bj.count_card(dealer.cards)
            
            player_turn = False
            game_flag = True
            
            
            if player_point > 21:
                win = 0
                msg = 'あなたの負けです'
            elif dealer_point > 21:
                win = 2
                msg = 'あなたの勝ちです！'
            elif player_point == dealer_point:
                win = 1
                msg = '引き分けです'
            elif player_point < dealer_point:
                win = 0
                msg = 'あなたの負けです'
            else:
                win = 2
                msg = 'あなたの勝ちです！'
            
            d = {
                'message': msg,
                'dealer_card':card_path(dealer.cards),
                'player_card':card_path(player.cards),
                'dealer_point':dealer_point,
                'player_point':player_point,
                'turn':player_turn,
                'flag':game_flag,
            }
            
            return render(request, 'game.html', d)