from enum import Enum
DEBUG = True
class Color(Enum):
    BLUE = 1
    RED = 2
    BLACK = 3
    YELLOW = 4
    GHOST = 5
class Error(Enum):
    success = 0
    cardNotFound = 1
    notValidCardSeq = 2
    notValidDataType = 3
class Card:
    cid = -1
    def __init__(self, color : Color, point : int):
        self.color = color
        self.point = point
        Card.cid += 1
        self.cid = Card.cid
    def __eq__(self, other):
        return (self.color == other.color and self.point == other.point)
    def __repr__(self):
        return(self.color.name + ' ' + str(self.point) + ' id:' + str(self.cid))
class Player:
    def __init__(self, uuid):
        self.cards = []
        self.uuid = uuid
        self.broke = False
class Table:
    def __init__(self):
        self.cards = []
def generateCards():
    """Generate a full deck in a list."""
    #Generate normal cards.
    CARDS = [Card(color, point) for color in Color if color != Color.GHOST for point in list(range(1, 14)) * 2]
    #Generate ghost cards.
    CARDS.append(Card(Color.GHOST, 1))
    CARDS.append(Card(Color.GHOST, 2))
    return CARDS
def isValidCardSequence(cardSeq):
    """Check if a card sequence is valid."""
    #Ensure at least 3 cards are in a sequence.
    if(len(cardSeq) < 3): return False
    cardSeq.sort(key = lambda card: card.point)
    #First, check if it's a valid group.
    colorSet = set()
    validGroup = True
    for card in cardSeq:
        if(card.color in colorSet):
            validGroup = False
            break
        colorSet.add(card.color)
    if(validGroup): return True
    #If it's not a valid group, check if it's a valid run.
    #Color in a run should be same.
    colorSet = set(map(lambda card: card.color, cardSeq))
    if(len(colorSet) > 1): return False
    #And the point should be continous.
    point = cardSeq[0].point
    for card in cardSeq:
        if(card.point != point): return False
        point += 1
    return True