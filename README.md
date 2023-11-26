# Контакты
### Имя: Петраков Владимир
### E-mail: v.petrakov@g.nsu.ru

# Запуск
```console
python main.py
```

# Обзор решения

## Классы
- ***RGBGame*** - класс, который содержажит игровую логику, а также хранит ходы и результат игры.

- ***Player*** - класс с текущем счетом игрока.

- ***Board*** - класс с характеристиками игровой доски, с текущем расположением шаров и массивом кластеров. Содержит интерфейс взамодействия с шарами и кластерами.

- ***Point*** - класс с координатами шара. Создан, чтобы уменьшить количество параметров методов других классов.

- ***Ball*** - класс с характеристиками шара. Содержит функционал сдвигов в определенную точку и сравнения шаров.

- ***Cluster*** - класс-обертка над массивом шаров. Содержит функционал выбора приоритетного шара в кластере и слияния двух кластеров в один.

- ***ClusterizationAlgorithm*** - класс, содержащий алгоритм определения кластеров. Совершается обход по игровой доске, для каждого шара создается отдельный кластер, после чего через интерфейс кластера происходит слияние со всеми возможными и уже построенными кластерами.

- ***CompressionAlgorithm*** - класс-фасад для алгоритмов преобразования игровой доски после удаления кластера.

- ***Compressor*** - Абстрактный класс сжатия (паттерн Шаблонный метод). Содержит базовый функционал для поиска шаров, которые необходимо сдвинуть после удаления кластера. Классы-потомки определают методы выборки необходимых начальных точек из удленного кластера для поиска сдвигаемых шаров, фиксации координаты для обхода и поиска, а также методы сдвига шаров.

- ***VerticallyCompressor*** - класс, содержащий алгоритм сжатия по вертикали. Необходимые начальные точки: минимальный x для каждого y в удаленном кластере. Для обхода и поиска фиксируем y.

- ***HorizontallyCompressor*** - класс, содержащий алгоритм сжатия по горизонтали. Необходимые начальные точки: такие x при y = 1, в которых (x - 1, y) лежит шар, а в (x, y) нет шара. Для обхода и поиска фиксируем x.

- ***ShiftRange*** - класс, содержащий размер сдвига и отрезок, который нужно сдвинуть (вторая координата фиксирована). Создан, чтобы уменьшить количество параметров методов других классов.

- ***Strategy*** - Абстрактный класс игровой стратегии. Задача стратегии: вернуть кластер, который удалится на текущем ходе.

- ***SimpleStrategy*** - класс, реализующий игровую стратегию, которая заключается в удалении самого большого кластера на текущем ходе. Если есть равныые по размеру кластеры, выбираем по приоритетному шару.

- ***Move*** - класс, содержащий информацию о ходе.

# Тесты
### Тесты производились на Python 3.11.5
- ### Тест 1:
    #### Ввод:
    ```
    1
    
    RBGRBGRBGRBGRBG
    BGRBGRBGRBGRBGR
    GRBGRBGRBGRBGRB
    RBGRBGRBGRBGRBG
    BGRBGRBGRBGRBGR
    GRBGRBGRBGRBGRB
    RBGRBGRBGRBGRBG
    BGRBGRBGRBGRBGR
    GRBGRBGRBGRBGRB
    RBGRBGRBGRBGRBG
    ```
    #### Вывод:
    ```
    Game 1:
    Final score: 0, with 150 balls remaining.
    ```
