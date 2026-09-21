# levels.py
# 方向：0上 1右 2下 3左，None=空格子
LEVELS = [
    # 第1关（入门）
    [
        [None, 1, None, None],
        [None, None, None, 0],
        [3, None, None, None],
        [None, None, 2, None]
    ],
    # 第2关
    [
        [1, None, None, None],
        [None, None, 0, None],
        [None, 3, None, None],
        [None, None, None, 2]
    ],
    # 第3关（难度提升）
    [
        [None, 1, None, 0],
        [3, None, None, None],
        [None, None, 2, None],
        [0, None, None, 1]
    ]
]

# 方向字符映射，用于调试
DIR_CHAR = {0:"↑",1:"→",2:"↓",3:"←"}
