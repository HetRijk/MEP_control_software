# Wire management

## Sourcemeter (white tape)

WO3196 (per 2020/03/24, device 9)

| Sourcemeter (coax) | Feedthrough | Small plugs | PCB  | Chip |
| ------------------ | ----------- | ----------- | ---- | ---- |
| 1                  | Brown       | Yellow      | 5    | I+   |
| 2                  | Black       | Orange      | 8    | I-   |
| 3                  | Orange      | Blue        | 12   | V+   |
| 4                  | Blue        | Black       | 10   | V-   |

## Temperature controller (black tape)

| Controller | Feedthrough | Small plugs | PCB         | Devices |
| ---------- | ----------- | ----------- | ----------- | ------- |
| Sensor 1   | Orange      | Orange      | 2 (red)     | Pt1000  |
| Sensor 2   | Blue        | Green       | 4           | Pt1000  |
| Heater 1   | Black       | Green       | 9           | Heater  |
| Heater2    | Brown       | Red         | 11 (orange) | Heater  |

## PCB Layout

![1571393234125](C:\Users\LocalAdmin\AppData\Roaming\Typora\typora-user-images\1571393234125.png)         x

| PCB Number | Colour wire | Notes                   |
| ---------- | ----------- | ----------------------- |
| 1          | Black       | Tied to Orange 8        |
| 2          | Orange      | Red at PCB              |
| 3          | White       | Detached per 2020/24/03 |
| 4          | Green       | Tied to Orange 2        |
| 5          | Yellow      | Tied to Blue 12         |
| 6          | -           | -                       |
| 7          | -           | -                       |
| 8          | Orange      | Tied to Black 1         |
| 9          | Green       | Tied to Red 11          |
| 10         | Black       | Tied to White 3         |
| 11         | Red         | Orange at PCB           |
| 12         | Blue        | Tied to Yellow 5        |

 