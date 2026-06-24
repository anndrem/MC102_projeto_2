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

def sortCards(cards):
    c1, n1 = cards[0][0], cards[0][1]
    c2, n2 = cards[1][0], cards[1][1]
    c3, n1 = cards[2][0], cards[2][1]

    return c1, n1


class SmartPlayer(Player):
    def __init__(self, ra, name):
        super().__init__(ra, name) 

        self._respond = RESPOSTA['aceitar']

    def theresManilha(self, cards, top_card):
        manilhas = {}   
        
        idx_c1, idx_n1 = ORDER_CARDS.index(cards[0][0]), ORDER_NIPES.index(cards[0][1])
        idx_c2, idx_n2 = ORDER_CARDS.index(cards[1][0]), ORDER_NIPES.index(cards[1][1])
        idx_c3, idx_n3 = ORDER_CARDS.index(cards[2][0]), ORDER_NIPES.index(cards[2][1])

        for key, value in {idx_c1: idx_n1, idx_c2: idx_n2, idx_c3: idx_n3}.items():
            if key == ORDER_CARDS.index(top_card[0]) + 1:
                manilhas[ORDER_CARDS[key]] = ORDER_NIPES[value]

        return True if len(manilhas) else False
    def sortCards(self, cards, top_card = None):
        if len(cards) < 3:
            return None
        
        c1, n1 = cards[0][0], cards[0][1]
        c2, n2 = cards[1][0], cards[1][1]
        c3, n3 = cards[2][0], cards[2][1]
        
        player_cards = {c1: n1, c2: n2, c3: n3}

        idx_c1 = ORDER_CARDS.index(cards[0][0])
        idx_c2 = ORDER_CARDS.index(cards[1][0])
        idx_c3 = ORDER_CARDS.index(cards[2][0])

        verification_idx = [idx_c1, idx_c2, idx_c3]
        
        idx_best_card = max(verification_idx)
        verification_idx.remove(idx_best_card)

        idx_worst_card = min(verification_idx)
        verification_idx.remove(idx_worst_card)
        
        best_card = ORDER_CARDS[idx_best_card]
        mid_card = ORDER_CARDS[verification_idx[0]]
        worst_card = ORDER_CARDS[idx_worst_card]
        
        # basic_sort = [best_card, mid_card, worst_card]
        # changes_cards = basic_sort.copy()

        # if len(manilhas) >= 0:
        #     for i in range(len(manilhas)):
        #         if basic_sort[i] != manilhas[i]:
        #             changes_cards[changes_cards.index(manilhas[i])] = basic_sort[i]
        #             basic_sort[i] = manilhas[i]

        # print(f'basic = {basic_sort}')
        # print(f'change = {changes_cards}')
        print(f'manilhas em mao: {manilhas}')
        sorted_cards = [(best_card, player_cards[best_card]), (mid_card, player_cards[mid_card]), (worst_card, player_cards[worst_card])]
        return sorted_cards

    '''O JOGO ESTA DEFINIDO AQUI'''
    def play(self, top_card, play_hist, score_hist):

        if len(self.cards) == 3:
            print(f'vira: {top_card}')
            print(f'old cards: {self.cards}')
            sorted_cards = self.sortCards(self.cards, top_card)

        if self._cards:
            return DECISAO['normal'], self._cards[0]
            
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