- ### Тест 2:
    #### Ввод:
    ```
    1
    
    RRRRRRRRRRRRRRR
    GGGGGGGGGGGGGGG
    RRRRRRRRRRRRRRR
    BBBBBBBBBBBBBBB
    GGGGGGGGGGGGGGG
    BBBBBBBBBBBBBBB
    RRRRRRRRRRRRRRR
    GGGGGGGGGGGGGGG
    RRRRRRRRRRRRRRR
    GGGGGGGGGGGGGGG
    ```
    #### Вывод:
    ```
    Game 1:
    Move 1 at (1,1): removed 15 balls of color G, got 169 points.
    Move 2 at (1,1): removed 15 balls of color R, got 169 points.
    Move 3 at (1,1): removed 15 balls of color G, got 169 points.
    Move 4 at (1,1): removed 15 balls of color R, got 169 points.
    Move 5 at (1,1): removed 15 balls of color B, got 169 points.
    Move 6 at (1,1): removed 15 balls of color G, got 169 points.
    Move 7 at (1,1): removed 15 balls of color B, got 169 points.
    Move 8 at (1,1): removed 15 balls of color R, got 169 points.
    Move 9 at (1,1): removed 15 balls of color G, got 169 points.
    Move 10 at (1,1): removed 15 balls of color R, got 169 points.
    Final score: 2690, with 0 balls remaining.
    ```
- ### Тест 3:
    #### Ввод:
    ```
    1
    
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    ```
    #### Вывод:
    ```
    Game 1:
    Move 1 at (1,12): removed 20 balls of color B, got 324 points.
    Move 2 at (1,11): removed 30 balls of color R, got 784 points.
    Move 3 at (1,1): removed 10 balls of color R, got 64 points.
    Move 4 at (1,1): removed 10 balls of color G, got 64 points.
    Move 5 at (1,1): removed 10 balls of color R, got 64 points.
    Move 6 at (1,1): removed 10 balls of color B, got 64 points.
    Move 7 at (1,1): removed 10 balls of color G, got 64 points.
    Move 8 at (1,1): removed 10 balls of color B, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Move 11 at (1,1): removed 10 balls of color R, got 64 points.
    Move 12 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 2748, with 0 balls remaining.
    ```
- ### Тест 4:
    #### Ввод:
    ```
    1
    
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRRRRR
    RGRBGBRGRGBBBRR
    ```
    #### Вывод:
    ```
    Game 1:
    Move 1 at (2,11): removed 31 balls of color R, got 841 points.
    Move 2 at (1,11): removed 19 balls of color B, got 289 points.
    Move 3 at (1,1): removed 10 balls of color R, got 64 points.
    Move 4 at (1,1): removed 10 balls of color G, got 64 points.
    Move 5 at (1,1): removed 10 balls of color R, got 64 points.
    Move 6 at (1,1): removed 10 balls of color B, got 64 points.
    Move 7 at (1,1): removed 10 balls of color G, got 64 points.
    Move 8 at (1,1): removed 10 balls of color B, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Move 11 at (1,1): removed 10 balls of color R, got 64 points.
    Move 12 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 2770, with 0 balls remaining.
    ```
- ### Тест 5:
    #### Ввод:
    ```
    1
    
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    BGRBGBRGRGRRRRR
    RBRBGBRGRGBBBRR
    ```
    #### Вывод:
    ```
    Game 1:
    Move 1 at (2,11): removed 31 balls of color R, got 841 points.
    Move 2 at (1,11): removed 19 balls of color B, got 289 points.
    Move 3 at (1,3): removed 10 balls of color R, got 64 points.
    Move 4 at (1,2): removed 11 balls of color B, got 81 points.
    Move 5 at (1,2): removed 19 balls of color G, got 289 points.
    Move 6 at (2,1): removed 11 balls of color B, got 81 points.
    Move 7 at (1,1): removed 19 balls of color R, got 289 points.
    Move 8 at (1,1): removed 10 balls of color G, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 3126, with 0 balls remaining.
    ```
- ### Тест 6:
    #### Ввод:
    ```
    1
    
    BGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    BGRBGBRGRGRRRRR
    RBRBGBRGRGBBBRR
    ```
    #### Вывод:
    ```
    Game 1:
    Move 1 at (2,11): removed 31 balls of color R, got 841 points.
    Move 2 at (1,11): removed 19 balls of color B, got 289 points.
    Move 3 at (1,3): removed 10 balls of color R, got 64 points.
    Move 4 at (1,2): removed 11 balls of color B, got 81 points.
    Move 5 at (1,2): removed 19 balls of color G, got 289 points.
    Move 6 at (2,1): removed 12 balls of color B, got 100 points.
    Move 7 at (1,1): removed 18 balls of color R, got 256 points.
    Move 8 at (1,1): removed 10 balls of color G, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 3112, with 0 balls remaining.
    ```
