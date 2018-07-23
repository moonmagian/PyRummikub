import gameDefine
import random
class Game:
    def __init__(self, *players):
        random.seed()
        self.table = []
        self.deck = gameDefine.generateCards()
        self.players = players[:]
        self.drawInitCards()
    def drawInitCards(self):
        for player in self.players:
            for i in range(1, 15):
                self.drawCard(player.uuid)
    def drawCard(self, uuid):
        """Draw a card from deck to uuid."""
        cardId = random.randint(0, len(self.deck) - 1)
        list(filter(lambda player: player.uuid == uuid, self.players))[0].cards.append(self.deck[cardId])
        del(self.deck[cardId])
    def isTableValid(self):
        for cardSeq in self.table:
            gameDefine.isValidCardSequence(cardSeq)
    def findCardWithCid(self, source: int):
        tempCard = None
        #Check card in deck.
        for i, card in enumerate(self.deck):
            if(card.cid == source):
                tempCard = card
        #check card in table
        for i, cardPile in enumerate(self.table):
            for j, card in enumerate(cardPile):
                if(card.cid == source): 
                    tempCard = card
        #check card in player's cards.
        for i, player in enumerate(self.players):
            for j, card in enumerate(player.cards):
                if(card.cid == source):
                    tempCard = card
        return tempCard 
    def moveCardWithCid(self, source: int, dest: list):
        """Move source card to dest list.(lower performance)"""
        tempCard = None
        #Check card in deck.
        for i, card in enumerate(self.deck):
            if(card.cid == source):
                tempCard = card
                del(self.deck[i])
        #check card in table
        for i, cardPile in enumerate(self.table):
            for j, card in enumerate(cardPile):
                if(card.cid == source): 
                    tempCard = card
                    del(self.table[i][j])
        #check card in player's cards.
        for i, player in enumerate(self.players):
            for j, card in enumerate(player.cards):
                if(card.cid == source):
                    tempCard = card
                    del(self.players[i][j])
        if(not tempCard):
            return (False, gameDefine.Error.cardNotFound)
        else:
            dest.append(tempCard)
            return (True, gameDefine.Error.success)
    def makeNewTableSequence(self, seq):
        """Create a new table sequence with given crad sequence. seq can be a list of cid or a list of card."""
        cardSeq = []
        for card in seq:
            if(type(card) == gameDefine.Card):
                cardSeq.append(self.findCardWithCid(card.cid))
            elif(type(card) == int):
                cardSeq.append(self.findCardWithCid(card))
            else:
                return (False, gameDefine.Error.notValidDataType)
        if(gameDefine.isValidCardSequence(cardSeq)):
            self.table.append([])
            for card in cardSeq:
                self.moveCardWithCid(card.cid, self.table[-1])
            return (True, gameDefine.Error.success)
        else:
            return (False, gameDefine.Error.notValidCardSeq)

def test():
    print('Testing game init.')
    game = Game(gameDefine.Player('1'), gameDefine.Player('2'))
    command = input('Test command:')
    while(command):
        command = command.split(' ')
        if(command[0] == 'printDeck' or command[0] == 'pd'):
            print(game.deck)
        if(command[0] == 'printPlayerCards' or command[0] == 'pc'):
            for player in game.players:
                print('playerId:' + player.uuid)
                print(player.cards)
        if(command[0] == 'printTable' or command[0] == 'pt'):
            for cardSeq in game.table:
                print(cardSeq)
        if(len(command) == 3 and (command[0] == 'giveCardToPlayer' or command[0] == 'g')):
            print('moving card')
            game.moveCardWithCid(int(command[1]), list(filter(lambda player: player.uuid == command[2], game.players))[0].cards)
        if(len(command) >= 2 and (command[0] == 'makeNewSequenceOnTable' or command[0] == 'm')):
            print('making new sequence on table')
            if(game.makeNewTableSequence([int(c) for c in command[1:]])[0]):
                print('success.')
            else:
                print('failed. Not valid sequence.')
        if(command[0] == '?' or command[0] == 'help'):
            print("""
            Rummikub Test Menu:
            (p)rint(d)eck: print current deck.
            (p)rintPlayer(c)ards: print all player's cards.
            (p)rint(t)able: print current table cards.
            (g)iveCardToPlayer [playerid]: give a card from deck to a player.
            (m)akeNewSequenceOnTable [cid1] [cid2] ...: generate a table card sequence from valid cids.
            """)
        command = input('Test command:')
if(__name__ == '__main__'):
    test()
