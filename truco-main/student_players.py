### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    André de Almeida Maximiano 
# RA #01 (quem entregou o código):      306387
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]
from basic_players import Player

DECISAO = {'encoberta': 0, 'normal': 1, 'truco': 2}
RESPOSTA = {'correr': 0, 'aceitar': 1, 'aumentar': 2}

ORDER_CARDS = ['4' ,'5' ,'6' ,'7' ,'Q' ,'J' ,'K' ,'A' ,'2' ,'3']
ORDER_NIPES = ['Diamonds', 'Spades', 'Hearts', 'Clubs']

class SmartPlayer(Player):
    
    def __init__(self, ra, name):
        super().__init__(ra, name) 
        self._respond = RESPOSTA['aceitar']

    def _theresManilha(self,top_card):
        manilhas = {}   
        idx = -1

        idx_c1, idx_n1 = ORDER_CARDS.index(self.cards[0][0]), ORDER_NIPES.index(self.cards[0][1])
        idx_c2, idx_n2 = ORDER_CARDS.index(self.cards[1][0]), ORDER_NIPES.index(self.cards[1][1])
        idx_c3, idx_n3 = ORDER_CARDS.index(self.cards[2][0]), ORDER_NIPES.index(self.cards[2][1])

        for key, value in [[idx_c1, idx_n1], [idx_c2, idx_n2], [idx_c3, idx_n3]]:
            if key == ORDER_CARDS.index(top_card[0]) + 1:
                idx = self.cards.index((ORDER_CARDS[key], ORDER_NIPES[value]))
                manilhas[ORDER_CARDS[key]] = ORDER_NIPES[value]


        return (True, idx) if idx != -1 else (False, -1)
    
    def _sortCards(self):
        if len(self.cards) < 3:
            return None
        
        idx_c1, idx_n1 = ORDER_CARDS.index(self.cards[0][0]), ORDER_NIPES.index(self.cards[0][1])
        idx_c2, idx_n2 = ORDER_CARDS.index(self.cards[1][0]), ORDER_NIPES.index(self.cards[1][1])
        idx_c3, idx_n3 = ORDER_CARDS.index(self.cards[2][0]), ORDER_NIPES.index(self.cards[2][1])

        verification_idx = [[idx_c1, idx_n1], [idx_c2, idx_n2], [idx_c3, idx_n3]]
        verification_idx.sort(key= lambda x: x[0], reverse=True)
        
        sorted_cards = [(ORDER_CARDS[verification_idx[0][0]], ORDER_NIPES[verification_idx[0][1]]), (ORDER_CARDS[verification_idx[1][0]], ORDER_NIPES[verification_idx[1][1]]), (ORDER_CARDS[verification_idx[2][0]], ORDER_NIPES[verification_idx[2][1]])]
        return sorted_cards

    '''O JOGO ESTA DEFINIDO AQUI'''
    def play(self, top_card, play_hist, score_hist):
        
        manilha = (False, -1)
        if len(self.cards) == 3:
            # print(f'CARTAS NAO ORDENADAS:\n--{self.name}: {self.cards}')
            manilha = self._theresManilha(top_card)
            self.cards = self._sortCards()
            # print(f'CARTAS ORDENADAS:\n--{self.name}: {self.cards}')


        if manilha[0]:
            idx_manilha = manilha[1]
            print(f'JOGANDO MANILHA:\n--vira{top_card}: {self.cards[idx_manilha]}')
            return DECISAO['normal'], self.cards[idx_manilha]
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
