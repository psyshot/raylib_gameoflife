import pyray
from typing import List, Tuple

CELL_SIZE = 6
GRID_WIDTH = 140
GRID_HEIGHT = 100
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 60

# 方向：上、右、下、左（顺时针）
# 0=上, 1=右, 2=下, 3=左
DX = [0, 1, 0, -1]
DY = [-1, 0, 1, 0]

# 颜色调色板（支持多色扩展）
COLORS = [
    pyray.RAYWHITE,       # 0: 空白
    pyray.BLACK,          # 1: 已访问
]


class LangtonsAnt:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        # 蚂蚁起始位置：网格中心
        self.ant_x = width // 2
        self.ant_y = height // 2
        self.ant_dir = 0  # 初始朝上
        self.steps = 0

    def reset(self):
        """重置网格和蚂蚁"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0
        self.ant_x = self.width // 2
        self.ant_y = self.height // 2
        self.ant_dir = 0
        self.steps = 0

    def step(self):
        """执行一步兰顿蚂蚁规则"""
        # 获取当前格子的状态
        current_state = self.grid[self.ant_y][self.ant_x]

        if current_state == 0:
            # 白色格子：右转（顺时针）
            self.ant_dir = (self.ant_dir + 1) % 4
        else:
            # 黑色格子：左转（逆时针）
            self.ant_dir = (self.ant_dir - 1) % 4

        # 翻转当前格子颜色
        self.grid[self.ant_y][self.ant_x] = 1 - current_state

        # 向前移动一步（循环边界）
        self.ant_x = (self.ant_x + DX[self.ant_dir]) % self.width
        self.ant_y = (self.ant_y + DY[self.ant_dir]) % self.height

        self.steps += 1

    def draw(self):
        """绘制网格和蚂蚁"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    px = x * CELL_SIZE
                    py = y * CELL_SIZE
                    pyray.draw_rectangle(px, py, CELL_SIZE, CELL_SIZE, COLORS[1])

        # 绘制蚂蚁（红色高亮）
        ant_px = self.ant_x * CELL_SIZE
        ant_py = self.ant_y * CELL_SIZE
        pyray.draw_rectangle(ant_px, ant_py, CELL_SIZE, CELL_SIZE, pyray.RED)


def draw_ui(ant: LangtonsAnt, auto_play: bool, speed: int):
    """绘制用户界面"""
    pyray.draw_rectangle(0, 0, WINDOW_WIDTH, 36, pyray.GRAY)

    controls = [
        f"Steps: {ant.steps}",
        f"Speed: {speed}",
        f"[{'RUNNING' if auto_play else 'PAUSED'}]",
        "[SPACE] Play/Pause",
        "[S] Step",
        "[UP/DOWN] Speed",
        "[R] Reset",
        "[ESC] Quit",
    ]

    x_offset = 10
    for control in controls:
        pyray.draw_text(control, x_offset, 10, 14, pyray.BLACK)
        x_offset += pyray.measure_text(control, 14) + 20


def main():
    pyray.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Langton's Ant")
    pyray.set_target_fps(FPS)

    ant = LangtonsAnt(GRID_WIDTH, GRID_HEIGHT)

    auto_play = False
    speed = 1  # 每帧执行的步数

    while not pyray.window_should_close():
        pyray.begin_drawing()

        pyray.clear_background(pyray.RAYWHITE)

        draw_ui(ant, auto_play, speed)
        pyray.draw_line(0, 36, WINDOW_WIDTH, 36, pyray.BLACK)

        # 键盘控制
        if pyray.is_key_pressed(pyray.KEY_SPACE):
            auto_play = not auto_play

        if pyray.is_key_pressed(pyray.KEY_R):
            ant.reset()
            auto_play = False

        if pyray.is_key_pressed(pyray.KEY_S):
            ant.step()

        if pyray.is_key_pressed(pyray.KEY_UP):
            speed = min(speed * 2 if speed >= 1 else 1, 8192)
        if pyray.is_key_pressed(pyray.KEY_DOWN):
            speed = max(speed // 2, 1)

        # 自动播放：每帧执行多步以加速
        if auto_play:
            for _ in range(speed):
                ant.step()

        ant.draw()

        pyray.end_drawing()

    pyray.close_window()


if __name__ == "__main__":
    main()
