class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.moved = False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, '♙' if color == 'white' else '♟')
    
    def get_moves(self, board, row, col):
        moves = []
        d = -1 if self.color == 'white' else 1
        start = 6 if self.color == 'white' else 1
        
        # Вперёд на 1
        if 0 <= row + d < 8 and board[row + d][col] is None:
            moves.append((row + d, col))
            # Вперёд на 2 с начальной позиции
            if row == start and board[row + 2*d][col] is None:
                moves.append((row + 2*d, col))
        
        # Взятие по диагонали
        for dc in [-1, 1]:
            nr, nc = row + d, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target and target.color != self.color:
                    moves.append((nr, nc))
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, '♖' if color == 'white' else '♜')
    
    def get_moves(self, board, row, col):
        moves = []
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r, c = r + dr, c + dc
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, '♘' if color == 'white' else '♞')
    
    def get_moves(self, board, row, col):
        moves = []
        for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, '♗' if color == 'white' else '♝')
    
    def get_moves(self, board, row, col):
        moves = []
        for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r, c = r + dr, c + dc
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, '♕' if color == 'white' else '♛')
    
    def get_moves(self, board, row, col):
        moves = []
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].color != self.color:
                        moves.append((r, c))
                    break
                r, c = r + dr, c + dc
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color, '♔' if color == 'white' else '♚')
    
    def get_moves(self, board, row, col):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))
        return moves

class Chess:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.turn = 'white'
        self.game_over = False
        self.setup()
    
    def


setup(self):
        # Пешки
        for i in range(8):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')
        # Фигуры
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, P in enumerate(order):
            self.board[0][i] = P('black')
            self.board[7][i] = P('white')
    
    def show(self):
        print('\n     a   b   c   d   e   f   g   h')
        print('   ┌───┬───┬───┬───┬───┬───┬───┬───┐')
        for r in range(8):
            print(f' {8-r} │', end='')
            for c in range(8):
                piece = self.board[r][c]
                sym = piece.symbol if piece else ' '
                print(f' {sym} │', end='')
            print(f' {8-r}')
            if r < 7:
                print('   ├───┼───┼───┼───┼───┼───┼───┼───┤')
        print('   └───┴───┴───┴───┴───┴───┴───┴───┘')
        print('     a   b   c   d   e   f   g   h\n')
        if not self.game_over:
            status = " БЕЛЫЕ" if self.turn == 'white' else " ЧЁРНЫЕ"
            print(f'   Ход: {status}')
            if self.is_in_check(self.turn):
                print(' ШАХ!')
        print()
    
    def parse(self, pos):
        if len(pos) != 2:
            return None
        c = ord(pos[0].lower()) - ord('a')
        try:
            r = 8 - int(pos[1])
        except:
            return None
        return (r, c) if 0 <= r < 8 and 0 <= c < 8 else None
    
    def format(self, r, c):
        return f"{chr(ord('a') + c)}{8 - r}"
    
    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and isinstance(p, King) and p.color == color:
                    return (r, c)
        return None
    
    def is_attacked(self, row, col, by_color):
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == by_color:
                    if (row, col) in p.get_moves(self.board, r, c):
                        return True
        return False
    
    def is_in_check(self, color):
        king = self.find_king(color)
        if not king:
            return False
        enemy = 'black' if color == 'white' else 'white'
        return self.is_attacked(king[0], king[1], enemy)
    
    def get_legal_moves(self, fr, fc):
        piece = self.board[fr][fc]
        if not piece:
            return []
        
        legal = []
        for tr, tc in piece.get_moves(self.board, fr, fc):
            # Делаем ход временно
            captured = self.board[tr][tc]
            self.board[tr][tc] = piece
            self.board[fr][fc] = None
            
            # Проверяем шах
            if not self.is_in_check(piece.color):
                legal.append((tr, tc))
            
            # Отменяем
            self.board[fr][fc] = piece
            self.board[tr][tc] = captured
        
        return legal
    
    def has_moves(self, color):
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == color:
                    if self.get_legal_moves(r, c):
                        return True
        return False
    
    def move(self, f, t):
        fr = self.parse(f)
        to = self.parse(t)
        
        if not fr or not to:
            return " Неверный формат (пример: e2 e4)"
        
        piece = self.board[fr[0]][fr[1]]
        
        if not piece:
            return " Пустая клетка"
        if piece.color != self.turn:
            return " Это не ваша фигура"
        
        legal = self.get_legal_moves(fr[0], fr[1])
        
        if to not in legal:
            if self.is_in_check(self.turn):
                return " Вы под шахом! Защитите короля"
            return " Так ходить нельзя"
        
        # Делаем ход
        captured = self.board[to[0]][to[1]]
        self.board[to[0]][to[1]] = piece
        self.board[fr[0]][fr[1]] = None
        piece.moved = True
        
        msg = f"✓ {f} →