- ### Тест 7:
    #### Ввод:
    ```
    1
    
    RGGBBGGRBRRGGBG
    RBGRBGRBGRBGRBG
    RRRRGBBBRGGRBBB
    GGRGBGGBRRGGGBG
    GBGGRRRRRBGGRRR
    BBBBBBBBBBBBBBB
    BBBBBBBBBBBBBBB
    RRRRRRRRRRRRRRR
    RRRRRRGGGGRRRRR
    GGGGGGGGGGGGGGG
    ```
    #### Вывод:
    ```
    Game 1:
    Move 1 at (4,1): removed 32 balls of color B, got 900 points.
    Move 2 at (2,1): removed 39 balls of color R, got 1369 points.
    Move 3 at (1,1): removed 37 balls of color G, got 1225 points.
    Move 4 at (3,4): removed 11 balls of color B, got 81 points.
    Move 5 at (1,1): removed 8 balls of color R, got 36 points.
    Move 6 at (2,1): removed 6 balls of color G, got 16 points.
    Move 7 at (1,6): removed 6 balls of color B, got 16 points.
    Move 8 at (1,2): removed 5 balls of color R, got 9 points.
    Move 9 at (1,2): removed 5 balls of color G, got 9 points.
    Final score: 3661, with 1 balls remaining.
    ```
