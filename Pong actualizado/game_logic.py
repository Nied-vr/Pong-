from firebase_admin import db
from tkinter import messagebox
from profile_manager import current_profile

def update_high_score(new_high_score):
    if current_profile:
        ref = db.reference(f'profiles/{current_profile}/high_score')
        current_high_score = ref.get()
        if new_high_score > current_high_score:
            ref.set(new_high_score)

def view_high_score():
    if current_profile:
        ref = db.reference(f'profiles/{current_profile}/high_score')
        high_score = ref.get()
        messagebox.showinfo("Mayor Récord", f"El mayor récord es: {high_score}")

def delete_high_score():
    if current_profile:
        ref = db.reference(f'profiles/{current_profile}/high_score')
        ref.set(0)
        messagebox.showinfo("Mayor Récord", "El récord ha sido eliminado.")