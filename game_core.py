from levels import LEVELS

class Arrow:
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.dir = direction  # 0上 1右 2下 3左
        self.active = True   # 是否存在棋盘上
        self.shake = False   # 碰撞晃动标记

class GameCore:
    def __init__(self):
        self.level_idx = 0
        self.max_mistake = 3
        self.mistake = 0
        self.arrows = []
        self.load_level(self.level_idx)

    def load_level(self, level_num):
        """加载关卡，重置箭头、失误次数"""
        # 把关卡导入放在函数内部，避免头部循环导入！
        from levels import LEVELS
        self.levels = LEVELS
        
        self.mistake = 0
        self.arrows = []
        data = self.levels[level_num]
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                if val is not None:
                    self.arrows.append(Arrow(r, c, val))

    def get_arrow_at(self, r, c):
        for arr in self.arrows:
            if arr.active and arr.row == r and arr.col == c:
                return arr
        return None

    def check_block(self, arrow:Arrow):
        """路径检测：判断箭头前方有没有阻挡的箭头
        return True=有阻挡；False=无阻挡，可以飞出
        """
        dr, dc = 0,0
        if arrow.dir == 0: dr = -1
        elif arrow.dir ==1: dc = 1
        elif arrow.dir ==2: dr = 1
        elif arrow.dir ==3: dc = -1
        r = arrow.row + dr
        c = arrow.col + dc
        
        # 使用self.levels，不再直接引用全局LEVELS
        max_r = len(self.levels[self.level_idx])
        max_c = len(self.levels[self.level_idx][0])
        
        while 0 <= r < max_r and 0 <= c < max_c:
            a = self.get_arrow_at(r,c)
            if a is not None:
                return True
            r += dr
            c += dc
        return False

    def click_arrow(self, row, col):
        arr = self.get_arrow_at(row, col)
        if arr is None:
            return
        blocked = self.check_block(arr)
        if blocked:
            # 被阻挡，失误+1，触发晃动
            self.mistake += 1
            arr.shake = True
            return "block"
        else:
            # 无阻挡，消除箭头
            arr.active = False
            return "remove"

    def count_remaining(self):
        cnt = 0
        for a in self.arrows:
            if a.active:
                cnt +=1
        return cnt

    def is_win(self):
        return self.count_remaining() == 0

    def is_lose(self):
        return self.mistake >= self.max_mistake

    def next_level(self):
        # 内部导入关卡数据
        from levels import LEVELS
        self.levels = LEVELS
        
        self.level_idx +=1
        if self.level_idx >= len(self.levels):
            return True #全部通关
        self.load_level(self.level_idx)
        return False

# 兼容main.py里 from game_core import Game
Game = GameCore
