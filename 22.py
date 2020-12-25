# Day 22: Crab Combat
import pytest
from itertools import starmap

# Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score?
def part1(data):
  (d1, d2) = parse(data)
  while len(d1) and len(d2):
    (d1, d2) = play_round((d1, d2))
  score = winning_score(d1+d2)
  return score

# Defend your honor as Raft Captain by playing the small crab in a game of Recursive Combat using the same two decks as before. What is the winning player's score?
def part2(data):
  decks = parse(data)
  [winner, d1, d2] = play_recursive_game(decks)
  score = winning_score(d1+d2)
  return score
  # 30037 too low
  # 33006 too low
  # Output: 36621
  # Took 1m 24s 392ms 165µs

# Before the game starts, split the cards so each player has their own deck (your puzzle input). 
def parse(data):
  piles = data.split('\n\n')
  (p1, p2) = map(lambda p: list(map(int, p.split('\n')[1:])), piles)
  return (p1, p2)

# Then, the game consists of a series of rounds: both players draw their top card, and the player with the higher-valued card wins the round. The winner keeps both cards, placing them on the bottom of their own deck so that the winner's card is above the other card. If this causes a player to have all of the cards, they win, and the game ends.
def play_round(decks):
  (d1, d2) = decks
  if len(d1) == 0 or len(d2) == 0:
    raise Exception(f'Cannot play round with an empty deck ({d1, d2})')
  c1, c2 = d1.pop(0), d2.pop(0)
  if c1 > c2:
    d1 += [c1, c2]
  elif c2 > c1:
    d2 += [c2, c1]
  else:
    raise Exception(f'Cards match ({c1, c2})')
  return (d1, d2)

def winning_score(deck):
  # Once the game ends, you can calculate the winning player's score. The bottom card in their deck is worth the value of the card multiplied by 1, the second-from-the-bottom card is worth the value of the card multiplied by 2, and so on. With 10 cards, the top card is worth the value on the card multiplied by 10.
  deck.reverse()
  score = sum(starmap(lambda i, v: (i+1) * v, enumerate(deck)))
  return score

def play_recursive_game(decks):
  # Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
  (d1, d2) = decks
  previous_hands = set()
  round = 1
  # print(f'round {round}: new game {d1} {d2} - {previous_hands}')

  while len(d1) and len(d2):
    chk = checksum(d1 + [0] + d2)
    if chk in previous_hands:
      # the game instantly ends in a win for player 1.
      # print(f'round {round}: instant win P1 - {d1}, {d2} - {previous_hands}')
      return [1, d1, d2]
    previous_hands.add(chk)

    (d1, d2) = play_recursive_round((d1, d2))
    round += 1
    # print(f'round {round}: - {d1}, {d2}')

  winner = 1 if len(d1) > 0 else 2
  # print(f'round {round}: recursive win P{winner} - {d1}, {d2}')
  return [winner, d1, d2]


def play_recursive_round(decks):
  (d1, d2) = decks
  if len(d1) == 0 or len(d2) == 0:
    raise Exception(f'Cannot play round with an empty deck ({d1, d2})')

  # Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
  c1, c2 = d1.pop(0), d2.pop(0)

  # If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
  if len(d1) >= c1 and len(d2) >= c2:
    # To play a sub-game of Recursive Combat, each player creates a new deck by making a copy of the next cards in their deck (the quantity of cards copied is equal to the number on the card they drew to trigger the sub-game). During this sub-game, the game that triggered it is on hold and completely unaffected; no cards are removed from players' decks to form the sub-game. (For example, if player 1 drew the 3 card, their deck in the sub-game would be copies of the next three cards in their deck.)
    [winner, rd1, rd2] = play_recursive_game((d1.copy()[:c1], d2.copy()[:c2]))
    if winner == 1:
      # P1 winner
      d1 += [c1, c2]
    elif winner == 2:
      # P2 winner
      d2 += [c2, c1]
    else:
      raise Exception(f'Recursive Game Failed ({rd1, rd2})')

  # Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.
  else: 
    if c1 > c2:
      # P1 winner
      d1 += [c1, c2]
    elif c2 > c1:
      # P2 winner
      d2 += [c2, c1]
    else:
      raise Exception(f'Cards match ({c1, c2})')

  return (d1, d2)

def checksum(lst):
  chk = 0
  for n in lst:
    chk *= 13
    chk += n
    chk %= 65521
  return chk
  




