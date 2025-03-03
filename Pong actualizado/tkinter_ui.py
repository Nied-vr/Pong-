import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from firebase_admin import credentials, db
import firebase_admin
from pygame_game import run_pong_classic, run_pong_speed, run_pong_inverted_controls
from game_logic import update_high_score, view_high_score, delete_high_score
from profile_manager import current_profile

cred = credentials.Certificate("credencial.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pong-3e97f-default-rtdb.firebaseio.com/'
})

def start_game_classic():
    if not current_profile:
        messagebox.showwarning("Advertencia", "Seleccione un perfil")
        login_frame.place(x=200, y=100)  # Ensure the profile selection screen is shown again
        return
    title_label.place_forget()
    button_frame.place_forget()
    background_label.lift()  # Ensure the background image is always on top
    game_frame.place(x=0, y=0, width=800, height=600)
    run_pong_classic()
    restore_main_screen()

def save_config(config_type, config_data):
    if current_profile:
        ref = db.reference(f'profiles/{current_profile}/config/{config_type}')
        ref.set(config_data)

def configure_general():
    win_points = simpledialog.askinteger("Configuración General", "Ingrese los puntos para ganar:", minvalue=1)
    ball_size = simpledialog.askinteger("Configuración General", "Ingrese el tamaño de la pelota:", minvalue=1)
    if win_points and ball_size:
        save_config('general', {'win_points': win_points, 'ball_size': ball_size})

def configure_classic():
    ball_speed = simpledialog.askinteger("Configuración Pong Clásico", "Ingrese la velocidad de la pelota:", minvalue=1)
    if ball_speed:
        save_config('classic', {'ball_speed': ball_speed})

def configure_speed():
    initial_ball_speed = simpledialog.askinteger("Configuración Pong Velocidad", "Ingrese la velocidad inicial de la pelota:", minvalue=1)
    if initial_ball_speed:
        save_config('speed', {'initial_ball_speed': initial_ball_speed})

def configure_inverted_controls():
    ball_speed = simpledialog.askinteger("Configuración Controles Invertidos", "Ingrese la velocidad de la pelota:", minvalue=1)
    invert_time = simpledialog.askinteger("Configuración Controles Invertidos", "Ingrese el tiempo para cambiar los controles (ms):", minvalue=1000)
    if ball_speed and invert_time:
        save_config('inverted_controls', {'ball_speed': ball_speed, 'invert_time': invert_time})

def start_game_speed():
    if not current_profile:
        messagebox.showwarning("Advertencia", "Seleccione un perfil")
        login_frame.place(x=200, y=100)  # Ensure the profile selection screen is shown again
        return
    title_label.place_forget()
    button_frame.place_forget()
    background_label.lift()  # Ensure the background image is always on top
    game_frame.place(x=0, y=0, width=800, height=600)
    run_pong_speed()
    restore_main_screen()


def start_game_inverted_controls():
    if not current_profile:
        messagebox.showwarning("Advertencia", "Seleccione un perfil")
        login_frame.place(x=200, y=100)  # Ensure the profile selection screen is shown again
        return
    title_label.place_forget()
    button_frame.place_forget()
    background_label.lift()  # Ensure the background image is always on top
    game_frame.place(x=0, y=0, width=800, height=600)
    run_pong_inverted_controls()
    restore_main_screen()

def show_game_modes():
    title_label.place_forget()
    button_frame.place_forget()
    game_modes_frame.place(x=300, y=200)
    back_button.place(x=10, y=10)
    game_modes_frame.lift()
    back_button.lift()

def show_options():
    title_label.place_forget()
    button_frame.place_forget()
    options_frame.place(x=300, y=200)
    back_button.place(x=10, y=10)
    options_frame.lift()
    back_button.lift()

def exit_game():
    window.quit()

def restore_main_screen():
    title_label.place(x=300, y=40)
    button_frame.place(x=300, y=200)
    background_label.lift()
    title_label.lift()
    button_frame.lift()

def back_to_main_screen():
    game_frame.place_forget()
    options_frame.place_forget()
    game_modes_frame.place_forget()
    back_button.place_forget()
    restore_main_screen()

