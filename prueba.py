import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Configuración del juego
WIDTH, HEIGHT = 800, 600
PAD_WIDTH, PAD_HEIGHT = 20, 100
BALL_SIZE = 20
BALL_SPEED = 5

# Variables globales para el estado del juego
left_pad_pos = HEIGHT // 2 - PAD_HEIGHT // 2
right_pad_pos = HEIGHT // 2 - PAD_HEIGHT // 2
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [BALL_SPEED, BALL_SPEED]

def start_game():
    # Ocultar el menú principal
    title_label.pack_forget()
    button_frame.pack_forget()
    background_label.pack_forget()

    # Mostrar el lienzo del juego
    game_frame.pack()

    # Iniciar el juego
    run_game()

def show_options():
    messagebox.showinfo("Opciones", "Mostrar opciones del juego...")

def exit_game():
    window.quit()

def run_game():
    update_game()
    window.after(50, run_game)

def update_game(): ## Aqui debemos corregir el juego, y agregar el pygame 
    global left_pad_pos, right_pad_pos, ball_pos, ball_vel

    # Mover la pelota
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Colisiones con la parte superior e inferior
    if ball_pos[1] <= BALL_SIZE // 2 or ball_pos[1] >= HEIGHT - BALL_SIZE // 2:
        ball_vel[1] = -ball_vel[1]

    # Colisiones con las paletas
    if (ball_pos[0] <= PAD_WIDTH + BALL_SIZE // 2 and left_pad_pos <= ball_pos[1] <= left_pad_pos + PAD_HEIGHT) or \
       (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_SIZE // 2 and right_pad_pos <= ball_pos[1] <= right_pad_pos + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]

    # Colisiones con los bordes izquierdo y derecho
    if ball_pos[0] <= BALL_SIZE // 2 or ball_pos[0] >= WIDTH - BALL_SIZE // 2:
        ball_pos = [WIDTH // 2, HEIGHT // 2]

    # Dibujar los elementos del juego
    canvas.delete("all")
    canvas.create_rectangle(0, left_pad_pos, PAD_WIDTH, left_pad_pos + PAD_HEIGHT, fill="white")
    canvas.create_rectangle(WIDTH - PAD_WIDTH, right_pad_pos, WIDTH, right_pad_pos + PAD_HEIGHT, fill="white")
    canvas.create_oval(ball_pos[0] - BALL_SIZE // 2, ball_pos[1] - BALL_SIZE // 2,
                       ball_pos[0] + BALL_SIZE // 2, ball_pos[1] + BALL_SIZE // 2, fill="white")

# Crear la ventana principal
window = tk.Tk()
window.title("Pong")
window.geometry("800x600")

# Cargar la imagen de fondo
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Crear un widget de etiqueta para la imagen de fondo
background_label = tk.Label(window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Crear el título del juego
title_label = tk.Label(window, text="Pong", font=("Arial", 44), fg="white", bg="black")
title_label.pack(pady=40)

# Crear los botones del menú
button_frame = tk.Frame(window, bg="black")
button_frame.pack(pady=20)

new_game_button = tk.Button(button_frame, text="Nuevo Juego", font=("Arial", 24), width=15, command=start_game)
new_game_button.pack(pady=10)

options_button = tk.Button(button_frame, text="Opciones", font=("Arial", 24), width=15, command=show_options)
options_button.pack(pady=10)

exit_button = tk.Button(button_frame, text="Salir", font=("Arial", 24), width=15, command=exit_game)
exit_button.pack(pady=10)

# Crear el marco del juego y el lienzo
game_frame = tk.Frame(window, bg="black")
canvas = tk.Canvas(game_frame, bg="black", width=WIDTH, height=HEIGHT)
canvas.pack()

# Ejecutar la ventana principal
window.mainloop()