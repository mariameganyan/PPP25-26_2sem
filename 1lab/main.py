class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P' if color == 'white' else 'p')
    
    def can_move(self, board, fr, fc, tr, tc):
        d = -1 if self.color == 'white' else 1
        if fc == tc and board[tr][tc] is None:
            return tr == fr + d
        if abs(tc - fc) == 1 and tr == fr + d:
            return board[tr][tc] and board[tr][tc].color != self.color
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R' if color == 'white' else 'r')
    
    def can_move(self, board, fr, fc, tr, tc):
        if fr != tr and fc != tc:
            return False
        if fr == tr:
            step = 1 if tc > fc else -1
            for c in range(fc + step, tc, step):
                if board[tr][c]:
                    return False
        else:
            step = 1 if tr > fr else -1
            for r in range(fr + step, tr, step):
                if board[r][tc]:
                    return False
        target = board[tr][tc]
        return target is None or target.color != self.color

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N' if color == 'white' else 'n')
    
    def can_move(self, board, fr, fc, tr, tc):
        dr, dc = abs(tr - fr), abs(tc - fc)
        if (dr, dc) not in [(1,2), (2,1)]:
            return False
        target = board[tr][tc]
        return target is None or target.color != self.color

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B' if color == 'white' else 'b')
    
    def can_move(self, board, fr, fc, tr, tc):
        if abs(tr - fr) != abs(tc - fc):
            return False
        sr = 1 if tr > fr else -1
        sc = 1 if tc > fc else -1
        r, c = fr + sr, fc + sc
        while (r, c) != (tr, tc):
            if board[r][c]:
                return False
            r += sr
            c += sc
        target = board[tr][tc]
        return target is None or target.color != self.color

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q' if color == 'white' else 'q')
    
    def can_move(self, board, fr, fc, tr, tc):
        r = Rook(self.color)
        b = Bishop(self.color)
        return r.can_move(board, fr, fc, tr, tc) or b.can_move(board, fr, fc, tr, tc)

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K' if color == 'white' else 'k')
    
    def can_move(self, board, fr, fc, tr, tc):
        if max(abs(tr - fr), abs(tc - fc)) != 1:
            return False
        target = board[tr][tc]
        return target is None or target.color != self.color

class Chess:
    def __init__(self):
        self.b = [[None]*8 for _ in range(8)]
        self.turn = 'white'
        # Пешки
        for i in range(8):
            self.b[1][i] = Pawn('black')
            self.b[6][i] = Pawn('white')
        # Фигуры
        row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, p in enumerate(row):
            self.b[0][i] = p('black')
            self.b[7][i] = p('white')
    
    def show(self):
        print('\n  a b c d e f g h')
        for r in range(8):
            print(8-r, end=' ')
            for c in range(8):
                print(self.b[r][c].symbol if self.b[r][c] else '.', end=' ')
            print(8-r)
        print('  a b c d e f g h')
        print(f'Ход: {self.turn}\n')
    
    def move(self, f, t):
        fc, fr = ord(f[0])-97, 8-int(f[1])
        tc, tr = ord(t[0])-97, 8-int(t[1])
        p = self.b[fr][fc]
        if not p or p.color != self.turn:
            return False
        if not p.can_move(self.b, fr, fc, tr, tc):
            return False
        self.b[tr][tc] = p
        self.b[fr][fc] = None
        self.turn = 'black' if self.turn == 'white' else 'white'
        return True

# Игра
g = Chess()
while True:
    g.show()
    s = input('Ход (e2 e4): ').split()
    if len(s) == 2 and g.move(s[0], s[1]):
        print('OK\n')
    else:
        print('Ошибка\n')
        
        
        
        
        
           
        
#из доп. заданий № 2          
        
