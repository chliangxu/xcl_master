# 一张牌
class Card:
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['梅花', '方片', '红桃', '黑桃']

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank  # 牌面值
        self.suit = suit  # 花色
        self.is_face_up = face_up

    def __str__(self):  # 重写print()方法，打印一张牌的信息
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = 'XX'
        return rep

    def flip(self):  # 翻牌方法
        self.is_face_up = not self.is_face_up

    def get_name(self):
        if self.suit.__contains__('A'):
            return int(11)
        elif self.suit.__contains__("J") or self.suit.__contains__("Q") or self.suit.__contains__("K"):
            return int(10)
        else:
            return int(self.suit)


# 一手牌
class Hand:

    def __init__(self):
        self.cards = []  # cards列表变量存储牌手手里的牌

    def __str__(self):  # 重写print()方法，打印出牌手的所有牌
        if self.cards:
            rep = ''
            for card in self.cards:
                rep += str(card) + str(card.get_name()) + "\t"
        else:
            rep = '无牌'
        return rep

    # 返回每张牌的牌面值
    def compare(self):
        if self.cards:
            i = 0
            ret = 0
            for card1 in self.cards:
                ret += card1.get_name()
                i += 1
            return ret

    def clear(self):  # 清空手里的牌
        self.cards = []

    def add(self, card):  # 增加手里的牌
        self.cards.append(card)


# 一副牌
class Poke(Hand):

    # 一副牌
    def popul(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(suit, rank))

    # 随机发牌
    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand):  # 将牌发给玩家，每人默认2张牌
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.cards.remove(top_card)
                    hand.add(top_card)
                    # self.give(top_card,hand) #上两句可以用此句替换
                else:
                    print('不能继续发牌了，牌已经发完了!')


if __name__ == '__main__':
    # print('This is a module with classes for playing cards.')
    players = [Hand(), Hand(), Hand()]
    poke1 = Poke()
    poke1.popul()
    poke1.shuffle()
    poke1.deal(players, 2)  # 发给每人2张牌
    n = 0
    for hand in players:
        if n == 0:
            print("荷官\t ", end=":")
            ret1 = hand.compare()
            print("点数为%d：" % ret1)
            print(hand)

        else:
            print('牌手', n, end=':')
            ret2 = hand.compare()
            print("点数为%d：" % ret2)
            print(hand)
        n = n + 1
    if ret1 > ret2:
        print("荷官赢")
    elif ret1 < ret2:
        print("牌手%d赢" % (n - 1))
    else:
        print("打平")
