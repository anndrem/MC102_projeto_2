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
        self.hand_cards = hand_cards
        self.top_card = top_card
        self.ORDER_CARDS = ['4' ,'5' ,'6' ,'7' ,'Q' ,'J' ,'K' ,'A' ,'2' ,'3']
        self.ORDER_NIPES = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        

    def _listIdx(self):
        idx_c1, idx_n1 = self.ORDER_CARDS.index(self.hand_cards[0][0]), self.ORDER_NIPES.index(self.hand_cards[0][1])
        idx_c2, idx_n2 = self.ORDER_CARDS.index(self.hand_cards[1][0]), self.ORDER_NIPES.index(self.hand_cards[1][1])
        idx_c3, idx_n3 = self.ORDER_CARDS.index(self.hand_cards[2][0]), self.ORDER_NIPES.index(self.hand_cards[2][1])
        
        cards_idx = [[idx_c1, idx_n1], [idx_c2, idx_n2], [idx_c3, idx_n3]]
        return cards_idx

    def theresIsManilha(self):
        idx = False
        my_manilhas = []
        cards_idx = self._listIdx()
        
        for card, nipe in cards_idx:
            if card == self.ORDER_CARDS.index(self.top_card[0]) + 1:
                idx = self.hand_cards.index((self.ORDER_CARDS[card], self.ORDER_NIPES[nipe]))
                my_manilhas.append(idx)

        return [True, my_manilhas] if idx != -1 else [False, [-1]]
    
    def sortCards(self):
        if len(self.hand_cards) < 3:
            return None
        
        cards_idx = self._listIdx()
        cards_idx.sort(key= lambda x: x[0], reverse=True)
        
        sorted_cards = [(self.ORDER_CARDS[cards_idx[0][0]], self.ORDER_NIPES[cards_idx[0][1]]), 
                        (self.ORDER_CARDS[cards_idx[1][0]], self.ORDER_NIPES[cards_idx[1][1]]),
                        (self.ORDER_CARDS[cards_idx[2][0]], self.ORDER_NIPES[cards_idx[2][1]])]
        
        return sorted_cards

class SmartPlayer(Player):
    def __init__(self, ra, name):
        super().__init__(ra, name) 
        self._respond = RESPOSTA['aceitar']
        self._manilha = [False,[-1]]
        self.my_manilhas = []
        self._CheckCards = CheckCards

    '''O JOGO ESTA DEFINIDO AQUI'''
    def play(self, top_card, play_hist, score_hist):
        player_checker = self._CheckCards(self.cards, top_card)

        if len(self.cards) == 3:
            self.cards = player_checker.sortCards()
            self._manilha = player_checker.theresIsManilha()
            self.my_manilhas = self._manilha[1]

        if len(self.my_manilhas) == 0:
            self._manilha[0] = False
        else: 
            self._manilha[0] = True

        # TODO: arrumar o (index out of range) da manilha - acontece quando temos mais de uma manilha que carrega o index antigo da carta 
        # (sugestao: ao inves de usar o index, salvar a propria manilha como carta e depois procurar o index)
        if self._manilha[1]:
            pedir_truco = True if score_hist[-1][-1] == 1 else False
            idx_manilha = self.my_manilhas[-1]
            self.my_manilhas.pop()
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