class Board:
    def __init__(self):
        self.board = [[None]*8 for _ in range(8)]
        self.player = 1  # 1 - белые, 2 - черные
        
        # Расстановка шашек
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 1:
                    if i < 3: self.board[i][j] = 2  # черные
                    if i > 4: self.board[i][j] = 1  # белые
    
    def show(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.board[i][j] == 1: print("Б", end=" ")
                elif self.board[i][j] == 2: print("Ч", end=" ")
                else: print("·" if (i+j)%2==0 else " ", end=" ")
            print()
    
    def move(self, fr, fc, tr, tc):
        piece = self.board[fr][fc]
        if not piece or piece != self.player:
            return False
        
        dr, dc = tr-fr, tc-fc
        if abs(dr) != abs(dc) or dr == 0:
            return False
        
        # Обычный ход
        if abs(dr) == 1:
            if self.board[tr][tc] is None:
                self.board[tr][tc] = piece
                self.board[fr][fc] = None
                self.player = 3 - self.player
                return True
        
        # Взятие
        if abs(dr) == 2:
            mr, mc = (fr+tr)//2, (fc+tc)//2
            if self.board[mr][mc] and self.board[mr][mc] != piece and self.board[tr][tc] is None:
                self.board[tr][tc] = piece
                self.board[fr][fc] = None
                self.board[mr][mc] = None
                self.player = 3 - self.player
                return True
        
        return False

# Игра
game = Board()
while True:
    game.show()
    print(f"Ход {'белых' if game.player==1 else 'черных'} (строка_от столбец_от строка_куда столбец_куда):")
    try:
        fr, fc, tr, tc = map(int, input().split())
        if not game.move(fr, fc, tr, tc):
            print("Недопустимый ход!")
    except:
        print("Введите 4 числа через пробел")
        
        
        
        
        
        
        
        
        
        
        
#из доп. заданий № 3
        
# Создаем доску
board = {}

# Белые фигуры (1-6 ряд)
for i in range(8):
    board[(i, 1)] = 'P'  # пешки

# Фигуры на первой линии
board[(0, 0)] = 'R'  # ладья
board[(1, 0)] = 'N'  # конь
board[(2, 0)] = 'B'  # слон
board[(3, 0)] = 'Q'  # ферзь
board[(4, 0)] = 'K'  # король
board[(5, 0)] = 'B'  # слон
board[(6, 0)] = 'N'  # конь
board[(7, 0)] = 'R'  # ладья

# Черные фигуры (5-6 ряд)
for i in range(8):
    board[(i, 5)] = 'p'  # пешки

# Фигуры на последней линии
board[(0, 6)] = 'r'  # ладья
board[(1, 6)] = 'n'  # конь
board[(2, 6)] = 'b'  # слон
board[(3, 6)] = 'q'  # ферзь
board[(4, 6)] = 'k'  # король
board[(5, 6)] = 'b'  # слон
board[(6, 6)] = 'n'  # конь
board[(7, 6)] = 'r'  # ладья

def show_board():
    """Показывает доску в текстовом виде"""
    print("\n  a b c d e f g h")
    print("  ---------------")
    
    for y in range(6, -1, -1):
        row = str(y) + "|"
        for x in range(8):
            if (x, y) in board:
                piece = board[(x, y)]
                # Белые фигуры - большие буквы, черные - маленькие
                if piece.isupper():
                    row += f" {piece}"
                else:
                    row += f" {piece}"
            else:
                row += " ·"
        print(row)
    print()

def get_piece_name(piece):
    """Возвращает название фигуры"""
    names = {
        'K': 'Король', 'Q': 'Ферзь', 'R': 'Ладья', 
        'B': 'Слон', 'N': 'Конь', 'P': 'Пешка',
        'k': 'король', 'q': 'ферзь', 'r': 'ладья', 
        'b': 'слон', 'n': 'конь', 'p': 'пешка'
    }
    return names.get(piece, '?')

def get_valid_moves(x, y):
    """Возвращает список возможных ходов для фигуры"""
    piece = board[(x, y)]
    moves = []
    is_white = piece.isupper()
    piece_type = piece.upper()
    
    # Пешка
    if piece_type == 'P':
        # Направление: белые идут вверх (y+1), черные вниз (y-1)
        direction = 1 if is_white else -1
        
        # Ход вперед
        if (x, y + direction) not in board:
            moves.append((x, y + direction))
        
        # Взятие по диагонали
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx <= 7 and 0 <= ny <= 6:
                if (nx, ny) in board:
                    target = board[(nx, ny)]
                    # Можно взять фигуру противника
                    if target.isupper() != is_white:
                        moves.append((nx, ny))
    
    # Ладья
    elif piece_type == 'R':
        # Четыре направления
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, 8):
                nx, ny = x + dx * i, y + dy * i
                if nx < 0 or nx > 7 or ny < 0 or ny > 6:
                    break
                if (nx, ny) in board:
                    target = board[(nx, ny)]
                    if target.isupper() != is_white:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))
    
    # Конь
    elif piece_type == 'N':
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= 7 and 0 <= ny <= 6:
                if (nx, ny) not in board:
                    moves.append((nx, ny))
                else:
                    target = board[(nx, ny)]
                    if target.isupper() != is_white:
                        moves.append((nx, ny))
    
    # Слон
    elif piece_type == 'B':
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                nx, ny = x + dx * i, y + dy * i
                if nx < 0 or nx > 7 or ny < 0 or ny > 6:
                    break
                if (nx, ny) in board:
                    target = board[(nx, ny)]
                    if target.isupper() != is_white:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))
    
    # Ферзь
    elif piece_type == 'Q':
        # Все 8 направлений
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, 8):
                nx, ny = x + dx * i, y + dy * i
                if nx < 0 or nx > 7 or ny < 0 or ny > 6:
                    break
                if (nx, ny) in board:
                    target = board[(nx, ny)]
                    if target.isupper() != is_white:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))
    
    # Король
    elif piece_type == 'K':
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx <= 7 and 0 <= ny <= 6:
                    if (nx, ny) not in board:
                        moves.append((nx, ny))
                    else:
                        target = board[(nx, ny)]
                        if target.isupper() != is_white:
                            moves.append((nx, ny))
    
    return moves

