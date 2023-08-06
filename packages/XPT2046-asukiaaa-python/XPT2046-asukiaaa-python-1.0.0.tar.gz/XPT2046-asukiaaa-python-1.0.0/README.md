# XPT2046_asukiaaa_python

Python library for XPT2046 Touchscreen.
This library references [Luca8991/XPT2046-Python](https://github.com/Luca8991/XPT2046-Python) and [Adafruit_CircuitPython_RGB_Display](https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display).

## Usage

### Enable SPI for Raspberry Pi

```sh
sudo raspi-config nonint do_spi 0
```

No need to reboot.

### Wiring

| Raspberri Pi  | <--> | XPT2046 |
| :------------ |:---------------:| -----:|
| MOSI (GPIO10) | <--> | DIN |
| MISO (GPIO9) | <--> | DO |
| SCLK (GPIO11) | <--> | CLK |
| GPIO7 or any | <--> | CS |
| 3V3 | <--> | VCC |
| GND | <--> | GND |

This library does not use IRQ pin.

Code, same as in [tests/print_touch.py](https://github.com/asukiaaa/XPT2046_asukiaaa_python/blob/main/tests/print_touch.py) file:

```py
from XPT2046_asukiaaa_python import XPT2046
import board
import busio
from digitalio import DigitalInOut
from time import sleep

cs = DigitalInOut(board.D7)
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
touch = XPT2046(spi, cs=cs)

print("start monitoring touch")

while True:
    touch.update()
    if touch.coordinate is not None:
        print(touch.coordinate)
    sleep(.01)
```

## License

MIT

## References

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
