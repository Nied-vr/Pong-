import tkinter as tk
from tkinter import messagebox

def start_game():
    # Ocultar el menú principal
    title_label.pack_forget()
    button_frame.pack_forget()
    
    # Mostrar el lienzo del juego
    game_frame.pack()

    # Aquí puedes iniciar la lógica del juego
    run_game()

def show_options():
    messagebox.showinfo("Opciones", "Mostrar opciones del juego...")

def exit_game():
    window.quit()

def run_game():
    # Aquí puedes agregar la lógica del juego Pong
    pass

# Crear la ventana principal
window = tk.Tk()
window.title("Pong")
window.geometry("800x600")
window.configure(bg="black")

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
canvas = tk.Canvas(game_frame, bg="black", width=800, height=500)
canvas.pack()

# Ejecutar la ventana principal
window.mainloop()