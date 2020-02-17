# Wire management

## Sourcemeter (white tape)

| Sourcemeter (big plugs) | Feedthrough | Small plugs | PCB  | Chip         |
| ----------------------- | ----------- | ----------- | ---- | ------------ |
| Black                   | Black       | Black       | 1    | Top left     |
| Yellow                  | Brown       | Yellow      | 5    | Bottom left  |
| Red                     | Orange      | Orange 2    | 8    | Top right    |
| Blue                    | Blue        | Blue        | 12   | Bottom right |

WO3196 (per 31/12/2019, correctie 17/02/2020)

| Sourcemeter (coax) | Feedthrough | Small plugs | PCB  | Chip                   |
| ------------------ | ----------- | ----------- | ---- | ---------------------- |
| 1                  | Black       | Black       | 1    | Top left (voltage)     |
| 2                  | Brown       | White       | 3    | Middle left (current)  |
| 3                  | Orange      | Orange 2    | 8    | Top right (voltage)    |
| 4                  | Blue        | Black       | 10   | Middle right (current) |

## Temperature controller (black tape)

| Controller | Feedthrough | Small plugs | PCB         | Devices |
| ---------- | ----------- | ----------- | ----------- | ------- |
| Sensor 1   | Orange      | Orange      | 2 (red)     | Pt1000  |
| Sensor 2   | Blue        | Green       | 4           | Pt1000  |
| Heater 1   | Black       | Green       | 9           | Heater  |
| Heater2    | Brown       | Red         | 11 (orange) | Heater  |

## PCB Layout

![1571393234125](C:\Users\LocalAdmin\AppData\Roaming\Typora\typora-user-images\1571393234125.png)         x

| PCB Number | Colour wire | Notes            |
| ---------- | ----------- | ---------------- |
| 1          | Black       | Tied to Orange 8 |
| 2          | Orange      | Red at PCB       |
| 3          | White       | -                |
| 4          | Green       | Tied to Orange 2 |
| 5          | Yellow      | Disconnected     |
| 6          | -           | -                |
| 7          | -           | -                |
| 8          | Orange      | Tied to Black 1  |
| 9          | Green       | Tied to Red 11   |
| 10         | Black       | Tied to White 3  |
| 11         | Red         | Orange at PCB    |
| 12         | Blue        | Disconnected     |

