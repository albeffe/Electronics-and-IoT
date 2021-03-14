import utime
from machine import Pin

DELAY_BETWEEN_DIGITS = 5  # delay between digits refresh
DELAY_BETWEEN_GAMES = 500  # delay between set and games score
DELAY_RESET = 1000  # time to keep the button pressed to reset the game

# Pin-component configuration
DIGIT_SELECTORS = [26, 27, 28, 0]  # Raspberry GPs associated to each display digit selector [1, 2, 3, 4]
DISPLAY_SEGMENTS = [15, 12, 21, 19, 18, 14, 22]  # Raspberry GPs associated to display segment [A, B, C, D, E, F, G]
DECIMAL_POINT_PIN = 20  # Raspberry GP associated to the display's decimal point
PLAYER1_BUTTON_PIN = 2
PLAYER2_BUTTON_PIN = 13

# Dictionary from digit 0 to 9 written with segments [A, B, C, D, E, F, G]
NUMBERS_CONFIGURATIONS = {0: [1, 1, 1, 1, 1, 1, 0],
                          1: [0, 1, 1, 0, 0, 0, 0],
                          2: [1, 1, 0, 1, 1, 0, 1],
                          3: [1, 1, 1, 1, 0, 0, 1],
                          4: [0, 1, 1, 0, 0, 1, 1],
                          5: [1, 0, 1, 1, 0, 1, 1],
                          6: [1, 0, 1, 1, 1, 1, 1],
                          7: [1, 1, 1, 0, 0, 0, 0],
                          8: [1, 1, 1, 1, 1, 1, 1],
                          9: [1, 1, 1, 1, 0, 1, 1]}


def notify_power_on():
    """
    The function makes the Raspberry Pico's onboard led flash so it notifies users it is ready
    """
    onboard_led = Pin(25, Pin.OUT)
    enabled = False
    for i in range(10):
        if enabled:
            onboard_led.off()
        else:
            onboard_led.on()
        utime.sleep_ms(125)
        enabled = not enabled


def pins_initialization():
    # Initialization
    for GP in DIGIT_SELECTORS:
        Pin(GP, Pin.OUT).on()  # All digits unselected (a digit is selected when the associated Pin is off)
    for GP in DISPLAY_SEGMENTS:
        Pin(GP, Pin.OUT).off()  # All segments switched off


def display_number(number):
    """
    Given an integer number the function prints it on the display
    """
    Pin(DISPLAY_SEGMENTS[0], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][0])
    Pin(DISPLAY_SEGMENTS[1], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][1])
    Pin(DISPLAY_SEGMENTS[2], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][2])
    Pin(DISPLAY_SEGMENTS[3], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][3])
    Pin(DISPLAY_SEGMENTS[4], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][4])
    Pin(DISPLAY_SEGMENTS[5], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][5])
    Pin(DISPLAY_SEGMENTS[6], Pin.OUT)(NUMBERS_CONFIGURATIONS[number][6])


def show_current_game_score(pl1_points, pl2_points):

    # The points of the two players are divided in digits
    pl1_tens = int(list("0" + str(pl1_points))[-2])
    pl1_units = int(list("0" + str(pl1_points))[-1])
    pl2_tens = int(list("0" + str(pl2_points))[-2])
    pl2_units = int(list("0" + str(pl2_points))[-1])
    current_score = [pl1_tens, pl1_units, pl2_tens, pl2_units]

    for digit in range(4):
        if ((digit == 0 or digit == 2) and current_score[digit] != 0) or (digit == 1 or digit == 3):
            # Digit Selection
            Pin(DIGIT_SELECTORS[digit], Pin.OUT).off()

            # Show Number
            display_number(current_score[digit])

            # Show Decimal Point
            if digit == 1:
                Pin(DECIMAL_POINT_PIN, Pin.OUT).on()

            # Sleep
            utime.sleep_ms(DELAY_BETWEEN_DIGITS)

            # Clear Decimal Point
            if digit == 1:
                Pin(DECIMAL_POINT_PIN, Pin.OUT).off()

            # Clear Number
            for segment in DISPLAY_SEGMENTS:
                Pin(segment, Pin.OUT).off()

            # Digit Deselection
            Pin(DIGIT_SELECTORS[digit], Pin.OUT).on()

    utime.sleep_ms(DELAY_BETWEEN_DIGITS)


def show_current_set_score(pl1_games, pl2_games):

    # The points of the two players are divided in digits
    pl1_tens = int(list("0" + str(pl1_games))[-2])
    pl1_units = int(list("0" + str(pl1_games))[-1])
    pl2_tens = int(list("0" + str(pl2_games))[-2])
    pl2_units = int(list("0" + str(pl2_games))[-1])
    set_score = [pl1_tens, pl1_units, pl2_tens, pl2_units]

    # Display is cleared for longer so it is easy to understand is not the game score but the set one
    pins_initialization()
    utime.sleep_ms(DELAY_BETWEEN_GAMES)

    for ms in range(DELAY_BETWEEN_GAMES):
        for digit in range(4):
            if ((digit == 0 or digit == 2) and set_score[digit] != 0) or (digit == 1 or digit == 3):
                # Digit Selection
                Pin(DIGIT_SELECTORS[digit], Pin.OUT).off()

                # Show Number
                display_number(set_score[digit])

                # Show Decimal Point
                if digit == 1:
                    Pin(DECIMAL_POINT_PIN, Pin.OUT).on()

                # Sleep
                utime.sleep_ms(DELAY_BETWEEN_DIGITS)

                # Clear Decimal Point
                if digit == 1:
                    Pin(DECIMAL_POINT_PIN, Pin.OUT).off()

                # Clear Display
                for segment in DISPLAY_SEGMENTS:
                    Pin(segment, Pin.OUT).off()

                # Digit Deselection
                Pin(DIGIT_SELECTORS[digit], Pin.OUT).on()

    pins_initialization()
    utime.sleep_ms(DELAY_BETWEEN_GAMES)


if __name__ == '__main__':

    notify_power_on()
    pins_initialization()

    # Match Initialization
    player1_button = Pin(PLAYER1_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    player2_button = Pin(PLAYER2_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    player1_points = 0
    player1_games = 0
    player2_points = 0
    player2_games = 0

    try:
        while True:
            show_current_game_score(player1_points, player2_points)

            if player1_button.value() == 1:
                player1_points += 1

                # When a player scores a point, if his new score is 21 he won the game
                if player1_points == 21:
                    player1_games += 1
                    player1_points = 0
                    player2_points = 0

                    # Set score is then displayed
                    show_current_set_score(player1_games, player2_games)

                # After the click, the system waits so no multiple press are accidentally captured
                utime.sleep_ms(DELAY_BETWEEN_GAMES)

            if player2_button.value() == 1:
                player2_points += 1

                if player2_points == 21:
                    player2_games += 1
                    player1_points = 0
                    player2_points = 0

                    show_current_set_score(player1_games, player2_games)

                utime.sleep_ms(DELAY_BETWEEN_GAMES)

    except KeyboardInterrupt:
        pins_initialization()
        print("Script terminated by keyboard")
