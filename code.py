import keypad
import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

time.sleep(1)
# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

# 8 Rows 5 Columns
km = keypad.KeyMatrix(
    row_pins=(board.GP5, board.GP6, board.GP7, board.GP8, board.GP9,board.GP10, board.GP11, board.GP12),
    column_pins=(board.GP0, board.GP1, board.GP2, board.GP3, board.GP4),
)

key_ZX81 = {0 : Keycode.FIVE,
            1 : Keycode.FOUR,
            2 : Keycode.THREE,
            3 : Keycode.TWO,
            4 : Keycode.ONE,
            
            5 : Keycode.T,
            6 : Keycode.R,
            7 : Keycode.E,
            8 : Keycode.W,
            9 : Keycode.Q,

            10 : Keycode.SIX,
            11 : Keycode.SEVEN,
            12 : Keycode.EIGHT,
            13 : Keycode.NINE,
            14 : Keycode.ZERO,
            
            15 : Keycode.G,
            16 : Keycode.F,
            17 : Keycode.D,
            18 : Keycode.S,
            19 : Keycode.A,
            
            20 : Keycode.Y,
            21 : Keycode.U,
            22 : Keycode.I,
            23 : Keycode.O,
            24 : Keycode.P,
            
            25 : Keycode.V,
            26 : Keycode.C,
            27 : Keycode.X,
            28 : Keycode.Z,
            29 : Keycode.LEFT_SHIFT,

            30 : Keycode.H,
            31 : Keycode.J,
            32 : Keycode.K,
            33 : Keycode.L,
            34 : Keycode.ENTER,
            
            35 : Keycode.B,
            36 : Keycode.N,
            37 : Keycode.M,
            38 : Keycode.PERIOD,
            39 : Keycode.SPACE,
           }
# Create an event we will reuse
event = keypad.Event()

#print ("Starting...")
shift = False       # True if shift pressed
comma = False       # True if comma sent instead of shift period

while True:
    if km.events.get_into(event):
        # Convert the event to a specific key
        key_code = key_ZX81.get(event.key_number, 0)
        
        if key_code != 0:
            if event.pressed:
                # Need to translate shift period to comma
                if key_code == Keycode.LEFT_SHIFT:
                    shift = True
                if key_code == Keycode.PERIOD and shift:
                    comma = True
                    # Release shift and send comma
                    kbd.release(Keycode.LEFT_SHIFT)
                    kbd.press(Keycode.COMMA)
                else:
                    kbd.press(key_code)
            else:
                if key_code == Keycode.LEFT_SHIFT:
                    shift = False
                if key_code == Keycode.PERIOD and comma:
                    comma = False
                    kbd.release(Keycode.COMMA)
                    #Restore the shift state if needed
                    if shift:
                        kbd.press(Keycode.LEFT_SHIFT)
                else:
                    kbd.release(key_code)
