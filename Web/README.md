# Web tasks

## Bad blog

### Условие

> Зацените какой бложик поднял.
http://84.201.135.200:7005

### Решение

Залетаем на сайт и регистрируемся. После этого заходим в куки и видим u_id, эта кука подсказывает нам, что наш user id = (какое-то число). Первым делом, что можно сделать - сменить u_id на 1, ведь админский аккаунт всегда первый. Меняем его и получаем флажок

### Флаг

**mshp{meh_t00_many_ways_t0_s0lv3_th1s_t4sk}**

***

## Эквестрия

### Условие

> Каждый имеет свое отражение в зеркале.
http://84.201.135.200:7002/

### Решение

Открываем сайт и видим форму. Первое, что пришло в голову - вставить кавычку. Но это действие ни к чему не привело. Т.к. кроме формы на сайте ничего нет, то нужно всё еще пытаться взаимодействовать с формой. Возможно в запросе используются не одинарные, а двойные кавычки? Если ввести такой payload в логин:
```
" OR 1=1 -- 
```
То мы получим флаг

### Флаг

**flag{w0w_y0u_know_it"?}**

***

## Hash Station

### Условие

> Эти современные технологии криптомайнинга уже и до нас добрались...
http://84.201.135.200:7007/

[Файл на сайте](files/hash_station/server.py)

### Решение

Открываем сайт и видим форму с сылкой на файл. Откроем файл. Нас интересует эта функция:
```python
@app.route('/hash/')
def get_hash():
    data = request.args.get('data', '') + flag
    result = ''
    for i in range(0, len(data), 8):
        block = hashlib.md5(data[i: i + 8].encode()).hexdigest() + "\n"
        result += block
    return result
```
Она конкатенирует введённую строку и флаг, потом берёт хэш от первых 8 символов и выводит хэш от них, потом берёт вторые 8 символов и выводит md5 от них и т.д.

Если ввести в форму 7 символов "a", то программа возьмёт 7 символов "a" и первую букву флага. Нам остаётся только перебрать её.

Напишем код, который достанет первую часть флага:
```python
import requests
import hashlib
from string import ascii_letters, punctuation, digits

url = 'http://84.201.135.200:7007/hash/?data='
alphabet = ascii_letters + punctuation + digits


def brute_letter(s: str, block_hash):
    for a in alphabet:
        h = hashlib.md5((s + a).encode()).hexdigest()
        if h == block_hash:
            return a


def get_block_hashes(s: str):
    return requests.get(url+s).text.strip().split()


def main():
    flag = ''

    for i in range(8):
        block_hash = get_block_hashes('a' * (7 - i))[0]
        payload = 'a' * (7 - i) + flag
        let = brute_letter(payload, block_hash)
        flag += let
    print(flag)
```

После этого допишем код, чтобы он доставал остальную часть флага:

```python
import requests
import hashlib
from string import ascii_letters, punctuation, digits

url = 'http://84.201.135.200:7007/hash/?data='
alphabet = ascii_letters + punctuation + digits


def brute_letter(s: str, block_hash):
    for a in alphabet:
        h = hashlib.md5((s + a).encode()).hexdigest()
        if h == block_hash:
            return a


def get_block_hashes(s: str):
    return requests.get(url + s).text.strip().split()


def main():
    flag = ''

    for i in range(8):
        block_hash = get_block_hashes('a' * (7 - i))[0]
        payload = 'a' * (7 - i) + flag
        let = brute_letter(payload, block_hash)
        flag += let

    for block_id in range(1, len(get_block_hashes(''))):
        block_flag = flag[-7:]  # Отсекаем лишнюю часть, чтобы хэшировать строку из 8-ми символов
        for i in range(8):
            payload = 'a' * (7 - (i % 8))  # Настраиваем отступ, чтобы достать нужный нам хэш
            block_hash = get_block_hashes(payload)[block_id]
            let = brute_letter(block_flag, block_hash)
            if not let:
                break  # Случайно был взят не тот хэш. Просто его пропустим
            block_flag = block_flag[1:] + let
            flag += let
    print(flag)


if __name__ == '__main__':
    main()

```

### Флаг

**MSHP{h@sh_my_m1nd_@nd_ThR0W_aWaY}**