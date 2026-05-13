import math
import itertools
import functools
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

def visualize(poly_iters, ax, title="Polygons"):
    if not isinstance(poly_iters, list):
        poly_iters = [poly_iters]
        
    colors = ['#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4']
    all_x, all_y = [], []
    
    for idx, it in enumerate(poly_iters):
        polys = list(it) 
        if not polys: 
            continue
        
        patches = [MplPolygon(poly, closed=True) for poly in polys]
        col = PatchCollection(patches, facecolor=colors[idx % len(colors)], edgecolor='black', alpha=0.6)
        ax.add_collection(col)
        
        for p in polys:
            for x, y in p:
                all_x.append(x)
                all_y.append(y)
                
    if all_x and all_y:
        ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
        ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=10)

def tr_translate(dx, dy):
    return lambda poly: tuple((x + dx, y + dy) for x, y in poly)

def tr_rotate(angle_rad, cx=0, cy=0):
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    return lambda poly: tuple(
        (cx + (x-cx)*cos_a - (y-cy)*sin_a, cy + (x-cx)*sin_a + (y-cy)*cos_a)
        for x, y in poly
    )

def tr_symmetry(axis='point', cx=0, cy=0):
    if axis == 'x':   
        return lambda poly: tuple((x, 2*cy - y) for x, y in poly)
    elif axis == 'y': 
        return lambda poly: tuple((2*cx - x, y) for x, y in poly)
    else:             
        return lambda poly: tuple((2*cx - x, 2*cy - y) for x, y in poly) # Точечная

def tr_homothety(cx, cy, k):
    return lambda poly: tuple((cx + k*(x-cx), cy + k*(y-cy)) for x, y in poly)

def gen_rectangle(w, h, dx, dy):
    base = ((0, 0), (0, h), (w, h), (w, 0))
    return map(lambda i: tr_translate(i*dx, i*dy)(base), itertools.count())

def gen_triangle(side, dx, dy):
    h = side * math.sqrt(3) / 2
    base = ((0, 0), (side, 0), (side/2, h))
    return map(lambda i: tr_translate(i*dx, i*dy)(base), itertools.count())

def gen_hexagon(side, dx, dy):
    base = tuple((side * math.cos(math.radians(a)), side * math.sin(math.radians(a))) for a in range(0, 360, 60))
    return map(lambda i: tr_translate(i*dx, i*dy)(base), itertools.count())

def polygon_area(poly):
    n = len(poly)
    return 0.5 * abs(sum(map(lambda i: poly[i][0]*poly[(i+1)%n][1] - poly[(i+1)%n][0]*poly[i][1], range(n))))

def side_lengths(poly):
    n = len(poly)
    return map(lambda i: math.dist(poly[i], poly[(i+1)%n]), range(n))

def is_convex(poly):
    if len(poly) < 3: return False
    n = len(poly)
    crosses = list(map(lambda i: (poly[(i+1)%n][0]-poly[i][0])*(poly[(i+2)%n][1]-poly[(i+1)%n][1]) - 
                                 (poly[(i+1)%n][1]-poly[i][1])*(poly[(i+2)%n][0]-poly[(i+1)%n][0]), range(n)))
    return all(c >= 0 for c in crosses) or all(c <= 0 for c in crosses)

def point_in_convex_poly(px, py, poly):
    n = len(poly)
    crosses = list(map(lambda i: (poly[(i+1)%n][0]-poly[i][0])*(py-poly[i][1]) - 
                                 (poly[(i+1)%n][1]-poly[i][1])*(px-poly[i][0]), range(n)))
    return all(c >= 0 for c in crosses) or all(c <= 0 for c in crosses)

# Доп. задание 1
def flt_convex_polygon():
    return is_convex

def flt_angle_point(px, py):
    return lambda poly: any(math.isclose(x, px) and math.isclose(y, py) for x, y in poly)

def flt_square(max_area):
    return lambda poly: polygon_area(poly) < max_area

def flt_short_side(max_len):
    return lambda poly: min(side_lengths(poly)) < max_len

def flt_point_inside(px, py):
    return lambda poly: is_convex(poly) and point_in_convex_poly(px, py, poly)

def flt_polygon_angles_inside(target_poly):
    return lambda poly: is_convex(poly) and any(map(lambda pt: point_in_convex_poly(pt[0], pt[1], poly), target_poly))

# Доп. задание 3
def make_filter_decorator(hof):
    def decorator_factory(*args, **kwargs):
        fn = hof(*args, **kwargs) if callable(hof) and args or kwargs or hof.__code__.co_argcount > 0 else hof()
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*f_args, **f_kwargs):
                new_args = [filter(fn, arg) if hasattr(arg, '__iter__') and not isinstance(arg, tuple) else arg for arg in f_args]
                return func(*new_args, **f_kwargs)
            return wrapper
        return decorator_factory
    return decorator_factory

def make_map_decorator(hof):
    def decorator_factory(*args, **kwargs):
        fn = hof(*args, **kwargs)
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*f_args, **f_kwargs):
                new_args = [map(fn, arg) if hasattr(arg, '__iter__') and not isinstance(arg, tuple) else arg for arg in f_args]
                return func(*new_args, **f_kwargs)
            return wrapper
        return decorator_factory
    return decorator_factory

dec_flt_convex_polygon = make_filter_decorator(flt_convex_polygon)
dec_flt_angle_point = make_filter_decorator(flt_angle_point)
dec_flt_square = make_filter_decorator(flt_square)
dec_flt_short_side = make_filter_decorator(flt_short_side)
dec_flt_point_inside = make_filter_decorator(flt_point_inside)
dec_flt_polygon_angles_inside = make_filter_decorator(flt_polygon_angles_inside)

