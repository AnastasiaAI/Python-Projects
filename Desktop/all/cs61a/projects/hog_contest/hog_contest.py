"""
This is a minimal contest submission file. You may also submit the full
hog.py from Project 1 as your contest entry.

Only this file will be submitted. Make sure to include any helper functions
from `hog.py` that you'll need here! For example, if you have a function to
calculate Free Bacon points, you should make sure it's added to this file
as well.

Don't forget: your strategy must be deterministic and pure.
"""

PLAYER_NAME = 'Anastasia'

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

def final_strategy(sc, opp_sc):
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