- ### Тест 8:
    #### Ввод:
    ```
    7

    RBGRBGRBGRBGRBG
    BGRBGRBGRBGRBGR
    GRBGRBGRBGRBGRB
    RBGRBGRBGRBGRBG
    BGRBGRBGRBGRBGR
    GRBGRBGRBGRBGRB
    RBGRBGRBGRBGRBG
    BGRBGRBGRBGRBGR
    GRBGRBGRBGRBGRB
    RBGRBGRBGRBGRBG

    RRRRRRRRRRRRRRR
    GGGGGGGGGGGGGGG
    RRRRRRRRRRRRRRR
    BBBBBBBBBBBBBBB
    GGGGGGGGGGGGGGG
    BBBBBBBBBBBBBBB
    RRRRRRRRRRRRRRR
    GGGGGGGGGGGGGGG
    RRRRRRRRRRRRRRR
    GGGGGGGGGGGGGGG

    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR

    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRRRRR
    RGRBGBRGRGBBBRR

    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    BGRBGBRGRGRRRRR
    RBRBGBRGRGBBBRR

    BGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    RGRBGBRGRGRBBRR
    BGRBGBRGRGRRRRR
    RBRBGBRGRGBBBRR
    
    RGGBBGGRBRRGGBG
    RBGRBGRBGRBGRBG
    RRRRGBBBRGGRBBB
    GGRGBGGBRRGGGBG
    GBGGRRRRRBGGRRR
    BBBBBBBBBBBBBBB
    BBBBBBBBBBBBBBB
    RRRRRRRRRRRRRRR
    RRRRRRGGGGRRRRR
    GGGGGGGGGGGGGGG
    ```
    #### Вывод:
    ```
    Game 1:
    Final score: 0, with 150 balls remaining.

    Game 2:
    Move 1 at (1,1): removed 15 balls of color G, got 169 points.
    Move 2 at (1,1): removed 15 balls of color R, got 169 points.
    Move 3 at (1,1): removed 15 balls of color G, got 169 points.
    Move 4 at (1,1): removed 15 balls of color R, got 169 points.
    Move 5 at (1,1): removed 15 balls of color B, got 169 points.
    Move 6 at (1,1): removed 15 balls of color G, got 169 points.
    Move 7 at (1,1): removed 15 balls of color B, got 169 points.
    Move 8 at (1,1): removed 15 balls of color R, got 169 points.
    Move 9 at (1,1): removed 15 balls of color G, got 169 points.
    Move 10 at (1,1): removed 15 balls of color R, got 169 points.
    Final score: 2690, with 0 balls remaining.

    Game 3:
    Move 1 at (1,12): removed 20 balls of color B, got 324 points.
    Move 2 at (1,11): removed 30 balls of color R, got 784 points.
    Move 3 at (1,1): removed 10 balls of color R, got 64 points.
    Move 4 at (1,1): removed 10 balls of color G, got 64 points.
    Move 5 at (1,1): removed 10 balls of color R, got 64 points.
    Move 6 at (1,1): removed 10 balls of color B, got 64 points.
    Move 7 at (1,1): removed 10 balls of color G, got 64 points.
    Move 8 at (1,1): removed 10 balls of color B, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Move 11 at (1,1): removed 10 balls of color R, got 64 points.
    Move 12 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 2748, with 0 balls remaining.

    Game 4:
    Move 1 at (2,11): removed 31 balls of color R, got 841 points.
    Move 2 at (1,11): removed 19 balls of color B, got 289 points.
    Move 3 at (1,1): removed 10 balls of color R, got 64 points.
    Move 4 at (1,1): removed 10 balls of color G, got 64 points.
    Move 5 at (1,1): removed 10 balls of color R, got 64 points.
    Move 6 at (1,1): removed 10 balls of color B, got 64 points.
    Move 7 at (1,1): removed 10 balls of color G, got 64 points.
    Move 8 at (1,1): removed 10 balls of color B, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Move 11 at (1,1): removed 10 balls of color R, got 64 points.
    Move 12 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 2770, with 0 balls remaining.

    Game 5:
    Move 1 at (2,11): removed 31 balls of color R, got 841 points.
    Move 2 at (1,11): removed 19 balls of color B, got 289 points.
    Move 3 at (1,3): removed 10 balls of color R, got 64 points.
    Move 4 at (1,2): removed 11 balls of color B, got 81 points.
    Move 5 at (1,2): removed 19 balls of color G, got 289 points.
    Move 6 at (2,1): removed 11 balls of color B, got 81 points.
    Move 7 at (1,1): removed 19 balls of color R, got 289 points.
    Move 8 at (1,1): removed 10 balls of color G, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 3126, with 0 balls remaining.

    Game 6:
    Move 1 at (2,11): removed 31 balls of color R, got 841 points.
    Move 2 at (1,11): removed 19 balls of color B, got 289 points.
    Move 3 at (1,3): removed 10 balls of color R, got 64 points.
    Move 4 at (1,2): removed 11 balls of color B, got 81 points.
    Move 5 at (1,2): removed 19 balls of color G, got 289 points.
    Move 6 at (2,1): removed 12 balls of color B, got 100 points.
    Move 7 at (1,1): removed 18 balls of color R, got 256 points.
    Move 8 at (1,1): removed 10 balls of color G, got 64 points.
    Move 9 at (1,1): removed 10 balls of color R, got 64 points.
    Move 10 at (1,1): removed 10 balls of color G, got 64 points.
    Final score: 3112, with 0 balls remaining.

    Game 7:
    Move 1 at (4,1): removed 32 balls of color B, got 900 points.
    Move 2 at (2,1): removed 39 balls of color R, got 1369 points.
    Move 3 at (1,1): removed 37 balls of color G, got 1225 points.
    Move 4 at (3,4): removed 11 balls of color B, got 81 points.
    Move 5 at (1,1): removed 8 balls of color R, got 36 points.
    Move 6 at (2,1): removed 6 balls of color G, got 16 points.
    Move 7 at (1,6): removed 6 balls of color B, got 16 points.
    Move 8 at (1,2): removed 5 balls of color R, got 9 points.
    Move 9 at (1,2): removed 5 balls of color G, got 9 points.
    Final score: 3661, with 1 balls remaining.
    ```