def start_tkinter_ui():
    global window, title_label, button_frame, background_label, game_frame, options_frame, login_frame, profile_listbox, back_button, game_modes_frame

    window = tk.Tk()
    window.title("Pong")
    window.geometry("800x600")

    background_image = Image.open("background.JPEG")
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(window, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_frame = tk.Frame(window, bg="black")
    login_frame.place(x=200, y=100)

    profile_label = tk.Label(login_frame, text="Seleccionar Perfil", font=("Arial", 20), fg="white", bg="black")
    profile_label.pack(pady=10)

    profile_listbox = tk.Listbox(login_frame, font=("Arial", 16), width=30, height=10)
    profile_listbox.pack(pady=10)
    load_profiles()

    select_button = tk.Button(login_frame, text="Seleccionar", font=("Arial", 16), command=select_profile)
    select_button.pack(pady=5)

    new_profile_button = tk.Button(login_frame, text="Nuevo Perfil", font=("Arial", 16), command=create_profile)
    new_profile_button.pack(pady=5)

    delete_profile_button = tk.Button(login_frame, text="Eliminar Perfil", font=("Arial", 16), command=delete_profile)
    delete_profile_button.pack(pady=5)

    title_label = tk.Label(window, text="Pong", font=("Arial", 44), fg="white", bg="black")
    button_frame = tk.Frame(window, bg="black")
    new_game_button = tk.Button(button_frame, text="Nuevo Juego", font=("Arial", 20), width=12, height=2, command=show_game_modes)
    options_button = tk.Button(button_frame, text="Opciones", font=("Arial", 20), width=12, height=2, command=show_options)
    exit_button = tk.Button(button_frame, text="Salir", font=("Arial", 20), width=12, height=2, command=exit_game)

    new_game_button.pack(pady=5)
    options_button.pack(pady=5)
    exit_button.pack(pady=5)

    game_frame = tk.Frame(window, bg="black")
    canvas = tk.Canvas(game_frame, bg="black", width=800, height=600)
    canvas.pack()

    options_frame = tk.Frame(window, bg="black")
    general_config_button = tk.Button(options_frame, text="Configuración general", font=("Arial", 20), width=25, height=2, command=configure_general)
    classic_config_button = tk.Button(options_frame, text="Configuración Pong clásico", font=("Arial", 20), width=25, height=2, command=configure_classic)
    speed_config_button = tk.Button(options_frame, text="Configuración Pong velocidad", font=("Arial", 20), width=25, height=2, command=configure_speed)
    inverted_controls_config_button = tk.Button(options_frame, text="Configuración Controles invertidos", font=("Arial", 20), width=25, height=2, command=configure_inverted_controls)

    general_config_button.pack(pady=5)
    classic_config_button.pack(pady=5)
    speed_config_button.pack(pady=5)
    inverted_controls_config_button.pack(pady=5)

    game_modes_frame = tk.Frame(window, bg="black")
    classic_game_button = tk.Button(game_modes_frame, text="Pong Clásico", font=("Arial", 20), width=20, height=2, command=start_game_classic)
    speed_game_button = tk.Button(game_modes_frame, text="Pong Velocidad", font=("Arial", 20), width=20, height=2, command=start_game_speed)
    inverted_controls_game_button = tk.Button(game_modes_frame, text="Pong Controles Invertidos", font=("Arial", 20), width=20, height=2, command=start_game_inverted_controls)

    classic_game_button.pack(pady=5)
    speed_game_button.pack(pady=5)
    inverted_controls_game_button.pack(pady=5)

    back_button = tk.Button(window, text="←", font=("Arial", 20), command=back_to_main_screen)

    login_frame.lift()  # Ensure the login frame is on top initially

    window.mainloop()

def load_profiles():
    ref = db.reference('profiles')
    profiles = ref.get()
    profile_listbox.delete(0, tk.END)
    if profiles:
        for profile in profiles.keys():
            profile_listbox.insert(tk.END, profile)

def select_profile():
    global current_profile
    selected_profile = profile_listbox.get(tk.ACTIVE)
    if selected_profile:
        current_profile = selected_profile
        login_frame.place_forget()
        restore_main_screen()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un perfil")

def create_profile():
    new_profile_name = simpledialog.askstring("Nuevo Perfil", "Ingrese el nombre del nuevo perfil:")
    if new_profile_name:
        ref = db.reference('profiles')
        ref.child(new_profile_name).set({'high_score': 0})
        load_profiles()

def delete_profile():
    selected_profile = profile_listbox.get(tk.ACTIVE)
    if selected_profile:
        ref = db.reference('profiles')
        ref.child(selected_profile).delete()
        load_profiles()

def show_config(config_type):
    messagebox.showinfo("Configuración", f"Mostrando configuración para: {config_type}")