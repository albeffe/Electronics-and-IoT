import utime
from machine import Pin
from machine import I2C
from pico_i2c_lcd import I2cLcd

DELAY_AFTER_BUTTON_PRESS = 500
PLAYER1_BUTTON_PIN = 15
PLAYER2_BUTTON_PIN = 2
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20


def power_on_routine():
    # Onboard led signal
    onboard_led = Pin(25, Pin.OUT)
    enabled = False

    for i in range(10):
        if enabled:
            onboard_led.off()
        else:
            onboard_led.on()
        utime.sleep_ms(125)
        enabled = not enabled

    # Lcd initialization
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    lcd.clear()
    return lcd


def make_lcd_string(pl_number, pts, games):
    lcd_string = "PL" + str(pl_number) + "     " + str(pts) + "    " + str(games)
    return lcd_string


def display_score(lcd, pl1_pts, pl1_games, pl2_pts, pl2_games):
    lcd.clear()
    lcd.move_to(0, 0)  # First Row
    lcd.putstr(make_lcd_string(1, pl1_pts, pl1_games))
    lcd.move_to(0, 1)  # Second Row
    lcd.putstr(make_lcd_string(2, pl2_pts, pl2_games))


if __name__ == '__main__':

    lcd_screen = power_on_routine()

    # Match Initialization
    player1_button = Pin(PLAYER1_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    player2_button = Pin(PLAYER2_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    player1_points = 0
    player1_games = 0
    player2_points = 0
    player2_games = 0

    display_score(lcd_screen, player1_points, player1_games, player2_points, player2_games)

    while True:
        if player1_button.value() == 1:
            player1_points += 1

            # When a player scores a point, if his new score is 21 he won the game
            if player1_points == 21:
                player1_games += 1
                player1_points = 0
                player2_points = 0

            display_score(lcd_screen, player1_points, player1_games, player2_points, player2_games)

            # After the click, the system waits so no multiple press are accidentally captured
            utime.sleep_ms(DELAY_AFTER_BUTTON_PRESS)

        if player2_button.value() == 1:
            player2_points += 1

            if player2_points == 21:
                player2_games += 1
                player1_points = 0
                player2_points = 0

            display_score(lcd_screen, player1_points, player1_games, player2_points, player2_games)

            utime.sleep_ms(DELAY_AFTER_BUTTON_PRESS)
