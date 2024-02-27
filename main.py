import pygame
import sys
import math
import tkinter as tk

def wait():
    # Дополнительный цикл ожидания события закрытия окна
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.Clock().tick(30)

def calculating_current_altitude(v: float|int, t:float|int, g: float|int) -> float:
    return round(v * t - (g * t**2) / 2, 2)

def calculating_current_length(v: float|int, t:float|int) -> float:
    return round(v * t, 2)

def run_ball(v: float|int, a: int, g: float|int, k: int):
    # Инициализация Pygame
    pygame.init()

    # Определение цветов
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Размеры окна
    WIDTH, HEIGHT = 1000, 1000

    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(" ")
    
    # Начальные координаты мячика
    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2
    
    gravity = g * k
    speed = v * k
    
    # Счетчик времени
    time = 0
    
    # Скорость по каждой оси
    v_x = speed * round(math.cos(math.radians(a)), 5)
    v_y = speed * round(math.sin(math.radians(a)), 5)
    
    # Максимальная высота полета.
    y_max = 0
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Вычисление новых координат мячика.
        ball_x = WIDTH / 2 + calculating_current_length(v_x, time)
        ball_y = HEIGHT + calculating_current_altitude(v_y, time, gravity)
        
        time += 0.01

        # Очистка экрана
        screen.fill(WHITE)

        # Рисование координатных осей
        pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)
        pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

        # Рисование мячика
        pygame.draw.circle(screen, RED, (int(ball_x), int(HEIGHT - (ball_y - HEIGHT / 2))), 20)
        
        # Для рисования на поле
        font = pygame.font.Font(None, 36)
        
        # Отображение скорости мячика:
        v_y_font = font.render(f'Vy: {round(math.sqrt((v_y / k - g * time)**2), 2)}', True, BLACK)
        screen.blit(v_y_font, (10, 10))
        
        # Отображение максимальной высоты мячика:
        h_m_font = font.render(f'Hm: {y_max}', True, BLACK)
        screen.blit(h_m_font, (10, 35))

        # Метки на осях
        text_x = font.render(f'X: {round((ball_x - WIDTH / 2) / k, 4)}', True, BLACK)
        text_y = font.render(f'Y: {round((ball_y - HEIGHT) / k, 4)}', True, BLACK)
        screen.blit(text_x, (WIDTH - 110, HEIGHT // 2 + 10))
        screen.blit(text_y, (WIDTH // 2 + 10, 10))
        
        if round((ball_y - HEIGHT) / k, 4) > y_max:
            y_max = round((ball_y - HEIGHT) / k, 4)

        # print(f"x: {round((ball_x - WIDTH / 2) / k, 4)} | y: {round((ball_y - HEIGHT) / k, 4)}")
        # print(v_x / round(math.cos(math.radians(a)), 5), v_y / round(math.cos(math.radians(a)), 5)) # Док-во, что общая скорость тела не изменяется.
        print(((v_y - g * time)**2) ** 0.5)

        # Обновление экрана
        pygame.display.flip()

        # Задержка для контроля скорости анимации
        pygame.time.Clock().tick(100)

        # Если мяч упал на землю
        if (ball_y - HEIGHT) / k < 0:
            break
        
    print(f"y_max: {y_max}")
    
    try:   
        wait()
    except:
        return 
    
def main():
    k = 1
    
    def slider_update_value(value):
        nonlocal k
        k = float(value)
        
    def run():
        nonlocal k
        
        v = float(speed_entry.get())
        a = float(angle_entry.get())
        g = float(gravity_entry.get())
        
        run_ball(v, a, g, k)
    
    root = tk.Tk()
    
    root.title(" ")
    root.resizable(False, False)
    
    speed_label = tk.Label(root, text="speed: ")
    speed_entry = tk.Entry(root)
    speed_label.pack()
    speed_entry.pack()
    
    angle_label = tk.Label(root, text="angle: ")
    angle_entry = tk.Entry(root)
    angle_label.pack()
    angle_entry.pack()
    
    gravity_label = tk.Label(root, text="gravity: ")
    gravity_entry = tk.Entry(root)
    gravity_label.pack()
    gravity_entry.pack()
    
    coefficient_label = tk.Label(root, text="coefficient: ")
    coefficient_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, command=slider_update_value)
    coefficient_label.pack()
    coefficient_slider.pack()
    
    run_btn = tk.Button(root, text="run", command=run)
    run_btn.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()