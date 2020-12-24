# Day 22: Crab Combat
import pytest

# Play the small crab in a game of Combat using the two decks you just dealt. What is the winning player's score?
def part1(data):
  (p1, p2) = parse(data)
  return None

def part2(data):
  return None

# Before the game starts, split the cards so each player has their own deck (your puzzle input). 
def parse(data):
  piles = data.split('\n\n')

  (p1, p2) = map(lambda p: list(map(int, p.split('\n')[1:])), piles)
  return (p1, p2)

# Then, the game consists of a series of rounds: both players draw their top card, and the player with the higher-valued card wins the round. The winner keeps both cards, placing them on the bottom of their own deck so that the winner's card is above the other card. If this causes a player to have all of the cards, they win, and the game ends.


def test_parse(example1):
  (p1, p2) = parse(example1)
  assert p1 == [9, 2, 6, 3, 1]
  assert p2 == [5, 8, 4, 7, 10]

def test_part1(example1):
  # -- Round 1 --
  # Player 1's deck: 9, 2, 6, 3, 1
  # Player 2's deck: 5, 8, 4, 7, 10
  # Player 1 plays: 9
  # Player 2 plays: 5
  # Player 1 wins the round!

  # -- Round 2 --
  # Player 1's deck: 2, 6, 3, 1, 9, 5
  # Player 2's deck: 8, 4, 7, 10
  # Player 1 plays: 2
  # Player 2 plays: 8
  # Player 2 wins the round!

  # -- Round 3 --
  # Player 1's deck: 6, 3, 1, 9, 5
  # Player 2's deck: 4, 7, 10, 8, 2
  # Player 1 plays: 6
  # Player 2 plays: 4
  # Player 1 wins the round!

  # -- Round 4 --
  # Player 1's deck: 3, 1, 9, 5, 6, 4
  # Player 2's deck: 7, 10, 8, 2
  # Player 1 plays: 3
  # Player 2 plays: 7
  # Player 2 wins the round!

  # -- Round 5 --
  # Player 1's deck: 1, 9, 5, 6, 4
  # Player 2's deck: 10, 8, 2, 7, 3
  # Player 1 plays: 1
  # Player 2 plays: 10
  # Player 2 wins the round!

  # ...several more rounds pass...

  # -- Round 27 --
  # Player 1's deck: 5, 4, 1
  # Player 2's deck: 8, 9, 7, 3, 2, 10, 6
  # Player 1 plays: 5
  # Player 2 plays: 8
  # Player 2 wins the round!

  # -- Round 28 --
  # Player 1's deck: 4, 1
  # Player 2's deck: 9, 7, 3, 2, 10, 6, 8, 5
  # Player 1 plays: 4
  # Player 2 plays: 9
  # Player 2 wins the round!

  # -- Round 29 --
  # Player 1's deck: 1
  # Player 2's deck: 7, 3, 2, 10, 6, 8, 5, 9, 4
  # Player 1 plays: 1
  # Player 2 plays: 7
  # Player 2 wins the round!


  # == Post-game results ==
  # Player 1's deck: 
  # Player 2's deck: 3, 2, 10, 6, 8, 5, 9, 4, 7, 1
  assert part1(example1) is None

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