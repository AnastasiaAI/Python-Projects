"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    score, pig_out = 0, False
    while num_rolls:
        die = dice()
        if die == 1:
            pig_out = True
        else:
            score += die
        num_rolls -= 1
    return (pig_out and 1) or score #If pig_out == True, and shortcircuits to last Tue val 1, else or will give first True val
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    return (score % 10) * (score // 10) % 10 + 1
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def is_swap(score0, score1):
    """Return whether the current player's score has a ones digit
    equal to the opponent's score's tens digit."""
    # BEGIN PROBLEM 4
    if score0 == 0 and score1 == 0:
        return False
    if score0 % 10 == score1 // 10:
        return True
    else:
        return False
    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence

#extra_turn_pl0 = True #you allowed an extra turn
#extra_turn_pl1 = True
#turn = 0
def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
#    turn_tracker = 0
#    global turn
    # BEGIN PROBLEM 5
#    if score0 == 0 and score1 == 0:
#        helper_turn(False, False, True)

#    def time_trot(turn, num_rolls, player):
#        global extra_turn_pl0
#        global extra_turn_pl1
        # turn gets tracked in the while loop
#        if player == 1:
#            if not extra_turn_pl0: # if other player got 2 extra turns but now it's other player,
#                extra_turn_pl0 = extra(extra_turn_pl0) #he gets extra in the future again
#            if turn % 8 == num_rolls and extra_turn_pl1:
#                player = other(player) #to give me extra turn
#                extra_turn_pl1 = extra(extra_turn_pl1) #to not give me 3rd extra turn
#        elif player == 0:
#            if not extra_turn_pl1:
#                extra_turn_pl1 = extra(extra_turn_pl1)
#            if turn % 8 == num_rolls and extra_turn_pl0:
#                player = other(player)
#                extra_turn_pl1 = extra()
#        extra_turn_pl0, extra_turn_pl1 = extra(extra_turn_pl0), extra(extra_turn_pl1)

#        def extra(extra_turn):
#            """Return 1 if extra turn just happened
#            """
#            return not extra_turn

    while score0 < goal and score1 < goal:
#        turn = helper_turn(0, True, scoe0, score1)
        if player == 1:
            num_rolls = strategy1(score1, score0)
#            print(num_rolls)
#            time_trot(turn, num_rolls, player) #to switch player, and then switch again --> 2 turns
            score1 += take_turn(num_rolls, score0, dice) # free_bacon is inside take_turn
            if is_swap(score1, score0):
                score1, score0 = score0, score1
        elif player == 0:
    #        print(strategy0(score0, score1))
            score0 += take_turn(strategy0(score0, score1), score1, dice)
            if is_swap(score0, score1):
                score1, score0 = score0, score1
        player = other(player)
    # END PROBLEM 5
    # BEGIN PROBLEM 6
        say = say(score0, score1)
    # END PROBLEM 6
    return score0, score1

#def helper_turn(check, add, score0, score1):
#    global turn
#    if score0 == 0 and score1 == 0:
#        turn = 1
#    if check: #to be used by strategy
#        return turn
#    elif add: #to be used by while loop in play
#        turn += 1
#        return turn






#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 18) # Player 0 gets 8 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 18
    Player 1 takes the lead by 12
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(11, 0)
    >>> f2 = f1(11, 9)
    9 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 9)
    >>> f4 = f3(12, 20) # Player 1 gets 3 points, then Swine Swap applies
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f5 = f4(20, 32) # Player 0 gets 20 points, then Swine Swap applies
    12 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 42) # Player 1 gets 10 points; not enough for a new high
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def gain(score0, score1):
        if who == 0:
            current_score = score0
        else:
            current_score = score1
        gain = current_score - previous_score
        highest_gain = previous_high
        if gain > highest_gain:
            highest_gain = gain #i.e. "current gain is now the highest"
            print(highest_gain, "point(s)! That's the biggest gain yet for Player", who)
        return announce_highest(who, highest_gain, current_score)
    return gain
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(fn, num_samples=10000):
    """Return a function that returns the average value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def repeat_and_average(*args):
        total = 0
        for i in range (0, num_samples):
            total += fn(*args)
        return total/num_samples
    return repeat_and_average
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=10000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    max_score, number_of_dice, best_dice = 0, 1, 0
    while number_of_dice <= 10:
        score = make_averaged(roll_dice, num_samples)(number_of_dice, dice)
#        print("num_rolls:", number_of_dice, "av_score: ", score)
        if score > max_score:
            best_dice, max_score = number_of_dice, score
        number_of_dice += 1
    return best_dice
    # END PROBLEM 9
#>>> max_scoring_num_rolls()
#num_rolls: 1 av_score:  3.49535
#num_rolls: 2 av_score:  5.85743
#num_rolls: 3 av_score:  7.32991
#num_rolls: 4 av_score:  8.25496
#num_rolls: 5 av_score:  8.59808
#num_rolls: 6 av_score:  8.64769
#num_rolls: 7 av_score:  8.55689
#num_rolls: 8 av_score:  8.11398
#num_rolls: 9 av_score:  7.77904
#num_rolls: 10 av_score:  7.33997

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('my_bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('my_swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score) >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10

def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS. ********BAD_PART: "It also returns 0 if rolling 0 would give at least margin points,
    even if this would cause a non-beneficial swap."
    """
    # BEGIN PROBLEM 11
    if score < opponent_score and is_swap(score + free_bacon(opponent_score), opponent_score):
            return 0
    else:
        return bacon_strategy(score, opponent_score, margin, num_rolls)
    # END PROBLEM 11

