### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    André de Almeida Maximiano 
# RA #01 (quem entregou o código):      306387
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]
from basic_players import Player




DECISAO = {'encoberta': 0, 'normal': 1, 'truco': 2}
RESPOSTA = {'correr': 0, 'aceitar': 1, 'aumentar': 2}

class CheckCards():
    def __init__(self, hand_cards, top_card = None):
        self._hand_cards = hand_cards
        self._top_card = top_card
        self._ORDER_CARDS = ['4' ,'5' ,'6' ,'7' ,'Q' ,'J' ,'K' ,'A' ,'2' ,'3']
        self._ORDER_RANK = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        

    def _listIdx(self):
        order_c_idx = lambda x: self._ORDER_CARDS.index(x)
        order_r_idx = lambda x: self._ORDER_RANK.index(x)

        cards_idx = [
            (order_c_idx(card), order_r_idx(rank)) 
            for card, rank in self._hand_cards
            ]
        
        return cards_idx

    def thereIsTrump(self):
        found = False
        trumps = []
        cards_idx = self._listIdx()
        
        for card, rank in cards_idx:
            if card == 1 + self._ORDER_CARDS.index(self._top_card[0]):
                found = True
                trump = (self._ORDER_CARDS[card], self._ORDER_RANK[rank])
                trumps.append(trump)
        
        return (found, trumps)
    
    def sortCards(self):

        cards_idx = self._listIdx()
        cards_idx.sort(key= lambda c: c[0], reverse=True)
    
        sorted_cards = [
            (self._ORDER_CARDS[card] , self._ORDER_RANK[rank])
            for card, rank in cards_idx
        ]
    
        return sorted_cards
    
    def is_higher_than(self, oponent_card):
        cards_idx = self._listIdx()
        oponent_checker = CheckCards([oponent_card], self._top_card)
        oponent_trump = oponent_checker.thereIsTrump()

        found = False
        hihgers_idx = []
        hihgers = []

        oponent_card_idx = self._ORDER_CARDS.index(oponent_card[0])
        oponent_rank_idx = self._ORDER_RANK.index(oponent_card[1])
        
        for card, rank in cards_idx:
            if oponent_trump[0] and card == oponent_card_idx and rank > oponent_rank_idx:
                found = True
                hihgers_idx.append([card, rank])
            elif card > oponent_card_idx:
                found = True
                hihgers_idx.append([card, rank])
        
        if len(hihgers_idx) > 0:
            hihgers_idx.sort(key= lambda x: x[0])
            
            hihgers = [
                (self._ORDER_CARDS[card_idx], self._ORDER_RANK[rank_idx])
                for card_idx, rank_idx in hihgers_idx
            ]

        return (found, hihgers)
    
class PlayersHand(CheckCards):
    def __init__(self, position, hand_cards, top_card):
        super().__init__(hand_cards, top_card)
        self._position = position
        self._hand_cards = hand_cards
        self._trumps = []

    def trumps(self):
        if len(self._hand_cards) < 3:
            return len(self._trumps) > 0 
           
        there_is_trump = self.thereIsTrump()

        if not there_is_trump[0]:
            return False

        self._trumps = there_is_trump[1]
        return True
    
    def use_trump(self):
        return self._hand_cards.index(self._trumps.pop())

    def play_check(self, current_round):
        if len(current_round) == 0:
            # primeiro a jogar
            pass

        
        last_play = current_round[-1]
        last_position = last_play[0]    
        last_card = last_play[1]    
        last_decision = last_play[2]   
        
        if last_position % 2 == 0:
            there_is_higher = self.is_higher_than(last_card)
            if there_is_higher[0]:
                return True, there_is_higher[1][0]
            else:
                return False, self._hand_cards[-1]
            
        elif last_position == self._position: 
            return False, self._hand_cards[0]
        
        else:
            return False, self._hand_cards[0]


class SmartPlayer(Player):
    def __init__(self, ra, name):
        super().__init__(ra, name) 
        self._respond = RESPOSTA['aceitar']
        self._CheckCards = CheckCards
        self._checker_hand = PlayersHand
    
    def _start(self, top_card):
            player_checker = self._CheckCards(self.cards, top_card)
            self.cards = player_checker.sortCards()
       
    '''O JOGO ESTA DEFINIDO AQUI'''
    def play(self, top_card, play_hist, score_hist):
        if len(self.cards) == 3:
            self._start(top_card)

        current_round = play_hist[-1]

        my_hand = self._checker_hand(self.position, self.cards, top_card)


        if my_hand.trumps():
            call_truco = True if score_hist[-1][-1] == 1 else False
            idx_trump = my_hand.use_trump()
            return DECISAO['truco'] if call_truco else DECISAO['normal'], self.cards[idx_trump]

        if len(current_round) > 0:
            play_best = my_hand.play_check(current_round)
            idx_card = self.cards.index(play_best[1])
            return DECISAO['normal'], self.cards[idx_card]
                
        
        if self._cards:
            return DECISAO['normal'], self.cards[0]
            
        return 1, None

    def respond(self,top_card,play_hist, score_hist):
        current_score = score_hist[-1][-1]
        teams_score = score_hist[-1][-2]
        
        if current_score <= 9 and teams_score[0] <= 10 and teams_score[1] <= 10:
            self._respond = RESPOSTA['aumentar']

        return self._respond


def pair_name():
    return 'Butequeiros de CC' 


def create_pair():
    p1 = SmartPlayer(11, 'Stalin')
    p2 = SmartPlayer(12, 'Lenin')
    return (p1, p2)
