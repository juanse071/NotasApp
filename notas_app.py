import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import json

# -----------------------
# Base de Datos
# -----------------------
def init_db():
    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_nota(contenido):
    if not contenido.strip():
        messagebox.showwarning("Advertencia", "La nota no puede estar vacía.")
        return

    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notas (contenido) VALUES (?)', (contenido,))
    conn.commit()
    conn.close()
    print("✅ Nota guardada en SQLite.")
    simular_envio_servidor(contenido)

def obtener_notas():
    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notas')
    filas = cursor.fetchall()
    conn.close()
    return filas

def eliminar_nota(id_nota):
    conn = sqlite3.connect('notas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notas WHERE id = ?', (id_nota,))
    conn.commit()
    conn.close()
    print("🗑 Nota eliminada de SQLite.")

# -----------------------
# Simulación REST
# -----------------------
def simular_envio_servidor(nota):
    json_data = json.dumps({'contenido': nota})
    print("📤 Enviando al servidor:", json_data)

# -----------------------
# Interfaz Gráfica
# -----------------------
def actualizar_lista():
    lista_notas.config(state='normal')
    lista_notas.delete(1.0, tk.END)
    notas = obtener_notas()
    for nota in notas:
        lista_notas.insert(tk.END, f"[{nota[0]}] 📝 {nota[1]}\n\n")
    lista_notas.config(state='disabled')

def on_eliminar_click():
    contenido = lista_notas.get("1.0", tk.END)
    seleccion = lista_notas.tag_ranges(tk.SEL)
    if not seleccion:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una nota para eliminar.")
        return
    
    texto_seleccionado = lista_notas.get(seleccion[0], seleccion[1])
    try:
        id_nota = int(texto_seleccionado.split(']')[0].replace('[', ''))
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta nota?"):
            eliminar_nota(id_nota)
            actualizar_lista()
    except:
        messagebox.showerror("Error", "No se pudo eliminar la nota. Asegúrate de seleccionar una nota válida.")

def on_guardar_click():
    contenido = entrada_texto.get("1.0", tk.END)
    guardar_nota(contenido)
    entrada_texto.delete("1.0", tk.END)
    actualizar_lista()

# -----------------------
# Main App
# -----------------------
init_db()

ventana = tk.Tk()
ventana.title("🗒 Mis Notas")
ventana.geometry("600x500")
ventana.resizable(False, False)

# Tema ttk
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 12))
style.configure("TFrame", background="#f0f0f0")

# Frame principal
main_frame = ttk.Frame(ventana, padding="20")
main_frame.pack(expand=True, fill="both")

# Título
titulo = ttk.Label(main_frame, text="Gestor de Notas", font=("Segoe UI", 16, "bold"))
titulo.pack(pady=10)

# Área de entrada
ttk.Label(main_frame, text="Escribe tu nota:").pack(anchor='w', pady=5)
entrada_texto = scrolledtext.ScrolledText(main_frame, width=70, height=5, font=("Segoe UI", 10))
entrada_texto.pack(pady=5)

# Frame para botones
botones_frame = ttk.Frame(main_frame)
botones_frame.pack(fill='x', pady=5)

# Botón guardar
btn_guardar = ttk.Button(botones_frame, text="💾 Guardar Nota", command=on_guardar_click)
btn_guardar.pack(side='left', padx=5)

# Botón eliminar
btn_eliminar = ttk.Button(botones_frame, text="🗑 Eliminar Nota", command=on_eliminar_click)
btn_eliminar.pack(side='left', padx=5)

# Lista de notas
ttk.Label(main_frame, text="Notas guardadas:").pack(anchor='w', pady=(10, 5))
lista_notas = scrolledtext.ScrolledText(main_frame, width=70, height=12, font=("Segoe UI", 10))
lista_notas.pack()

# Cargar contenido inicial
actualizar_lista()

ventana.mainloop()
