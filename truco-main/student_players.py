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
        self._ORDER_RANKS = ['Diamonds', 'Spades', 'Hearts', 'Clubs']
        

    def _listIdx(self):
        order_c_idx = lambda x: self._ORDER_CARDS.index(x)
        order_r_idx = lambda x: self._ORDER_RANKS.index(x)

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
                trump = (self._ORDER_CARDS[card], self._ORDER_RANKS[rank])
                trumps.append(trump)
        
        return (found, trumps)
    
    def sortCards(self):
        if len(self._hand_cards) < 2:
            return self._hand_cards

        cards_idx = self._listIdx()
        cards_idx.sort(key= lambda c: c[0], reverse=True)
    
        sorted_cards = [
            (self._ORDER_CARDS[card] , self._ORDER_RANKS[rank])
            for card, rank in cards_idx
        ]
    
        return sorted_cards
    
    def sortPlays(self, plays):
        self._hand_cards = self.sortCards()

        last_plays = {
            pos: card
            for pos, card, _ in plays
            if card is not None
        }

        sorted_plays = [
            (pos, card)
            for card in self._hand_cards
            for pos, player_card in last_plays.items()
            if player_card == card
        ]

        return sorted_plays
    
    def is_higher_than(self, oponent_card):
        cards_idx = self._listIdx()
        
        oponent_checker = CheckCards([oponent_card], self._top_card)
        oponent_trump = oponent_checker.thereIsTrump()
        
        my_trump = self.thereIsTrump()

        found = False
        hihgers_idx = []
        hihgers = []

        oponent_card_idx = self._ORDER_CARDS.index(oponent_card[0])
        oponent_rank_idx = self._ORDER_RANKS.index(oponent_card[1])
        
        for card, rank in cards_idx:
            if oponent_trump[0] and card == oponent_card_idx and rank > oponent_rank_idx:
                found = True
                hihgers_idx.append([card, rank])
            elif card > oponent_card_idx:
                found = True
                hihgers_idx.append([card, rank])
            elif my_trump[0]:
                found = True
                card_trump = self._ORDER_CARDS.index(my_trump[1][0][0])
                rank_trump = self._ORDER_RANKS.index(my_trump[1][0][1])
                hihgers_idx.append([card_trump, rank_trump])
        
        if len(hihgers_idx) > 0:
            hihgers_idx.sort(key= lambda x: x[0])
            
            hihgers = [
                (self._ORDER_CARDS[card_idx], self._ORDER_RANKS[rank_idx])
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
    
    def _round_plays(self, current_hand, id_round):
        current_round = []
        idx_round = [0,2,1]
        _round = idx_round.index(id_round)

        # current_hand funciona por mao
        slice_round = [0, 4, 8]
        current_round = current_hand[slice_round[_round]:]

        print(f'round : {_round + 1}')
        return current_round
    
    def play_check(self, _current_hand, id_round):
        stronger = False
        best_play_card = []
        current_round = self._round_plays(_current_hand, id_round)

        if len(current_round) < 1:
            # primeiro a jogar
            print('primeiro a jogar')
            return True, self._hand_cards[0]
        
        
        _last_cards = [
            card
            for _,card, _ in current_round
            if card is not None
        ]

        checkPlays = CheckCards(_last_cards)
        sorted_plays = checkPlays.sortPlays(current_round)

        winning_play =  sorted_plays[0]
        winning_position = winning_play[0]    
        winning_card = winning_play[1]    
        
        print(f'{winning_position}: {winning_card}')
        
        if winning_position == self._position: 
            stronger = False
            best_play_card = self._hand_cards[0]
            print(f'ganhei: {best_play_card}')
        elif winning_position % 2 == 1:
            stronger = False
            best_play_card = self._hand_cards[-1]
            print(f'descate: {best_play_card}')

        else:
            there_is_higher = self.is_higher_than(winning_card)
            print(f'posso? {there_is_higher}')
            if there_is_higher[0]:
                stronger = True
                best_play_card = there_is_higher[1][0]
                print(f'eu mato: {best_play_card}')
            else:
                stronger = False
                best_play_card = self._hand_cards[-1]
                print(f'to mal: {best_play_card}')


        return stronger, best_play_card

    def Good_Hand(self):
        best_cards = 0
        cont = 0
        good_cards = False
        
        for carta in self._hand_cards:
                if carta in self._trumps:
                   cont += 1
                   best_cards += 1                
                if carta not in self._trumps:
                    if self._ORDER_CARDS.index(carta[0]) >= 6:
                        cont +=1
                    if self._ORDER_CARDS.index(carta[0]) > 7:
                        best_cards +=1
        if cont ==3 or best_cards >=2:
            good_cards = True               
        
        return good_cards
        

class SmartPlayer(Player):
    def __init__(self, ra, name):
        super().__init__(ra, name) 
        self._respond = RESPOSTA['aceitar']
        self._CheckCards = CheckCards
        self._checker_hand = PlayersHand
    
    def _start(self, top_card):
            player_checker = self._CheckCards(self.cards, top_card)
            self.cards = player_checker.sortCards()
            player_hand = self._checker_hand(self._position,self.cards,top_card)
            self._good_hand = player_hand.Good_Hand()
            print(f'vira : {top_card}')

    def play(self, top_card, play_hist, score_hist):
        if not self._cards:
            return 1, None

        if len(self.cards) == 3:
            self._start(top_card)

        print(f'{self.name} : {self.cards}')
        my_hand = self._checker_hand(self.position, self.cards, top_card)

        current_hand = play_hist[-1]
        id_round = len(self.cards) % 3
        best_play = my_hand.play_check(current_hand, id_round)

        if my_hand.trumps():
            call_truco = True if score_hist[-1][-1] == 1 else False
            idx_trump = my_hand.use_trump()
            return DECISAO['truco'] if call_truco else DECISAO['normal'], self.cards[idx_trump]
        else:
            idx_card = self.cards.index(best_play[1])
            return DECISAO['normal'], self.cards[idx_card]
            
    def respond(self,top_card,play_hist, score_hist):
        current_score = score_hist[-1][-1]
        teams_score = score_hist[-1][-2]
        my_hand = self._checker_hand(self._position, self.cards, top_card)
        
        if teams_score[0] < 11:
            if teams_score[0] + current_score < 12:
                if self._good_hand:
                    return RESPOSTA['aumentar']
                if my_hand.trumps():
                    return RESPOSTA['aceitar']
                return RESPOSTA['correr']
            return RESPOSTA['aceitar']      
        
        return RESPOSTA['aceitar']


def pair_name():
    return 'Butequeiros de CC' 


def create_pair():
    p1 = SmartPlayer(11, 'Stalin')
    p2 = SmartPlayer(12, 'Lenin')
    return (p1, p2)