def test_parse(example1):
  (p1, p2) = parse(example1)
  assert p1 == [9, 2, 6, 3, 1]
  assert p2 == [5, 8, 4, 7, 10]

def test_play_round(example1):
  decks = parse(example1)
  # -- Round 1 --
  # Player 1's deck: 9, 2, 6, 3, 1
  # Player 2's deck: 5, 8, 4, 7, 10
  # Player 1 plays: 9
  # Player 2 plays: 5
  # Player 1 wins the round!

  decks = play_round(decks)
  assert decks == ([2, 6, 3, 1, 9, 5], [8, 4, 7, 10])
  # -- Round 2 --
  # Player 1's deck: 2, 6, 3, 1, 9, 5
  # Player 2's deck: 8, 4, 7, 10
  # Player 1 plays: 2
  # Player 2 plays: 8
  # Player 2 wins the round!

  decks = play_round(decks)
  assert decks == ([6, 3, 1, 9, 5], [4, 7, 10, 8, 2])
  # -- Round 3 --
  # Player 1's deck: 6, 3, 1, 9, 5
  # Player 2's deck: 4, 7, 10, 8, 2
  # Player 1 plays: 6
  # Player 2 plays: 4
  # Player 1 wins the round!

  decks = play_round(decks)
  assert decks == ([3, 1, 9, 5, 6, 4], [7, 10, 8, 2])
  # -- Round 4 --
  # Player 1's deck: 3, 1, 9, 5, 6, 4
  # Player 2's deck: 7, 10, 8, 2
  # Player 1 plays: 3
  # Player 2 plays: 7
  # Player 2 wins the round!

  decks = play_round(decks)
  assert decks == ([1, 9, 5, 6, 4], [10, 8, 2, 7, 3])
  # -- Round 5 --
  # Player 1's deck: 1, 9, 5, 6, 4
  # Player 2's deck: 10, 8, 2, 7, 3
  # Player 1 plays: 1
  # Player 2 plays: 10
  # Player 2 wins the round!

  # ...several more rounds pass...

  for _ in range(27 - 5):
    decks = play_round(decks)
    
  assert decks == ([5, 4, 1], [8, 9, 7, 3, 2, 10, 6])
  # -- Round 27 --
  # Player 1's deck: 5, 4, 1
  # Player 2's deck: 8, 9, 7, 3, 2, 10, 6
  # Player 1 plays: 5
  # Player 2 plays: 8
  # Player 2 wins the round!

  decks = play_round(decks)
  assert decks == ([4, 1], [9, 7, 3, 2, 10, 6, 8, 5])
  # -- Round 28 --
  # Player 1's deck: 4, 1
  # Player 2's deck: 9, 7, 3, 2, 10, 6, 8, 5
  # Player 1 plays: 4
  # Player 2 plays: 9
  # Player 2 wins the round!

  decks = play_round(decks)
  assert decks == ([1], [7, 3, 2, 10, 6, 8, 5, 9, 4])
  # -- Round 29 --
  # Player 1's deck: 1
  # Player 2's deck: 7, 3, 2, 10, 6, 8, 5, 9, 4
  # Player 1 plays: 1
  # Player 2 plays: 7
  # Player 2 wins the round!

  decks = play_round(decks)
  assert decks == ([], [3, 2, 10, 6, 8, 5, 9, 4, 7, 1])
  # == Post-game results ==
  # Player 1's deck: 
  # Player 2's deck: 3, 2, 10, 6, 8, 5, 9, 4, 7, 1

def test_winning_score():
  assert winning_score([3, 2, 10, 6, 8, 5, 9, 4, 7, 1]) == 306

def test_part1(example1):
  assert part1(example1) == 306

def test_part2(example1):
  # After the game, the winning player's score is calculated from the cards they have in their original deck using the same rules as regular Combat. In the above game, the winning player's score is 291.
  assert part2(example1) == 291

def test_checksum():
  assert checksum([2, 10, 6, 8, 5, 9, 4, 7, 1, 3]) != checksum([6, 8, 5, 9, 4, 7, 1, 3, 2, 10])

  checksums = []
  deck = [3, 2, 10, 6, 8, 5, 9, 4, 7, 1]
  for _ in range(len(deck)):
    checksums.append(checksum(deck))
    deck = deck[1:] + deck[0:1]

  assert sorted(checksums) == sorted(list(set(checksums)))


@pytest.fixture
def example1():
  return """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""