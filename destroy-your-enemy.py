"""
DESTROY YOUR ENEMY
battle with the enemy player's naval ship and destroy their ship.
your ship is the pixel in the bottom, opponent's ship is at the top.
navigate by pressing buttons A and B.
press buttons A and B at the same time to shoot.
the ship will be destroyed when it gets three hits.
communication is implemented via the radio module.
"""

from microbit import *
import radio

radio.on()

game_speed = 50  # milliseconds between game steps
reload_delay = 30  # game steps for a reload
header_bytes = b'navy'  # header prepended to avoid interference
pos_self, pos_enemy = 2, 2
shoot_self, shoot_enemy = None, None
reload_delay_self, reload_delay_enemy = 0, 0
health_self, health_enemy = 3, 3

def send_valid(packet):
    # transmit data with header bytes prepended to it
    radio.send_bytes(header_bytes + packet)

def receive_valid():
    # validate received data and return stripped data
    data_raw = radio.receive_bytes()
    if data_raw is not None and data_raw.startswith(header_bytes):
        return data_raw[len(header_bytes):]
    else:
        return None

def show_explosion(init_x, init_y):
    # display explosion when a ship is detroyed
    display.set_pixel(init_x, init_y, 9)
    for radius in range(8):
        for x in range(5):
            for y in range(5):
                if ((x - init_x)**2 + (y - init_y)**2)**0.5 <= radius:
                    display.set_pixel(x, y, 9)
        radius += 1
        sleep(50)
    # fade out the explosion
    for i in range(7):
        for x in range(5):
            for y in range(5):
                display.set_pixel(x, y, 8-i)
        sleep(50)
    display.clear()

def draw_ships():
    # draw the ships
    global self_brightness, other_brightness
    display.clear()
    if reload_delay_self > 0: self_brightness = 5
    else: self_brightness = 9
    if reload_delay_enemy > 0: other_brightness = 5
    else: other_brightness = 9
    display.set_pixel(pos_self, 4, self_brightness)
    display.set_pixel(4 - pos_enemy, 0, other_brightness)

def receive_data():
    # receive data from the other player
    global shoot_enemy, reload_delay_enemy, pos_enemy
    data = receive_valid()
    if data is not None:
        # if decodes to a numeric position, move the enemy
        if 0 <= ord(data) <= 4:
            pos_enemy = ord(data)
        # if shoot byte is received, initialize sequence
        elif data == b'\xf1':
            shoot_enemy = (4 - pos_enemy, 0)
            reload_delay_enemy = reload_delay

# pair with the enemy player
connecting_shown = False
while True:
    sleep(100)
    if receive_valid() == b'\xf0':
        send_valid(b'\xf0')
        display.scroll("GO", delay=80)
        break
    else:
        if connecting_shown is False:
            display.scroll("CONNECTING", delay=80, wait=False)
            connecting_shown = True
        send_valid(b'\xf0')

# main loop
while True:
    # shoot if two buttons are pressed
    if button_a.is_pressed() and button_b.is_pressed():
        button_a.get_presses()
        button_b.get_presses()
        if reload_delay_self == 0:
            send_valid(b'\xf1')
            shoot_self = (pos_self, 4)
            reload_delay_self = reload_delay
    # move left if button A is pressed
    elif not(button_a.is_pressed()) and button_a.get_presses():
        pos_self = max(pos_self - 1, 0)
        send_valid(bytes([pos_self]))
    # move right if button B is pressed
    elif not(button_b.is_pressed()) and button_b.get_presses():
        pos_self = min(pos_self + 1, 4)
        send_valid(bytes([pos_self]))
    receive_data()
    draw_ships()
    # handle self shoot
    if shoot_self is not None:
        display.set_pixel(shoot_self[0], shoot_self[1], 9)
        shoot_self = shoot_self[0], shoot_self[1] - 1
        if shoot_self[1] < 0:
            if shoot_self[0] == 4 - pos_enemy:
                health_enemy -= 1
                if health_enemy == 0:
                    show_explosion(4 - pos_enemy, 0)
                    display.scroll("YOU WIN", delay=80)
                    break
            shoot_self = None
    # handle enemy shoot
    if shoot_enemy is not None:
        display.set_pixel(shoot_enemy[0], shoot_enemy[1], 9)
        shoot_enemy = shoot_enemy[0], shoot_enemy[1] + 1
        if shoot_enemy[1] == 4:
            if shoot_enemy[0] == pos_self:
                health_self -= 1
                if health_self == 0:
                    show_explosion(pos_self, 4)
                    display.scroll("YOU LOSE", delay=80)
                    break
            shoot_enemy = None
    # decrement reload delays
    if reload_delay_self > 0: reload_delay_self -= 1
    if reload_delay_enemy > 0: reload_delay_enemy -= 1
    sleep(game_speed)