###***      ____MY BACON LISTS____      ***###
ls_10 =[19, 33, 77, 91] #from Excel :)
ls_9 = [18, 24, 29, 36, 42, 47, 63, 68, 74, 81, 86, 92]
ls_8 = [17, 39, 71, 93]
ls_7 = [16, 23, 28, 32, 44, 49, 61, 66, 78, 82, 87, 94]
ls_6 = [16, 35, 51, 53, 55, 57, 59, 75, 95]
ls_5 = [14, 22, 27, 38, 41, 46, 64, 69, 72, 83, 88, 96]
ls_4 = [13, 31, 79, 97]
ls_3 = [12, 21, 26, 34, 43, 48, 62, 67, 76, 84, 89, 98]
ls_2 = [11, 37, 73, 99]
ls_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 25, 30, 40, 45, 50, 52, 54, 56, 60, 65, 70, 80, 85, 90]

def my_bacon_strategy(opponent_score, desired_bacon=(ls_10+ls_9), num_rolls=6):
    #desired = ls_10 + ls_9
    if opponent_score in desired_bacon:
        return 0
    else:
        return num_rolls

def my_swap_strategy(sc, opp_sc, margin1=8, margin2=8, desired_bacon=(ls_10+ls_9)):
    """ Returns num_rolls to force swap, if swap is desirable by either rollin 0, or 10 (to get 1)
    """
    opp_lead = opp_sc - sc
    if opp_lead > margin1 and is_swap(sc + free_bacon(opp_sc), opp_sc):
        return 0
    elif opp_lead > margin2 and is_swap(sc + 1, opp_sc):
        return 10
    else:
        return my_bacon_strategy(opp_sc, desired_bacon)