dec_tr_translate = make_map_decorator(tr_translate)
dec_tr_rotate = make_map_decorator(tr_rotate)
dec_tr_symmetry = make_map_decorator(tr_symmetry)
dec_tr_homothety = make_map_decorator(tr_homothety)


def agr_origin_nearest(poly_seq):
    dist = lambda p: min(math.dist((0,0), pt) for pt in p)
    return functools.reduce(lambda p1, p2: p1 if dist(p1) < dist(p2) else p2, poly_seq)

def agr_max_side(poly_seq):
    return functools.reduce(lambda acc, p: max(acc, max(side_lengths(p))), poly_seq, 0)

def agr_min_area(poly_seq):
    return functools.reduce(lambda acc, p: min(acc, polygon_area(p)), poly_seq, float('inf'))

def agr_perimeter(poly_seq):
    return functools.reduce(lambda acc, p: acc + sum(side_lengths(p)), poly_seq, 0)

def agr_area(poly_seq):
    return functools.reduce(lambda acc, p: acc + polygon_area(p), poly_seq, 0)


def dec_tr_translate(dx, dy):
    """Декоратор, применяющий трансляцию к каждому полигону из итератора"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            iterator = func(*args, **kwargs)
            return (tr_translate(dx, dy)(polygon) for polygon in iterator)
        return wrapper
    return decorator

def dec_flt_square(max_area):
    """Декоратор, фильтрующий полигоны по площади"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            iterator = func(*args, **kwargs)
            return (polygon for polygon in iterator if polygon_square(polygon) < max_area)
        return wrapper
    return decorator

def main():
    fig1, axes1 = plt.subplots(1, 3, figsize=(15, 5))
    fig1.suptitle("Задание 2: Генераторы бесконечных последовательностей")
    visualize(itertools.islice(gen_rectangle(2, 1, 3, 0), 7), axes1[0], "Прямоугольники")
    visualize(itertools.islice(gen_triangle(2, 3, 0), 7), axes1[1], "Треугольники")
    visualize(itertools.islice(gen_hexagon(1.5, 3, 0), 7), axes1[2], "Шестиугольники")

    fig2, axes2 = plt.subplots(2, 2, figsize=(12, 10))
    fig2.suptitle("Задание 4: Визуализация трансформаций")

    r1 = map(tr_rotate(math.radians(30)), itertools.islice(gen_rectangle(2,1, 2.5,0), 7))
    r2 = map(tr_translate(0, 2), map(tr_rotate(math.radians(30)), itertools.islice(gen_rectangle(2,1, 2.5,0), 7)))
    r3 = map(tr_translate(0, 4), map(tr_rotate(math.radians(30)), itertools.islice(gen_rectangle(2,1, 2.5,0), 7)))
    visualize([r1, r2, r3], axes2[0, 0], "Три параллельные ленты (угол 30°)")

    i1 = map(tr_translate(5, 5), map(tr_rotate(math.radians(45)), itertools.islice(gen_rectangle(2,1, 2.5,0), 10)))
    i2 = map(tr_translate(5, 5), map(tr_rotate(math.radians(-45)), itertools.islice(gen_rectangle(2,1, 2.5,0), 10)))
    visualize([i1, i2], axes2[0, 1], "Две пересекающиеся ленты (в точке 5,5)")

    t_base = list(itertools.islice(gen_triangle(2, 2.5, 0), 7))
    t1 = iter(t_base)
    t2 = map(tr_translate(0, -0.5), map(tr_symmetry('x', cy=0), t_base))
    visualize([t1, t2], axes2[1, 0], "Ленты симметричных треугольников")

    base_q = ((1, 0.5), (2, 0.5), (2, 1), (1, 1))
    quads = map(lambda i: tr_homothety(0, 0, 1.3**i)(base_q), range(10))
    visualize(quads, axes2[1, 1], "Гомотетия: масштабируемые четырехугольники")

    fig3, axes3 = plt.subplots(1, 3, figsize=(15, 5))
    fig3.suptitle("Задание 6: Применение фильтров (Доп. задание 2)")

    q_all = map(lambda i: tr_homothety(0, 0, 1.3**i)(base_q), range(15))
    q_filtered = filter(flt_square(10), q_all) 
    visualize(q_filtered, axes3[0], "Ровно 6 масштабируемых фигур (flt_square)")

    t_all = map(lambda i: tr_homothety(0, 0, 1.2**i)(((0,0), (1,0), (0.5, 0.866))), range(15))
    t_filtered = filter(flt_short_side(1.8), t_all) # Пройдут первые 4 фигуры
    visualize(t_filtered, axes3[1], "<=4 фигуры с кратчайшей стороной < 1.8")

    i1 = map(tr_translate(5, 5), map(tr_rotate(math.radians(45)), itertools.islice(gen_rectangle(2,1, 2.5,0), 10)))
    visualize(i1, axes3[2], "Пересекающиеся с точкой (2,2)")

    @dec_flt_square(2.0)            
    @dec_tr_translate(0, 2)         
    def process_data(iterator):
        return iterator

    plt.tight_layout()
    plt.show()

    print("ДЕМОНСТРАЦИЯ АГРЕГИРУЮЩИХ ФУНКЦИЙ (reduce)")
    test_seq = list(map(lambda i: tr_homothety(0, 0, 1.2**i)(((1,1), (2,1), (2,2), (1,2))), range(5)))
    print(f"Nearest to origin (Area): {polygon_area(agr_origin_nearest(test_seq)):.2f}")
    print(f"Max side length:          {agr_max_side(test_seq):.2f}")
    print(f"Min area:                 {agr_min_area(test_seq):.2f}")
    print(f"Total perimeter:          {agr_perimeter(test_seq):.2f}")
    print(f"Total area:               {agr_area(test_seq):.2f}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
