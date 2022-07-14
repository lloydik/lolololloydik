# PPC tasks

## Follow me

### Условие

> Нет времени объяснять, следуй за мной.
>
> http://84.201.135.200:5010/ 

### Решение

Перейдя на сайт, мы видим сообщение `Go to /7a68`. Т.к. таск категории PPC, то мы просто напишем программу, которая будет следовать правилам этого сайта:
```python
import requests
uri = 'http://84.201.135.200:5010'
url = ''

while True:  # Пока не сломается
    resp = requests.get(uri + url).text
    url = resp.split()[-1]
    print(resp)
```

### Флаг

**shpctf{y0u_are_w3b_bruter}**

***

## QR challenge

### Условие

> Qr, они везде!!!!!!одын11!
nc 84.201.135.200 9999

### Решение

Здесь всё очевидно, надо просто написать программу для считывания qr-кода. Единственная проблема - символы ansi для изменения цвета в консоли, но они переводятся достаточно просто. Пример кода:

```python
from pyzbar.pyzbar import decode
import socket
from PIL import Image
import numpy as np

domain = ('84.201.135.200', 9999)
s = socket.socket()
s.connect(domain)
colors = {
    b'\x1b[100m\x1b[90m': b"00",
    b'\x1b[30m\x1b[40m': b"",
    b'\x1b[107m\x1b[97m': b"11",
    b'\x1b[97m\x1b[40m': b"\n"
}  # Словарь с заменой цвета в консоли на цвет в изображении

while True:  # Будет работать, пока не сломается
    data = s.recv(512000000)
    print(data.decode())
    data = data.replace(b'..', b'')  # Подчистка лишних символов

    for c in colors:
        data = data.replace(c, colors[c])
    arr = (b'\n'.join(data.split(b'/')[-1].split()[1:])).decode().split()  # Получаем только qr
    image_arr = []
    for a in arr:
        image_arr.append(a)
        image_arr.append(a)  # чтобы qr-код был квадратным и достаточно большим, чтобы его можно было счесть
    h = len(image_arr)
    w = len(image_arr[0])
    image_arr = np.array(list(''.join(image_arr)))
    image_arr = image_arr.reshape((h, w)).astype('uint8')*255

    img = Image.fromarray(image_arr)
    img.convert('1')
    qr = decode(img)  # Распознование qr
    print(qr)
    res = qr[0].data
    s.send(res)
```

### Флаг

**MSHP{4441cd7e6b665842bd3d8b390dd9c3aa}**