Self
Self
self.is


{t}"
        if captured:
            msg += f" (взятие)"
        
        # Превращение пешки
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to[0] == 0) or \
               (piece.color == 'black' and to[0] == 7):
                self.board[to[0]][to[1]] = Queen(piece.color)
                msg += " Пешка → Ферзь!"
        
        # Смена хода
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        # Проверка конца игры
        if not self.has_moves(self.turn):
            if self.is_in_check(self.turn):
                winner = " БЕЛЫЕ" if self.turn == 'black' else " ЧЁРНЫЕ"
                msg += f"\n\n МАТ! {winner} ПОБЕДИЛИ!"
                self.game_over = True
            else:
                msg += "\n\n ПАТ! Ничья."
                self.game_over = True
        
        return msg
    
    def show_moves(self, pos):
        p = self.parse(pos)
        if not p:
            return "Неверная позиция"
        
        piece = self.board[p[0]][p[1]]
        if not piece:
            return "Пустая клетка"
        
        moves = self.get_legal_moves(p[0], p[1])
        if not moves:
            return "Нет доступных ходов"
        
        return "Ходы: " + ", ".join(self.format(r, c) for r, c in moves)

def main():
    game = Chess()
    
    print("\n" + "="*45)
    print("         ♔ ШАХМАТЫ В ТЕРМИНАЛЕ ♚")
    print("="*45)
    print("\n Команды:")
    print("   e2 e4    — сделать ход")
    print("   m e2     — показать ходы фигуры")
    print("   new      — новая игра")
    print("   q        — выход")
    print("\n Белые: ♔♕♖♗♘♙   Чёрные: ♚♛♜♝♞♟")
    print("="*45)
    
    while True:
        game.show()
        
        if game.game_over:
            inp = input(" Новая игра? (y/n): ").strip().lower()
            if inp == 'y':
                game = Chess()
                continue
            break
        
        try:
            inp = input(" Ход: ").strip().split()
        except (EOFError, KeyboardInterrupt):
            print("\n Выход...")
            break
        
        if not inp:
            continue
        
        cmd = inp[0].lower()
        
        if cmd in ['q', 'quit', 'exit']:
            print(" До свидания!")
            break
        
        if cmd == 'new':
            game = Chess()
            print(" Новая игра!")
            continue
        
        if cmd == 'm' and len(inp) == 2:
            print(" " + game.show_moves(inp[1]))
            continue
        
        if len(inp) == 2:
            result = game.move(inp[0], inp[1])
            print(f" {result}")
        else:
            print(" Формат: e2 e4 или m e2")

if __name__ == "__main__":
    main()










#доп задание 2
class Piece:
    """Базовый класс для фигуры (как в шахматах)"""
    def __init__(self, color, row, col):
        self.color = color  # 'W' для белых, 'B' для черных
        self.row = row
        self.col = col

class Checker(Piece):
    """Класс Шашки, наследующийся от Фигуры"""
    def can_move(self, target_row, target_col, board):
        # Простая проверка: ход по диагонали на 1 клетку
        row_diff = target_row - self.row
        col_diff = abs(target_col - self.col)
        
        # Направление движения (белые вверх, черные вниз)
        direction = -1 if self.color == 'W' else 1
        
        # Обычный ход
        if row_diff == direction and col_diff == 1:
            if board[target_row][target_col] is None:
                return True
        
        # Логика боя (прыжок через фигуру)
        if row_diff == 2 * direction and col_diff == 2:
            mid_row = self.row + direction
            mid_col = self.col + (1 if target_col > self.col else -1)
            mid_piece = board[mid_row][mid_col]
            if mid_piece and mid_piece.color != self.color and board[target_row][target_col] is None:
                return "capture"
        
        return False

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_checkers()

    def setup_checkers(self):
        # Расстановка черных (сверху) и белых (снизу)
        for r in range(3):
            for c in range(8):
                if (r + c) % 2 != 0: self.grid[r][c] = Checker('B', r, c)
        for r in range(5, 8):
            for c in range(8):
                if (r + c) % 2 != 0: self.grid[r][c] = Checker('W', r, c)

    def move(self, r1, c1, r2, c2):
        checker = self.grid[r1][c1]
        if not checker: return "Здесь нет фигуры!"
        
        result = checker.can_move(r2, c2, self.grid)
        if result:
            # Если это был бой, удаляем съеденную фигуру
            if result == "capture":
                mid_row, mid_col = (r1 + r2) // 2, (c1 + c2) // 2
                self.grid[mid_row][mid_col] = None
            
            # Перемещаем фигуру
            self.grid[r2][c2] = checker
            self.grid[r1][c1] = None
            checker.row, checker.col = r2, c2
            return "Ход выполнен"
        return "Неверный ход"

    def display(self):
        for row in self.grid:
            print('|' + '|'.join([p.color if p else ' ' for p in row]) + '|')

