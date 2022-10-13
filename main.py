from machine import UART, Pin, PWM, ADC
import time

bt = UART(0, 9600)
r = PWM(Pin(2))
g = PWM(Pin(3))
b = PWM(Pin(4))
cds = ADC(Pin(28))

is_on = False
is_auto = False
cmd = ''

c = [255, 255, 255]

def on(p):
    p = p / 100
    r.duty_u16(int(c[0] / 255 * 65025 * p))
    g.duty_u16(int(c[1] / 255 * 65025 * p))
    b.duty_u16(int(c[2] / 255 * 65025 * p))

def off():
    r.duty_u16(0)
    g.duty_u16(0)
    b.duty_u16(0)
    
def color(t):
    v = ''
    data = ''
    while not '!' in v:
        if bt.any():
            data = bt.readline()
            if not data == b'\x00':
                data = data.decode(('utf-8'))
                v += data
    print(t, v)
    try:
        c[t-1] = int(v[0:len(v)-1])
    except:
        pass
    if t < 3:
        color(t+1)
    else:
        print(c)
        print(is_on)
        if is_on:
            on(100)
    
while True:
    if is_on:
        if is_auto:
            on(int(cds.read_u16() / 65535 * 100))
            print('auto')
            time.sleep(0.5)
    if bt.any():
        data = bt.readline()
        if not data == b'\x00':
            data = data.decode(('utf-8'))
            print('received data:', data)
            cmd += data
            if '!' in cmd:
                print('cmd:', cmd)
                if 'on' in cmd:
                    is_on = True
                    on(100)
                elif 'off' in cmd:
                    is_on = False
                    off()
                elif 'color' in cmd:
                    color(1)
                elif 'noauto' in cmd:
                    is_auto = False
                elif 'auto' in cmd:
                    is_auto = True
                elif 'connected' in cmd:
                    is_auto = False
                cmd = ''