final_matrix = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, 0, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1, 0, 7, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 2, 4, 4, 5, 0, 4, 7, 10, 6, 5, 7, 7, 7, 6, 7, 5, 7, 4, 7, 8, 6, 4, 4, 4, 7, 7, 5, 6, 6, 5, 6, 7, 8, 10, 7, 6, 8, 9, 8, 5, 8, 1, 10, 7, 7, 0, 10, 8, 10, 8, 9, 9, 1, 1, 1, 1, 2, 6, 2, 1, 0, 3, 1, 8, 10, 9, 2, 2, 0, 0, 4, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 5, 3, 3, 0, 0, 5, 3, 6, 4, 4, 7, 3, 4, 0, 5, 6, 5, 4, 5, 6, 7, 5, 9, 7, 5, 5, 7, 8, 7, 8, 6, 8, 6, 8, 7, 9, 8, 10, 7, 7, 5, 9, 7, 9, 9, 5, 9, 6, 9, 1, 2, 5, 7, 7, 7, 1, 8, 7, 0, 0, 9, 1, 2, 9, 1, 1, 7, 1, 0, 10, 1, 0, 4, 7, 10, 5, 1, 1, 9, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 0, 3, 3, 4, 2, 4, 4, 2, 5, 5, 6, 4, 5, 5, 5, 4, 4, 5, 5, 4, 6, 5, 9, 8, 6, 6, 7, 7, 10, 8, 7, 9, 10, 6, 7, 8, 10, 7, 5, 6, 9, 6, 9, 8, 5, 6, 9, 4, 6, 4, 8, 7, 7, 0, 6, 3, 10, 2, 0, 3, 4, 8, 10, 1, 0, 10, 1, 9, 2, 0, 1, 0, 4, 0, 0, 10, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 0, 3, 5, 3, 2, 0, 2, 3, 0, 0, 4, 3, 0, 3, 4, 0, 4, 5, 0, 8, 6, 7, 5, 0, 6, 5, 9, 7, 9, 6, 9, 6, 9, 5, 7, 5, 6, 7, 10, 8, 7, 9, 10, 10, 3, 10, 9, 0, 7, 0, 9, 8, 7, 8, 9, 10, 10, 4, 0, 10, 0, 1, 8, 1, 1, 0, 1, 1, 0, 0, 10, 0, 6, 9, 9, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2, 3, 0, 2, 2, 4, 5, 0, 3, 5, 3, 3, 3, 4, 4, 2, 3, 3, 4, 2, 3, 5, 0, 4, 6, 3, 7, 10, 8, 6, 5, 5, 5, 5, 9, 5, 8, 6, 9, 10, 6, 6, 9, 8, 7, 10, 0, 8, 9, 10, 10, 9, 10, 10, 9, 8, 9, 10, 2, 0, 9, 8, 10, 9, 1, 0, 9, 4, 3, 1, 0, 1, 2, 0, 10, 8, 8, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 5, 0, 0, 4, 2, 0, 7, 0, 2, 4, 4, 0, 1, 0, 0, 5, 5, 0, 6, 5, 5, 4, 8, 4, 6, 0, 4, 0, 4, 9, 5, 6, 9, 4, 8, 7, 5, 6, 5, 7, 6, 7, 10, 4, 7, 10, 0, 10, 5, 5, 0, 7, 4, 8, 8, 0, 6, 10, 4, 10, 0, 2, 10, 0, 8, 9, 10, 10, 3, 0, 0, 0, 0, 9, 1, 10, 9, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 3, 0, 4, 1, 3, 4, 0, 3, 1, 0, 0, 5, 2, 5, 5, 0, 0, 5, 0, 0, 6, 0, 5, 2, 5, 10, 5, 7, 7, 6, 7, 5, 5, 4, 3, 4, 5, 7, 10, 3, 5, 5, 6, 7, 6, 7, 8, 5, 5, 5, 9, 9, 6, 6, 10, 9, 9, 1, 10, 1, 0, 8, 9, 9, 2, 2, 6, 9, 1, 2, 10, 1, 3, 9, 1, 7, 7], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 0, 0, 2, 3, 3, 0, 0, 4, 0, 3, 0, 1, 1, 0, 2, 2, 0, 3, 0, 0, 5, 6, 5, 7, 0, 7, 4, 4, 0, 6, 5, 4, 4, 5, 7, 6, 0, 10, 6, 10, 0, 6, 8, 0, 4, 0, 9, 10, 0, 4, 9, 5, 7, 2, 6, 9, 4, 5, 0, 1, 2, 2, 2, 0, 0, 0, 1, 2, 10, 0, 10, 0, 0, 4, 0, 2, 3], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 0, 0, 2, 3, 3, 0, 0, 4, 3, 0, 0, 0, 3, 0, 1, 0, 0, 5, 5, 4, 5, 0, 7, 0, 0, 4, 8, 5, 5, 4, 4, 4, 6, 5, 7, 7, 9, 7, 6, 8, 10, 8, 5, 7, 6, 0, 8, 10, 5, 3, 5, 7, 10, 5, 6, 0, 7, 8, 1, 0, 0, 8, 6, 2, 9, 2, 1, 10, 8, 10, 2, 10, 7, 4, 1, 2, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 4, 0, 0, 5, 2, 0, 0, 5, 3, 0, 0, 5, 0, 5, 0, 0, 0, 3, 5, 5, 4, 3, 4, 4, 4, 5, 4, 5, 4, 8, 3, 4, 5, 5, 6, 7, 4, 0, 4, 7, 7, 0, 0, 10, 3, 9, 3, 3, 0, 4, 8, 7, 8, 9, 0, 10, 1, 1, 1, 2, 0, 0, 1, 2, 0, 0, 0, 1, 3, 2, 1, 1, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 10, 2, 3, 0, 0, 6, 3, 0, 0, 4, 0, 0, 9, 5, 6, 5, 4, 0, 4, 7, 6, 6, 6, 3, 8, 6, 7, 6, 4, 7, 3, 6, 10, 8, 6, 6, 8, 8, 0, 5, 6, 8, 6, 8, 5, 10, 0, 0, 6, 7, 4, 6, 4, 1, 1, 9, 10, 0, 10, 0, 1, 1, 9, 1, 0, 1, 10, 1, 6, 0, 2, 0, 10, 0, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 10, 0, 0, 0, 4, 2, 0, 0, 5, 3, 4, 4, 2, 4, 6, 6, 0, 8, 4, 4, 7, 4, 4, 5, 4, 3, 4, 4, 3, 4, 4, 7, 10, 10, 4, 6, 5, 8, 7, 8, 9, 0, 10, 7, 8, 0, 5, 8, 6, 8, 5, 1, 3, 0, 10, 0, 9, 0, 0, 7, 8, 1, 0, 4, 10, 0, 1, 1, 9, 0, 2, 7, 1, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 4, 0, 0, 0, 9, 3, 0, 3, 3, 4, 0, 3, 0, 0, 6, 4, 4, 3, 5, 5, 5, 4, 3, 3, 5, 4, 6, 4, 6, 8, 4, 7, 5, 7, 4, 5, 10, 5, 6, 8, 8, 8, 3, 9, 3, 8, 6, 9, 6, 10, 0, 6, 1, 9, 8, 10, 1, 9, 6, 1, 1, 10, 1, 10, 1, 1, 1, 0, 1, 10, 0, 1, 0, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 4, 0, 0, 0, 3, 2, 0, 0, 2, 3, 3, 4, 6, 6, 3, 4, 4, 4, 3, 5, 5, 7, 3, 5, 4, 7, 4, 7, 7, 7, 8, 9, 4, 9, 6, 7, 7, 4, 5, 8, 9, 10, 9, 8, 5, 9, 8, 0, 6, 9, 5, 9, 8, 7, 10, 0, 6, 10, 0, 9, 6, 4, 9, 0, 1, 0, 1, 1, 9, 2, 1, 0, 1, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 3, 8, 0, 0, 4, 2, 0, 6, 5, 0, 3, 5, 6, 2, 3, 3, 4, 0, 2, 0, 6, 4, 5, 4, 3, 4, 5, 7, 10, 6, 3, 3, 9, 0, 9, 8, 5, 9, 4, 5, 10, 9, 8, 9, 0, 8, 8, 8, 7, 8, 1, 3, 10, 9, 10, 9, 10, 10, 1, 10, 1, 9, 1, 0, 1, 2, 0, 10, 10, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 4, 3, 0, 3, 5, 3, 3, 3, 0, 5, 0, 6, 4, 4, 2, 0, 5, 5, 5, 4, 6, 6, 8, 0, 8, 5, 2, 4, 8, 4, 2, 6, 5, 8, 8, 5, 6, 8, 9, 8, 0, 6, 7, 0, 6, 10, 10, 0, 9, 9, 7, 10, 9, 8, 10, 7, 0, 1, 10, 1, 0, 0, 0, 3, 0, 8], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 4, 0, 0, 2, 0, 0, 5, 4, 0, 5, 0, 0, 4, 5, 3, 4, 0, 4, 2, 2, 2, 9, 7, 5, 7, 5, 0, 4, 3, 8, 0, 7, 0, 4, 4, 0, 2, 0, 9, 2, 0, 2, 5, 2, 9, 4, 2, 10, 5, 10, 1, 9, 6, 3, 3, 10, 4, 10, 0, 0, 1, 10, 9, 7, 9, 10, 7, 10, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5, 2, 0, 0, 4, 3, 0, 3, 0, 0, 4, 0, 0, 4, 0, 4, 0, 0, 5, 2, 4, 0, 8, 0, 5, 0, 4, 0, 5, 0, 6, 0, 8, 9, 5, 5, 6, 2, 9, 9, 4, 8, 5, 10, 10, 9, 6, 0, 8, 2, 10, 0, 7, 0, 9, 8, 0, 4, 9, 2, 10, 0, 3, 8, 2, 1, 2, 2, 5, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 4, 0, 2, 2, 0, 4, 2, 0, 1, 0, 7, 3, 3, 4, 1, 5, 5, 4, 5, 3, 8, 4, 5, 4, 4, 2, 9, 7, 4, 7, 6, 6, 6, 8, 4, 10, 0, 4, 5, 0, 9, 5, 6, 0, 8, 8, 9, 1, 1, 7, 4, 4, 4, 5, 0, 8, 9, 0, 1, 2, 10, 10, 0, 2, 9], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 3, 0, 0, 2, 4, 0, 0, 4, 2, 3, 3, 0, 0, 4, 1, 5, 0, 0, 0, 5, 6, 3, 5, 5, 4, 6, 7, 4, 6, 4, 7, 7, 5, 0, 6, 5, 6, 10, 0, 10, 7, 0, 6, 9, 0, 8, 4, 10, 10, 2, 10, 0, 7, 2, 2, 0, 0, 8, 0, 2, 0, 10, 8, 2, 1, 10, 10, 1, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 8, 3, 0, 3, 2, 0, 3, 4, 6, 5, 0, 6, 6, 3, 4, 3, 4, 7, 6, 6, 6, 4, 9, 7, 3, 7, 3, 4, 7, 5, 5, 9, 3, 1, 7, 8, 8, 7, 7, 3, 9, 1, 6, 9, 1, 2, 0, 0, 8, 4, 6, 0, 8, 1, 2, 0, 0, 0, 10, 0, 1, 0, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 3, 2, 0, 6, 3, 0, 4, 5, 6, 7, 0, 7, 4, 3, 0, 3, 6, 6, 4, 7, 7, 3, 6, 6, 0, 6, 9, 8, 4, 0, 0, 8, 8, 7, 10, 9, 10, 8, 8, 5, 0, 0, 0, 1, 6, 0, 7, 1, 2, 4, 4, 7, 1, 9, 1, 1, 8, 1, 0, 1, 0, 1, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 2, 0, 0, 2, 2, 0, 2, 5, 0, 3, 4, 4, 4, 0, 5, 4, 6, 6, 4, 5, 5, 7, 7, 8, 8, 7, 7, 7, 8, 6, 8, 9, 5, 3, 8, 7, 6, 9, 9, 8, 7, 7, 0, 10, 5, 7, 6, 1, 8, 6, 10, 1, 1, 0, 10, 8, 1, 10, 1, 1, 1, 9, 0, 1, 0, 7], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 5, 4, 3, 2, 3, 5, 4, 5, 6, 3, 5, 5, 5, 5, 7, 5, 7, 5, 7, 8, 8, 7, 8, 8, 9, 8, 8, 7, 6, 10, 6, 7, 8, 5, 8, 7, 10, 5, 8, 5, 9, 0, 8, 0, 7, 9, 0, 8, 9, 1, 0, 1, 4, 9, 0, 1, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 4, 0, 0, 2, 4, 2, 0, 2, 5, 5, 4, 4, 3, 3, 5, 7, 6, 5, 4, 7, 5, 6, 7, 3, 6, 5, 6, 7, 8, 8, 8, 10, 8, 9, 6, 6, 8, 9, 7, 9, 9, 10, 1, 7, 8, 1, 3, 0, 8, 10, 1, 1, 1, 3, 6, 2, 10, 10, 10, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 2, 0, 0, 3, 2, 0, 2, 0, 3, 5, 0, 4, 5, 3, 4, 6, 6, 4, 5, 5, 6, 2, 6, 5, 5, 6, 0, 8, 6, 5, 6, 0, 9, 6, 9, 7, 10, 0, 7, 8, 0, 6, 5, 10, 10, 6, 3, 9, 10, 5, 8, 3, 10, 9, 1, 1, 1, 1, 2, 1, 2, 0, 7], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 5, 0, 2, 2, 2, 2, 0, 4, 0, 2, 5, 3, 4, 4, 6, 4, 0, 3, 5, 5, 9, 7, 5, 6, 7, 6, 8, 8, 6, 7, 8, 0, 5, 0, 5, 2, 9, 2, 8, 8, 9, 6, 0, 7, 6, 0, 1, 0, 7, 0, 9, 10, 10, 10, 0, 10, 10, 10, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 5, 2, 0, 0, 0, 4, 0, 0, 3, 4, 2, 4, 2, 4, 4, 5, 4, 6, 3, 0, 7, 7, 3, 5, 5, 4, 8, 5, 7, 7, 4, 9, 6, 7, 0, 6, 7, 8, 8, 10, 10, 9, 7, 6, 5, 2, 8, 8, 2, 5, 7, 7, 7, 8, 7, 2, 7, 2, 2, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 0, 6, 3, 0, 2, 2, 2, 4, 3, 3, 3, 4, 3, 4, 3, 4, 7, 0, 3, 0, 7, 3, 0, 6, 5, 8, 5, 7, 7, 5, 0, 0, 10, 7, 0, 8, 5, 7, 10, 2, 4, 9, 0, 7, 9, 6, 7, 0, 9, 1, 3, 2, 2, 0, 2, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 3, 0, 1, 0, 0, 0, 0, 4, 4, 4, 0, 4, 0, 4, 4, 5, 4, 4, 5, 6, 5, 0, 6, 2, 6, 7, 0, 4, 8, 5, 2, 0, 7, 8, 4, 7, 10, 4, 6, 6, 1, 6, 1, 0, 0, 2, 6, 2, 0, 0, 0, 0, 0, 2, 8, 0, 5], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7, 2, 0, 3, 3, 4, 5, 4, 3, 5, 3, 4, 5, 4, 5, 3, 6, 6, 6, 3, 6, 2, 6, 6, 5, 4, 0, 7, 6, 4, 6, 9, 8, 1, 6, 6, 4, 4, 9, 1, 10, 1, 6, 9, 7, 4, 6, 0, 9, 5, 1, 0, 1, 1, 5], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 6, 3, 0, 3, 0, 4, 3, 1, 4, 3, 5, 4, 6, 7, 5, 6, 3, 4, 4, 0, 4, 0, 7, 6, 0, 4, 6, 0, 3, 0, 9, 9, 8, 0, 0, 9, 6, 3, 0, 4, 6, 0, 1, 0, 4, 6, 3, 2, 5, 3, 10, 1, 0, 0, 4], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 2, 0, 3, 3, 0, 2, 0, 4, 0, 6, 4, 5, 3, 5, 5, 6, 6, 4, 4, 5, 5, 5, 5, 3, 6, 6, 5, 7, 6, 8, 3, 7, 6, 8, 9, 5, 4, 8, 6, 0, 1, 4, 5, 1, 4, 4, 5, 1, 6, 4, 1, 0, 0, 0, 1, 1, 5], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 4, 0, 3, 0, 4, 0, 3, 0, 4, 0, 4, 4, 9, 5, 2, 6, 5, 6, 7, 6, 5, 8, 7, 7, 8, 4, 0, 6, 8, 8, 10, 8, 1, 10, 9, 5, 0, 5, 1, 8, 5, 0, 5, 0, 1, 5, 2, 1, 1, 0, 10, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 2, 0, 3, 0, 3, 0, 2, 3, 5, 0, 5, 6, 3, 4, 0, 5, 4, 6, 6, 3, 5, 5, 8, 8, 6, 5, 8, 5, 7, 8, 9, 8, 8, 0, 10, 5, 8, 5, 9, 8, 7, 4, 4, 3, 10, 1, 0, 0, 10, 8, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 3, 0, 3, 0, 3, 2, 2, 3, 2, 0, 4, 3, 4, 5, 2, 3, 6, 6, 4, 4, 6, 7, 5, 3, 5, 5, 9, 4, 8, 0, 9, 8, 9, 9, 3, 8, 9, 3, 10, 5, 9, 10, 4, 1, 3, 0, 7, 1, 1, 8, 10, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 4, 0, 2, 3, 2, 0, 4, 3, 4, 4, 4, 3, 6, 5, 6, 5, 5, 6, 5, 0, 8, 5, 0, 4, 8, 7, 9, 8, 10, 0, 0, 9, 8, 6, 10, 5, 6, 4, 9, 0, 1, 9, 1, 10, 10, 7, 10, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 3, 6, 0, 3, 0, 3, 3, 3, 0, 4, 0, 5, 0, 5, 5, 5, 4, 6, 4, 6, 8, 6, 8, 4, 5, 9, 6, 10, 7, 5, 4, 10, 10, 10, 2, 0, 6, 8, 4, 9, 10, 1, 10, 0, 10, 7, 5, 5, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 2, 0, 3, 2, 2, 5, 2, 4, 3, 4, 4, 4, 3, 0, 3, 6, 0, 5, 0, 3, 6, 0, 5, 5, 5, 5, 5, 7, 0, 7, 4, 4, 9, 9, 2, 4, 0, 2, 4, 10, 4, 10, 0, 5, 1, 1, 6, 0, 4, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2, 0, 1, 0, 2, 0, 2, 0, 2, 3, 3, 3, 2, 2, 5, 4, 3, 5, 4, 3, 0, 0, 5, 1, 7, 5, 0, 0, 4, 7, 1, 6, 8, 8, 0, 3, 4, 4, 0, 0, 4, 4, 4, 4, 0, 0, 1, 10, 6, 5, 4, 3], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 2, 0, 3, 2, 3, 2, 3, 0, 3, 3, 4, 4, 4, 3, 0, 2, 5, 4, 5, 0, 0, 6, 0, 6, 4, 5, 8, 8, 7, 9, 3, 10, 0, 6, 0, 4, 7, 2, 4, 4, 2, 2, 10, 4, 6, 6, 3, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 1, 0, 4, 4, 3, 4, 3, 0, 5, 0, 5, 5, 4, 0, 4, 3, 5, 5, 3, 7, 5, 3, 4, 6, 8, 0, 7, 10, 8, 0, 0, 6, 9, 3, 3, 0, 4, 0, 2, 0, 0, 4, 0, 6, 3, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 1, 0, 0, 7, 0, 4, 0, 4, 0, 3, 0, 0, 2, 2, 4, 0, 3, 4, 4, 4, 5, 5, 4, 0, 3, 0, 7, 7, 6, 10, 8, 0, 9, 8, 8, 9, 0, 6, 5, 3, 10, 1, 10, 1, 3, 6, 1, 3, 4], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5, 0, 2, 0, 5, 0, 3, 4, 4, 3, 5, 0, 2, 5, 5, 6, 4, 7, 3, 6, 6, 0, 5, 0, 6, 5, 9, 7, 8, 8, 9, 10, 0, 6, 1, 3, 5, 0, 1, 3, 0, 10, 10, 0, 3, 0, 3, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 3, 0, 2, 0, 2, 3, 4, 0, 0, 3, 4, 4, 0, 4, 6, 6, 6, 6, 4, 0, 6, 6, 8, 10, 7, 9, 9, 10, 7, 8, 8, 0, 10, 10, 8, 0, 1, 1, 1, 10, 5, 5, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 4, 0, 4, 0, 0, 2, 4, 3, 3, 0, 5, 5, 3, 7, 5, 6, 5, 5, 7, 8, 6, 7, 8, 10, 8, 9, 9, 9, 3, 10, 10, 10, 10, 0, 0, 3, 9, 1, 2, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 4, 0, 4, 0, 2, 0, 5, 0, 3, 0, 3, 3, 3, 3, 4, 0, 6, 0, 0, 3, 3, 3, 5, 5, 6, 5, 7, 0, 8, 9, 9, 7, 9, 10, 0, 9, 10, 9, 10, 10, 10, 0, 2, 5, 10, 0], [-1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 3, 0, 2, 0, 3, 0, 3, 0, 4, 5, 0, 2, 0, 1, 5, 6, 2, 6, 4, 0, 5, 0, 7, 6, 4, 7, 9, 2, 8, 5, 0, 0, 4, 2, 2, 0, 10, 2, 10, 0, 0, 4, 2, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 2, 0, 2, 0, 3, 0, 0, 1, 3, 3, 4, 2, 0, 1, 6, 0, 0, 2, 0, 5, 3, 5, 0, 5, 6, 6, 8, 0, 9, 8, 8, 8, 9, 8, 8, 2, 0, 0, 10, 2, 4, 4, 2, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 2, 0, 2, 0, 0, 0, 4, 3, 0, 2, 0, 5, 5, 3, 0, 5, 0, 0, 2, 0, 6, 5, 5, 0, 0, 8, 10, 8, 9, 0, 10, 10, 2, 0, 9, 0, 2, 2, 4, 4, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 1, 0, 2, 0, 1, 0, 0, 5, 4, 1, 0, 0, 3, 0, 5, 5, 4, 0, 2, 0, 6, 4, 4, 6, 1, 8, 6, 7, 1, 10, 9, 6, 8, 10, 1, 9, 0, 0, 1, 0, 1, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 3, 0, 3, 1, 0, 0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 6, 0, 5, 6, 7, 0, 0, 1, 4, 1, 0, 1, 1, 9, 10, 1, 10, 10, 10, 1, 10, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 5, 0, 1, 0, 3, 4, 0, 4, 1, 0, 0, 0, 0, 6, 5, 5, 6, 7, 7, 6, 6, 7, 0, 8, 7, 7, 8, 1, 10, 1, 0, 0, 0, 0, 1], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 0, 0, 3, 0, 4, 0, 6, 4, 0, 4, 0, 0, 3, 5, 0, 5, 3, 4, 5, 7, 8, 9, 8, 7, 8, 8, 10, 8, 8, 10, 1, 9, 1, 3, 10, 10, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 1, 0, 1, 10, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 2, 0, 0, 3, 2, 4, 0, 3, 9, 0, 7, 6, 0, 0, 5, 0, 5, 5, 4, 6, 7, 7, 8, 8, 9, 8, 7, 9, 9, 8, 8, 10, 1, 0, 3, 3, 10, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 2, 0, 3, 2, 0, 8, 0, 4, 4, 0, 3, 4, 0, 5, 4, 0, 4, 3, 7, 5, 6, 6, 8, 8, 6, 8, 10, 7, 8, 8, 10, 10, 0, 9, 10, 10, 0, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 10, 0, 0, 0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 1, 0, 0, 1, 1, 0, 9, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 4, 0, 3, 3, 4, 3, 4, 0, 3, 5, 3, 4, 4, 7, 0, 6, 6, 4, 6, 6, 7, 7, 10, 7, 8, 8, 10, 10, 9, 10, 10, 10, 1], [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 10, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 1, 2, 0, 0, 3, 0, 0, 4, 0, 5, 3, 0, 4, 2, 5, 6, 4, 7, 5, 6, 0, 8, 7, 6, 7, 7, 3, 8, 10, 9, 2, 2, 10, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 0, 1, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 10, 0, 10, 10, 0, 0, 10, 0, 0, 4, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 10, 0, 0, 1, 0, 2, 0, 0, 3, 3, 3, 3, 0, 4, 3, 0, 0, 0, 5, 0, 5, 6, 5, 4, 2, 7, 6, 6, 6, 10, 0, 2, 10, 9, 0, 2, 2, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 10, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 3, 2, 2, 10, 3, 0, 3, 2, 4, 0, 0, 5, 4, 5, 0, 0, 6, 7, 6, 0, 2, 0, 2, 10, 1, 0, 2, 10], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 2, 1, 0, 10, 0, 1, 0, 3, 0, 6, 0, 0, 3, 0, 10, 0, 1, 4, 0, 0, 9, 1, 0, 10, 0, 10, 10, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 4, 2, 0, 0, 0, 1, 3, 0, 2, 3, 0, 0, 3, 0, 4, 1, 2, 4, 4, 6, 6, 1, 6, 7, 6, 7, 5, 6, 0, 7, 0, 9, 0, 10, 0, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 9, 0, 6, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 0, 0, 1, 1, 0, 0, 0, 2, 0, 2, 2, 0, 3, 3, 0, 4, 10, 4, 3, 4, 0, 3, 4, 5, 6, 0, 6, 5, 6, 7, 9, 9, 9, 1, 1, 1, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 10, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 10, 0, 10, 3, 10, 0, 0, 0, 0, 10, 10, 0, 0, 0, 10, 0, 2, 0, 2, 0, 2, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 1, 2, 0, 1, 0, 2, 3, 0, 0, 0, 3, 0, 0, 5, 3, 7, 5, 6, 6, 6, 7, 0, 8, 8, 8, 9, 10, 10, 0, 9], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 10, 0, 1, 1, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 4, 0, 0, 4, 5, 5, 5, 5, 6, 0, 4, 0, 1, 8, 8, 8, 0, 0, 1, 1], [-1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 4, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 10, 1, 9, 0, 0, 0, 0, 0, 9, 0, 8, 0, 0, 9, 0, 0, 10, 0, 1, 0, 2, 0, 2, 0, 10, 0, 2, 9, 0, 0, 0, 2, 9, 0, 0, 1, 10, 0, 5, 0, 0, 2, 0, 0, 10, 3, 0, 4, 5, 5, 5, 4, 5, 5, 6, 4, 0, 1, 7, 0, 8, 9, 1, 10, 0], [-1, 10, 0, 2, 2, 0, 0, 0, 0, 0, 8, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 8, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 10, 0, 10, 1, 0, 0, 10, 0, 0, 0, 0, 2, 3, 4, 0, 4, 4, 4, 6, 5, 8, 10, 9, 7, 5, 1, 7, 8, 7, 8, 9, 0, 10], [-1, 10, 0, 1, 1, 0, 10, 0, 0, 0, 8, 2, 0, 10, 0, 10, 10, 10, 0, 0, 0, 10, 1, 0, 0, 9, 10, 10, 0, 0, 10, 10, 0, 0, 9, 10, 0, 9, 0, 10, 9, 0, 0, 7, 0, 8, 0, 0, 0, 0, 0, 1, 0, 10, 0, 10, 0, 1, 0, 10, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 1, 10, 3, 3, 0, 2, 0, 1, 0, 4, 6, 0, 3, 4, 2, 4, 4, 4, 6, 5, 7, 5, 7, 8, 10, 0, 10, 9, 9, 1], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 9, 0, 0, 10, 0, 2, 0, 0, 0, 0, 0, 0, 0, 10, 0, 8, 0, 0, 8, 0, 10, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 0, 0, 1, 9, 1, 0, 1, 0, 0, 2, 0, 0, 2, 0, 0, 4, 3, 0, 2, 4, 2, 3, 10, 4, 5, 5, 3, 5, 5, 6, 7, 1, 7, 8, 8, 0], [-1, 0, 0, 0, 0, 0, 10, 10, 0, 1, 1, 10, 10, 10, 0, 10, 0, 9, 0, 0, 0, 10, 0, 0, 0, 7, 1, 0, 0, 0, 2, 10, 10, 0, 1, 10, 0, 9, 0, 9, 7, 3, 0, 0, 0, 10, 3, 0, 0, 0, 10, 10, 0, 10, 0, 10, 0, 10, 0, 10, 2, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 2, 1, 8, 2, 0, 1, 3, 3, 0, 0, 3, 4, 3, 0, 4, 5, 5, 3, 4, 7, 5, 6, 0, 2, 2, 2, 10], [-1, 1, 0, 0, 0, 0, 10, 10, 0, 10, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 10, 0, 0, 0, 9, 10, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 1, 10, 9, 0, 0, 2, 9, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 3, 1, 3, 3, 4, 3, 3, 0, 4, 5, 3, 0, 0, 5, 6, 7, 0, 8, 2, 9], [-1, 9, 0, 0, 0, 0, 10, 9, 0, 10, 0, 9, 1, 9, 10, 9, 0, 0, 0, 0, 1, 0, 0, 10, 0, 1, 0, 0, 10, 0, 1, 10, 0, 0, 0, 9, 0, 8, 0, 10, 7, 0, 0, 0, 0, 6, 0, 0, 0, 0, 8, 10, 0, 10, 0, 10, 0, 10, 0, 10, 2, 0, 9, 0, 8, 0, 0, 7, 0, 8, 0, 10, 0, 9, 0, 0, 0, 0, 0, 2, 3, 1, 0, 3, 4, 2, 3, 3, 4, 5, 5, 4, 0, 4, 0, 6, 6, 2, 8, 8], [-1, 10, 0, 0, 0, 10, 9, 10, 0, 10, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 7, 10, 10, 0, 0, 7, 9, 2, 0, 0, 0, 0, 10, 0, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 10, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 10, 1, 0, 0, 2, 10, 9, 0, 0, 0, 0, 8, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 3, 4, 4, 0, 3, 0, 7, 5, 0, 4, 0, 5, 7, 1, 0, 1, 8], [-1, 10, 0, 0, 0, 9, 10, 9, 0, 10, 3, 9, 0, 9, 0, 8, 1, 0, 1, 0, 6, 10, 0, 0, 0, 3, 10, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 8, 9, 0, 7, 0, 0, 7, 10, 0, 0, 0, 7, 9, 1, 10, 1, 9, 0, 10, 0, 9, 0, 9, 1, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 8, 0, 8, 8, 0, 7, 2, 2, 0, 0, 2, 4, 3, 0, 3, 4, 4, 4, 0, 3, 0, 4, 0, 0, 1, 0, 7], [-1, 10, 0, 0, 0, 10, 9, 9, 0, 10, 6, 0, 8, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 1, 1, 7, 0, 0, 1, 1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 9, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 2, 0, 3, 3, 0, 2, 0, 3, 0, 4, 5, 7, 0, 7, 7], [-1, 9, 0, 9, 8, 10, 2, 9, 0, 9, 5, 9, 8, 8, 0, 0, 0, 7, 0, 0, 9, 9, 0, 0, 0, 6, 10, 0, 0, 0, 0, 9, 1, 0, 6, 9, 1, 6, 0, 0, 8, 0, 0, 7, 0, 0, 0, 0, 6, 0, 6, 8, 0, 9, 0, 9, 0, 9, 8, 9, 0, 9, 7, 0, 0, 0, 9, 6, 0, 0, 1, 9, 0, 8, 0, 8, 10, 0, 0, 8, 2, 0, 0, 0, 3, 3, 0, 0, 3, 3, 2, 0, 0, 3, 0, 6, 6, 8, 8, 7], [-1, 9, 0, 9, 10, 9, 8, 2, 0, 2, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 5, 8, 0, 0, 0, 2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 6, 1, 3, 0, 1, 6, 1, 6, 0, 0, 0, 0, 0, 1, 0, 9, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 9, 0, 0, 0, 0, 0, 8, 0, 7, 0, 2, 0, 0, 0, 3, 4, 0, 0, 5, 3, 3, 0, 0, 4, 0, 5, 6, 6, 0, 6], [-1, 10, 2, 8, 9, 9, 8, 8, 2, 7, 2, 9, 1, 8, 0, 7, 8, 7, 0, 0, 9, 0, 8, 0, 0, 6, 0, 8, 0, 0, 0, 8, 0, 0, 2, 0, 0, 6, 0, 8, 10, 0, 0, 0, 0, 9, 0, 0, 0, 0, 7, 9, 0, 8, 0, 9, 7, 9, 9, 8, 0, 0, 6, 0, 0, 0, 0, 9, 0, 0, 8, 0, 7, 7, 0, 0, 0, 0, 0, 8, 4, 0, 6, 0, 3, 3, 0, 2, 3, 3, 7, 0, 0, 3, 8, 6, 6, 6, 6, 6], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 0, 8, 0, 2, 1, 0, 7, 0, 0, 0, 0, 0, 5, 0, 0, 0, 8, 0, 6, 0, 0, 2, 0, 3, 0, 0, 5, 0, 6, 0, 0, 0, 0, 0, 9, 0, 3, 0, 0, 1, 6, 1, 0, 0, 1, 6, 1, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 6, 2, 3, 0, 0, 2, 3, 3, 0, 0, 0, 4, 4, 5, 5, 7, 0], [-1, 8, 0, 10, 10, 9, 10, 8, 10, 0, 1, 8, 0, 7, 0, 6, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 8, 8, 0, 0, 7, 0, 5, 0, 7, 5, 9, 0, 6, 0, 6, 8, 0, 5, 0, 8, 0, 0, 0, 0, 0, 10, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 6, 1, 7, 7, 0, 0, 7, 0, 0, 0, 0, 2, 3, 0, 0, 0, 3, 3, 2, 0, 0, 4, 5, 0, 6, 6, 8], [-1, 9, 0, 7, 9, 10, 10, 9, 7, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 7, 2, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 9, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 9, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 3, 1, 0, 0, 2, 3, 0, 0, 0, 3, 4, 4, 5, 5, 6], [-1, 7, 0, 9, 9, 8, 7, 8, 7, 1, 0, 8, 0, 8, 7, 0, 0, 0, 0, 1, 6, 8, 0, 6, 0, 0, 7, 0, 7, 0, 1, 7, 0, 0, 4, 7, 0, 5, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 8, 0, 7, 0, 8, 6, 7, 8, 7, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 8, 8, 0, 6, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 3, 0, 1, 0, 0, 4, 5, 5, 0, 5], [-1, 7, 0, 9, 8, 7, 10, 10, 8, 7, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 6, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 0, 1, 0, 0, 5, 0, 5, 0, 2, 0, 2, 0, 5, 0, 9, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 0, 9, 0, 5, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 6, 0, 0, 0, 0, 3, 5, 5, 5, 5], [-1, 6, 0, 10, 8, 7, 9, 6, 6, 9, 0, 7, 6, 7, 0, 6, 0, 0, 1, 0, 3, 8, 0, 0, 0, 0, 6, 0, 0, 0, 0, 7, 0, 1, 0, 0, 0, 4, 7, 0, 5, 0, 0, 0, 6, 0, 0, 0, 0, 6, 1, 7, 1, 7, 1, 6, 1, 7, 1, 7, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 8, 7, 0, 6, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 6, 2, 0, 0, 5, 2, 2, 0, 0, 1, 0, 3, 4, 4, 6, 0], [-1, 9, 7, 7, 6, 7, 8, 7, 8, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 7, 0, 0, 1, 0, 7, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 4, 7, 0, 0, 0, 0, 7, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8, 0, 0, 0, 1, 0, 4, 0, 0, 1, 0, 5, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 4, 4, 4, 5], [-1, 2, 8, 10, 2, 8, 6, 8, 8, 7, 0, 6, 8, 5, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 6, 1, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 0, 1, 0, 0, 4, 0, 4, 5, 0, 0, 4, 2, 0, 0, 0, 0, 6, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 3, 4, 4, 4], [-1, 6, 2, 2, 8, 2, 2, 2, 2, 2, 0, 0, 7, 0, 5, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 0, 0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 5, 1, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 3, 3, 5, 4], [-1, 8, 6, 6, 8, 5, 6, 5, 6, 6, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 3, 6, 5, 0, 0, 0, 6, 5, 0, 0, 0, 5, 0, 0, 2, 0, 0, 3, 0, 1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 0, 6, 0, 7, 4, 7, 0, 5, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 8, 0, 3, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 2, 0, 3, 4, 1], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 2, 0, 0, 0, 0, 2, 0, 6, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 3, 4, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 5, 5, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 4, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 3, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 2, 2, 3, 4], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 1, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 2, 0, 2, 0, 3, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [-1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def final_strategy(sc, opp_sc):
    num_rolls = int(final_matrix[sc][opp_sc])
    if num_rolls < -1:
        return int(final_strategy_old(sc, opp_sc))
    elif num_rolls >= 0:
        return int(num_rolls)

def final_strategy_new(sc, opp_sc):
    return int(final_matrix[sc][opp_sc])


def final_strategy_old(sc, opp_sc): #change###def final_strategy_old(sc, opp_sc):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """ # BEGIN PROBLEM 12
#    bacon = (opp_sc % 10) * (opp_sc // 10) % 10 + 1 # return 0
#    if sc + bacon >= 90:
#        return 0
#    elif (opp_sc - sc) > 10 and is_swap(sc + 1, opp_sc):
#        return 10 # to forse swap
#    else:
#        return my_swap_strategy(sc, opp_sc, 8, 8, ls_10+ls_9)
    bacon = (opp_sc % 10) * (opp_sc // 10) % 10 + 1 # return 0
    my_bacon = (sc % 10) * (sc // 10) % 10 + 1

    if sc == 0 and opp_sc == 0:
        return 0
    if sc < 3 : # starting the game
        return 10

    if sc + bacon >= 100: #if bacon can end the game
        return 0
    #chance of getting 1 = .166 , .3056 , .4213 , .5177 , .5981 ,
     #.6651 , .7209 , .7674 , .8062 , .833
    if sc < opp_sc:

        if is_swap(sc + 1, opp_sc):
            return 10
        elif is_swap(sc + bacon, opp_sc):
            return 0
        elif opp_sc > sc :
            acc_risk = 45 - (opp_sc - sc)
            total = 1
            risk = 15
            while risk < acc_risk :
                risk = risk * 1.3
                total += 1
            return total


    if sc > opp_sc:
        if sc > (opp_sc + 22) and not is_swap(sc + 1, opp_sc ) :
            if bacon > 9 and not is_swap(sc + bacon, opp_sc) :
                return 0
            else:
                return 7

        if is_swap(sc + 1, opp_sc ) or is_swap(sc + bacon, opp_sc):
            return 4
        elif is_swap(sc + 1 , opp_sc + 1) or is_swap(sc + 1 , opp_sc + my_bacon) :
            return 4
        elif sc > opp_sc :
            acc_risk = 75 - (sc - opp_sc)
            total = 1
            risk = 15
            while risk < acc_risk :
                risk = risk * 1.5
                total += 1
            return total

    return 5





    # END PROBLEM 12
##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()


#extra_turn = True
#def final_strategy(sc, opp_sc): #Using TROT
#    global extra_turn
#    if sc == 0 and opp_sc == 0:
#        return 0
#    elif extra_turn: # force a trot
#        extra_turn = not extra_turn
#        return turn % 8 #num_rolls to roll
#    elif not extra_turn:
#        extra_turn = not extra_turn
#        return final_strategy1(sc, opp_sc)