# Пример работы
game = Board()
print("Начальная доска:")
game.display()

# Пример хода: белая шашка с (5,2) на (4,3)
print("\nХод белых (5,2) -> (4,3):", game.move(5, 2, 4, 3))
game.display()









#доп задание 3
import sys

# --- КОНСТАНТЫ И КЛАССЫ ---

class HexCoord:
    """Класс для работы с кубическими координатами гексагональной сетки (x, y, z)"""
    def __init__(self, x, y, z):
        # В кубической системе сумма координат всегда равна 0
        assert x + y + z == 0, "Некорректные координаты гекса"
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return HexCoord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"

class Piece:
    """Шахматная фигура"""
    def __init__(self, color, type_char):
        self.color = color # 'w' (белые) или 'b' (черные)
        self.type = type_char # 'P', 'R', 'N', 'B', 'Q', 'K'
    
    def __str__(self):
        if self.color == 'w':
            return self.type
        else:
            return self.type.lower()

# --- ЛОГИКА ДОСКИ ---

class HexBoard:
    def __init__(self, size=5):
        # Размер доски (радиус). Для классических шахмат Глинского нужен radius=5 (11x11)
        self.radius = size
        self.grid = {} # Хранилище фигур: {(x,y,z): Piece}
        self._init_board()

    def _init_board(self):
        """Расстановка фигур по правилам Глинского (упрощенная для демонстрации)"""
        # Направления осей
        # X, Y, Z - это три оси гексагональной сетки
        
        # Расставим пешки и фигуры для белых (снизу) и черных (сверху)
        # Координаты подобраны для доски радиусом 5
        
        # Белые пешки (линия y=3)
        for x in range(-2, 3): # от -2 до 2
            self.grid[HexCoord(x, 3, -x-3)] = Piece('w', 'P')
        
        # Черные пешки (линия y=-3)
        for x in range(-2, 3):
            self.grid[HexCoord(x, -3, -x+3)] = Piece('b', 'P')

        # Белые фигуры (линия y=4)
        # Порядок: Ладья, Конь, Слон, Король, Слон, Конь, Ладья (адаптировано под гекс)
        # В Глинском расстановка специфическая, здесь упрощенный вариант "по центру"
        self.grid[HexCoord(0, 4, -4)] = Piece('w', 'K') # Король
        self.grid[HexCoord(-1, 4, -3)] = Piece('w', 'Q') # Ферзь
        self.grid[HexCoord(1, 4, -5)] = Piece('w', 'B') # Слон
        self.grid[HexCoord(-2, 4, -2)] = Piece('w', 'N') # Конь
        self.grid[HexCoord(2, 4, -6)] = Piece('w', 'N') # Конь
        self.grid[HexCoord(-3, 4, -1)] = Piece('w', 'R') # Ладья
        self.grid[HexCoord(3, 4, -7)] = Piece('w', 'R') # Ладья

        # Черные фигуры (зеркально)
        self.grid[HexCoord(0, -4, 4)] = Piece('b', 'K')
        self.grid[HexCoord(0, -4, 4)] = Piece('b', 'K') # Дубль для надежности в примере
        self.grid[HexCoord(0, -4, 4)] = Piece('b', 'K')
        # ... (для краткости кода расставим только королей и пешек, остальные аналогично)
        self.grid[HexCoord(0, -4, 4)] = Piece('b', 'K') 
        self.grid[HexCoord(-1, -4, 5)] = Piece('b', 'Q')
        self.grid[HexCoord(1, -4, 3)] = Piece('b', 'B')

    def get_moves(self, coord):
        """Возвращает список возможных ходов для фигуры в координате coord"""
        if coord not in self.grid:
            return []
        
        piece = self.grid[coord]
        moves = []
        
        # Базовые направления (6 сторон гекса)
        dirs = [
            HexCoord(1, 0, -1), HexCoord(1, -1, 0), HexCoord(0, -1, 1),
            HexCoord(-1, 0, 1), HexCoord(-1, 1, 0), HexCoord(0, 1, -1)
        ]
        
        # Логика для Пешки (упрощенная: ходит вперед по оси Y)
        if piece.type == 'P':
            direction = 1 if piece.color == 'w' else -1 # Белые идут в +Y, черные в -Y
            # Шаг вперед на 1
            target = coord + HexCoord(0, direction, -direction)
            if self._is_valid(target) and target not in self.grid:
                moves.append(target)
            # Шаг вперед на 2 (только со старта)
            start_y = 3 if piece.color == 'w' else -3
            if coord.y == start_y:
                target2 = coord + HexCoord(0, direction*2, -direction*2)
                if self._is_valid(target2) and target2 not in self.grid:
                    moves.append(target2)
            # Взятие (диагонали вперед)
            attack_dirs = [HexCoord(1, 0, -1), HexCoord(-1, 0, 1)] # Упрощенно
            # В гексах у пешки 2 направления атаки
            # Реализуем просто проверку соседних клеток по диагонали
            
        # Логика для Ладьи (движение по осям X, Y, Z)
        elif piece.type == 'R':
            for d in dirs:
                # Ладья ходит по 3 осям, это 6 направлений
                curr = coord
                while True:
                    curr = curr + d
                    if not self._is_valid(curr): break
                    if curr in self.grid:
                        if self.grid[curr].color != piece.color:
                            moves.append(curr) # Взятие
                        break # Блок фигурой
                    moves.append(curr) # Свободная клетка

        # Логика для Слона (движение по диагоналям между осями)
        elif piece.type == 'B':
            # Диагональные направления (между основными осями)
            diag_dirs = [
                HexCoord(1, 1, -2), HexCoord(2, -1, -1), HexCoord(1, -2, 1),
                HexCoord(-1, -1, 2), HexCoord(-2, 1, 1), HexCoord(-1, 2, -1)
            ]
            for d in diag_dirs:
                curr = coord
                while True:
                    curr = curr + d
                    if not self._is_valid(curr): break
                    if curr in self.grid:
                        if self.grid[curr].color != piece.color:
                            moves.append(curr)
                        break
                    moves.append(curr)
                    
        return moves

    def _is_valid(self, coord):
        """Проверка, находится ли клетка в пределах доски (радиус)"""
        return (abs(coord.x) <= self.radius and 
                abs(coord.y) <= self.radius and 
                abs(coord.z) <= self.radius)

    def render(self):
        """Отрисовка доски в ASCII"""
        print("\n--- ГЕКСАГОНАЛЬНЫЕ ШАХМАТЫ (Вид сверху, упрощенно) ---")
        print("Координаты: (x, y, z). Белые (заглавные), Черные (строчные)\n")
        
        # Проходим по Y от максимума к минимуму (сверху вниз)
        for y in range(self.radius, -self.radius - 1, -1):
            # Отступ для сдвига строк (чтобы было похоже на гексы)
            indent = " " * (self.radius - y) 
            line = indent
            
            # X меняется в зависимости от Y
            x_start = max(-self.radius, -self.radius - y)
            x_end = min(self.radius, self.radius - y)
            
            for x in range(x_start, x_end + 1):
                z = -x - y
                coord = HexCoord(x, y, z)
                
                if coord in self.grid:
                    line += f"[{self.grid[coord]}] "
                else:
                    line += "[ . ] "
            print(line)
        print("-" * 40)

# --- ЗАПУСК ---

if __name__ == "__main__":
    # Создаем доску радиусом 5 (классический размер 11x11)
    board = HexBoard(size=5)
    
    # 1. Рисуем доску
    board.render()
    
    # 2. Демонстрация работы логики ходов
    # Найдем белую пешку и покажем, куда она может пойти
    example_coord = HexCoord(0, 3, -3) # Координата центральной белой пешки
    
    if example_coord in board.grid:
        piece = board.grid[example_coord]
        print(f"\nФигура в {example_coord}: {piece}")
        moves = board.get_moves(example_coord)
        print(f"Возможные ходы: {moves}")
    else:
        print("\nФигура не найдена в тестовой координате.")
