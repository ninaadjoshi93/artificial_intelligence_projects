def score(roll):
    if roll[0] == roll[1] and roll[1] == roll[2]:
        return 25
    else:
        return sum(roll)


def calc_expected_roll_score(dice_ini_roll, roll_decision):
    if not roll_decision[0] and not roll_decision[1] and not roll_decision[2]:
        return score(dice_ini_roll)

    expected_score = 0.0
    no_of_outputs = 0.0

    if roll_decision[0] or roll_decision[1] or roll_decision[2]:
        if roll_decision[0]:
            for dice_a in range(1, 7):
                expected_score += score(
                    [dice_a, dice_ini_roll[1], dice_ini_roll[2]])
            no_of_outputs += 6

        if roll_decision[1]:
            for dice_b in range(1, 7):
                expected_score += score(
                    [dice_ini_roll[0], dice_b, dice_ini_roll[2]])
            no_of_outputs += 6

        if roll_decision[2]:
            for dice_c in range(1, 7):
                expected_score += score(
                    [dice_ini_roll[0], dice_ini_roll[1], dice_c])
            no_of_outputs += 6
    else:
        expected_score += score(
            [dice_ini_roll[0], dice_ini_roll[1], dice_ini_roll[2]])

    return expected_score / no_of_outputs


def game_of_chance():
    best_roll = []
    best_score = 0

    dice_ini_roll = [6, 6, 1]

    print "original roll", " ".join([str(x) for x in dice_ini_roll])

    for roll_one in (True, False):
        for roll_two in (True, False):
            for roll_three in (True, False):
                current_expect_score = calc_expected_roll_score(dice_ini_roll,
                                                                [roll_one,
                                                                 roll_two,
                                                                 roll_three])
                if best_score < current_expect_score:
                    best_score = current_expect_score
                    best_roll = [roll_one, roll_two, roll_three]

    if True not in best_roll:
        print "You have a good score. No need to re roll."
    else:
        print "You can get a best expected score of", best_score, \
            "by rolling", " ".join([str(dice_ini_roll[i])
                                    for i, x in enumerate(best_roll) if x])


game_of_chance()
