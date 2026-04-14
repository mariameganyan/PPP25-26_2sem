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

# --- Пример работы ---
game = Board()
print("Начальная доска:")
game.display()

# Пример хода: белая шашка с (5,2) на (4,3)
print("\nХод белых (5,2) -> (4,3):", game.move(5, 2, 4, 3))
game.display()
