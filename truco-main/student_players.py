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
        self._ORDER_NIPES = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        

    def _listIdx(self):
        order_c_idx = lambda x: self._ORDER_CARDS.index(x)
        order_n_idx = lambda x: self._ORDER_NIPES.index(x)


        idx_c1, idx_n1 = order_c_idx(self._hand_cards[0][0]), order_n_idx(self._hand_cards[0][1])
        idx_c2, idx_n2 = order_c_idx(self._hand_cards[1][0]), order_n_idx(self._hand_cards[1][1])
        idx_c3, idx_n3 = order_c_idx(self._hand_cards[2][0]), order_n_idx(self._hand_cards[2][1])
        
        cards_idx = [[idx_c1, idx_n1], [idx_c2, idx_n2], [idx_c3, idx_n3]]
        return cards_idx

    def thereIsManilha(self):
        found = False
        manilhas = []
        cards_idx = self._listIdx()
        
        for card, nipe in cards_idx:
            if card == 1 + self._ORDER_CARDS.index(self._top_card[0]):
                found = True
                manilha = (self._ORDER_CARDS[card], self._ORDER_NIPES[nipe])
                manilhas.append(manilha)
        
        return [found, manilhas]
    
    def sortCards(self):
        if len(self._hand_cards) < 3:
            return self._hand_cards
        
        cards_idx = self._listIdx()
        cards_idx.sort(key= lambda c: c[0], reverse=True)
        
        sorted_cards = [(self._ORDER_CARDS[cards_idx[0][0]], self._ORDER_NIPES[cards_idx[0][1]]), 
                        (self._ORDER_CARDS[cards_idx[1][0]], self._ORDER_NIPES[cards_idx[1][1]]),
                        (self._ORDER_CARDS[cards_idx[2][0]], self._ORDER_NIPES[cards_idx[2][1]])]
        return sorted_cards
    
class PlayersHand(CheckCards):
    def __init__(self, hand_cards, top_card):
        super().__init__(hand_cards, top_card)
        self._hand_cards = hand_cards
        self._manilhas = []

    def manilhas(self):
        if len(self._hand_cards) < 3:
            return len(self._manilhas) > 0 
           
        there_is_manilha = self.thereIsManilha()

        if not there_is_manilha[0]:
            return False

        self._manilhas = there_is_manilha[1]
        return True
    
    def use_manilha(self):
        return self._hand_cards.index(self._manilhas.pop())


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

        my_hand = self._checker_hand(self.cards, top_card)


        if my_hand.manilhas():
            pedir_truco = True if score_hist[-1][-1] == 1 else False
            idx_manilha = my_hand.use_manilha()
            return DECISAO['truco'] if pedir_truco else DECISAO['normal'], self.cards[idx_manilha]
        
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
