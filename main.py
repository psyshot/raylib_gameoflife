import pyray
import random
from typing import List, Tuple

CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

class GameOfLife:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.running = False

    def randomize(self):
        """随机初始化细胞状态"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = random.choice([0, 1])

    def clear(self):
        """清空所有细胞"""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0

    def count_neighbors(self, x: int, y: int) -> int:
        """计算某位置的邻居数量"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                count += self.grid[ny][nx]
        return count

    def update(self):
        """根据康威生命游戏规则更新网格"""
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)

                if self.grid[y][x] == 1:
                    if neighbors == 2 or neighbors == 3:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
                else:
                    if neighbors == 3:
                        new_grid[y][x] = 1

        self.grid = new_grid

    def toggle_cell(self, x: int, y: int):
        """切换细胞状态"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 - self.grid[y][x]

    def draw(self):
        """绘制网格"""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    pyray.draw_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1,
                        pyray.DARKGREEN
                    )

def draw_ui(game: GameOfLife, generation: int):
    """绘制用户界面"""
    pyray.draw_rectangle(0, 0, WINDOW_WIDTH, 40, pyray.GRAY)

    controls = [
        f"Generation: {generation}",
        "[SPACE] Play/Pause",
        "[R] Randomize",
        "[C] Clear",
        "[S] Step",
        "[ESC] Quit"
    ]

    x_offset = 10
    for control in controls:
        pyray.draw_text(control, x_offset, 10, 16, pyray.BLACK)
        x_offset += pyray.measure_text(control, 16) + 30

def get_grid_pos(mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
    """将鼠标位置转换为网格坐标"""
    x = mouse_pos[0] // CELL_SIZE
    y = (mouse_pos[1] - 40) // CELL_SIZE if mouse_pos[1] >= 40 else -1
    return (x, y)

def main():
    pyray.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Conway's Game of Life")
    pyray.set_target_fps(FPS)

    game = GameOfLife(GRID_WIDTH, GRID_HEIGHT)
    game.randomize()

    generation = 0
    auto_play = False

    while not pyray.window_should_close():
        pyray.begin_drawing()

        pyray.clear_background(pyray.LIGHTGRAY)

        draw_ui(game, generation)
        pyray.draw_line(0, 40, WINDOW_WIDTH, 40, pyray.BLACK)

        mouse_pos = pyray.get_mouse_position()
        grid_x, grid_y = get_grid_pos((int(mouse_pos.x), int(mouse_pos.y)))

        if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_LEFT):
            if grid_y >= 0:
                game.toggle_cell(grid_x, grid_y)

        if pyray.is_key_pressed(pyray.KEY_SPACE):
            auto_play = not auto_play

        if pyray.is_key_pressed(pyray.KEY_R):
            game.randomize()
            generation = 0
            auto_play = False

        if pyray.is_key_pressed(pyray.KEY_C):
            game.clear()
            generation = 0
            auto_play = False

        if pyray.is_key_pressed(pyray.KEY_S):
            game.update()
            generation += 1

        if auto_play:
            game.update()
            generation += 1

        game.draw()

        pyray.end_drawing()

    pyray.close_window()

if __name__ == "__main__":
    main()