def parse_position(pos):
    """Преобразует букву+цифру в координаты (a1 -> 0,0)"""
    if len(pos) != 2:
        return None
    col = pos[0].lower()
    if col not in 'abcdefgh':
        return None
    try:
        row = int(pos[1])
    except:
        return None
    if row < 0 or row > 6:
        return None
    return (ord(col) - ord('a'), row)

def format_position(x, y):
    """Преобразует координаты в букву+цифру (0,0 -> a0)"""
    return f"{chr(ord('a') + x)}{y}"

def main():
    turn = 'white'  # white или black
    selected = None
    
    print("=" * 50)
    print("Добро пожаловать в Hex Chess!")
    print("=" * 50)
    print("\nУправление:")
    print("- Введите координаты фигуры и куда ходить (например: a2 a3)")
    print("- Или выберите фигуру: введите координаты (например: a2)")
    print("- Чтобы выйти, введите 'quit'")
    print("- Чтобы посмотреть возможные ходы, введите 'moves'")
    print("\nОбозначения фигур:")
    print("Белые: K(король) Q(ферзь) R(ладья) B(слон) N(конь) P(пешка)")
    print("Черные: k(король) q(ферзь) r(ладья) b(слон) n(конь) p(пешка)")
    print()
    
    while True:
        show_board()
        
        # Показываем чей ход
        print(f"Ход: {'БЕЛЫЕ' if turn == 'white' else 'ЧЕРНЫЕ'}")
        
        # Если выбрана фигура, показываем возможные ходы
        if selected:
            x, y = selected
            piece = board[selected]
            print(f"Выбрана: {format_position(x, y)} ({get_piece_name(piece)})")
            moves_list = get_valid_moves(x, y)
            if moves_list:
                moves_str = ", ".join([format_position(mx, my) for mx, my in moves_list])
                print(f"Возможные ходы: {moves_str}")
            else:
                print("Нет возможных ходов для этой фигуры")
        
        # Ввод команды
        cmd = input("\n> ").strip().split()
        
        if not cmd:
            continue
        
        if cmd[0].lower() == 'quit':
            print("Игра завершена!")
            break
        
        if cmd[0].lower() == 'moves':
            if selected:
                x, y = selected
                moves_list = get_valid_moves(x, y)
                if moves_list:
                    print("Возможные ходы:")
                    for mx, my in moves_list:
                        target = board.get((mx, my), 'пусто')
                        print(f"  {format_position(mx, my)} -> {target if target != 'пусто' else 'пустая клетка'}")
                else:
                    print("Нет возможных ходов")
            else:
                print("Сначала выберите фигуру")
            continue
        
        # Обработка выбора фигуры или хода
        if len(cmd) == 1:
            # Выбор фигуры
            pos = parse_position(cmd[0])
            if pos and pos in board:
                piece = board[pos]
                # Проверяем, что фигура принадлежит текущему игроку
                if (turn == 'white' and piece.isupper()) or (turn == 'black' and piece.islower()):
                    selected = pos
                    print(f"Выбрана фигура {get_piece_name(piece)} на {format_position(pos[0], pos[1])}")
                else:
                    print("Это не ваша фигура!")
            else:
                print("Неверные координаты или пустая клетка!")
        
        elif len(cmd) == 2:
            # Ход: from to
            from_pos = parse_position(cmd[0])
            to_pos = parse_position(cmd[1])
            
            if not from_pos or not to_pos:
                print("Неверные координаты!")
                continue
            
            if from_pos not in board:
                print("На выбранной клетке нет фигуры!")
                continue
            
            piece = board[from_pos]
            
            # Проверяем, что фигура принадлежит текущему игроку
            if (turn == 'white' and not piece.isupper()) or (turn == 'black' and not piece.islower()):
                print("Это не ваша фигура!")
                continue
            
            # Проверяем, можно ли так ходить
            if to_pos in get_valid_moves(from_pos[0], from_pos[1]):
                # Делаем ход
                board[to_pos] = board[from_pos]
                del board[from_pos]
                print(f"Ход выполнен: {format_position(from_pos[0], from_pos[1])} -> {format_position(to_pos[0], to_pos[1])}")
                
                # Меняем игрока
                turn = 'black' if turn == 'white' else 'white'
                selected = None
            else:
                print("Так ходить нельзя!")
        
        else:
            print("Неверная команда!")
            print("Примеры:")
            print("  a2          - выбрать фигуру")
            print("  a2 a3       - сделать ход")
            print("  moves       - показать возможные ходы выбранной фигуры")
            print("  quit        - выйти из игры")

if __name__ == "__main__":
    main()
