import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import os
import webbrowser  # Asegúrate de tener este import
from tkinter.filedialog import asksaveasfilename

def mostrar_contenido_pKa():
    user_dir = os.path.expanduser("~")
    archivo_pKa = os.path.join(user_dir, "pI_predictor", "data", "pKa_customizados.txt")

    output_text.delete("1.0", tk.END)

    if os.path.exists(archivo_pKa):
        with open(archivo_pKa, "r") as f:
            contenido = f.read()
        output_text.insert(tk.END, contenido)
    else:
        output_text.insert(tk.END, "El archivo de pKa personalizados no existe.\n")

def guardar_pKa_customizados():
    texto = output_text.get("1.0", tk.END).strip()

    if texto:
        # Usar el directorio del usuario (Documents/pI_predictor/data)
        user_dir = os.path.expanduser("~")
        save_dir = os.path.join(user_dir, "pI_predictor", "data")
        os.makedirs(save_dir, exist_ok=True)
        archivo_pKa = os.path.join(save_dir, "pKa_customizados.txt")

        try:
            with open(archivo_pKa, 'w') as archivo:  # <-- cambia 'a' por 'w'
                archivo.write(texto + '\n')
            output_text.insert(tk.END, f"\nValores de pKa guardados exitosamente en:\n{archivo_pKa}\n")
        except Exception as e:
            output_text.insert(tk.END, f"Error al guardar los valores: {e}\n")

def guardar_salida_en_archivo():
    contenido = output_text.get("1.0", tk.END).strip()
    if not contenido:
        messagebox.showinfo("Guardar archivo", "No hay contenido para guardar.")
        return

    archivo = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
        title="Guardar como"
    )

    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")




def cargar_pKa_customizados():
    pKa_values_customized = {}
    user_dir = os.path.expanduser("~")
    archivo_pKa = os.path.join(user_dir, "pI_predictor", "data", "pKa_customizados.txt")

    try:
        with open(archivo_pKa, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(" ", 1)
                    amino_acid = parts[0]
                    pKa_values = {}

                    pKa_parts = parts[1].split(";")
                    for part in pKa_parts:
                        part = part.strip()
                        if "=" in part:
                            try:
                                key, value = part.split("=")
                                value = float(value.strip())
                                if 'pK1' in key:
                                    pKa_values['pK1'] = value
                                elif 'pK2' in key:
                                    pKa_values['pK2'] = value
                                elif 'pKR' in key:
                                    pKa_values['pKR'] = value
                            except ValueError:
                                continue
                    if amino_acid and pKa_values:
                        pKa_values_customized[amino_acid] = pKa_values

        return pKa_values_customized

    except FileNotFoundError:
        print(f"No se encontró el archivo de pKa personalizados en {archivo_pKa}")
        return {}

    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo: {e}")
        return {}


pKa_values_lehninger_book = {
    'G': {'pK1': 2.34, 'pK2': 9.6, 'pKR': None},
    'A': {'pK1': 2.34, 'pK2': 9.69, 'pKR': None},
    'V': {'pK1': 2.32, 'pK2': 9.62, 'pKR': None},
    'L': {'pK1': 2.36, 'pK2': 9.6, 'pKR': None},
    'I': {'pK1': 2.36, 'pK2': 9.68, 'pKR': None},
    'M': {'pK1': 2.28, 'pK2': 9.21, 'pKR': None},
    'P': {'pK1': 1.99, 'pK2': 10.96, 'pKR': None},
    'F': {'pK1': 1.83, 'pK2': 9.13, 'pKR': None},
    'Y': {'pK1': 2.2, 'pK2': 9.11, 'pKR': 10.07},
    'W': {'pK1': 2.38, 'pK2': 9.39, 'pKR': None},
    'S': {'pK1': 2.21, 'pK2': 9.15, 'pKR': None},
    'T': {'pK1': 2.11, 'pK2': 9.62, 'pKR': None},
    'C': {'pK1': 1.96, 'pK2': 10.28, 'pKR': 8.18},
    'N': {'pK1': 2.02, 'pK2': 8.8, 'pKR': None},
    'Q': {'pK1': 2.17, 'pK2': 9.13, 'pKR': None},
    'K': {'pK1': 2.18, 'pK2': 8.95, 'pKR': 10.53},
    'H': {'pK1': 1.82, 'pK2': 9.17, 'pKR': 6.0},
    'R': {'pK1': 2.17, 'pK2': 9.04, 'pKR': 12.48},
    'D': {'pK1': 1.88, 'pK2': 9.6, 'pKR': 3.65},
    'E': {'pK1': 2.19, 'pK2': 9.67, 'pKR': 4.25}
}


pKa_values_lehninger_adjusted = {}
common_pK1 = 2.34
common_pK2 = 9.69
common_pKR = {
    'C': 8.33,
    'D': 3.86,
    'E': 4.25,
    'H': 6.0,
    'K': 10.5,
    'R': 12.4,
    'Y': 10.0
}
for aa in pKa_values_lehninger_book:
    pKa_values_lehninger_adjusted[aa] = {
        'pK1': common_pK1,
        'pK2': common_pK2,
        'pKR': common_pKR.get(aa)
    }

# Variable para el método

def obtener_pKa_dict():
    if valor_pKa_usado_var.get() == "Libro-Lehninger":
        return pKa_values_lehninger_book
    elif valor_pKa_usado_var.get() == "Lehninger-ajustado":
        return pKa_values_lehninger_adjusted
    elif valor_pKa_usado_var.get() == "Personalizado":
        return cargar_pKa_customizados()  # Cargar los valores personalizados
    else:
        return {}

def calcular_carga():
    secuencia = input_entry.get().strip().upper()
    if not secuencia:
        messagebox.showwarning("Secuencia faltante", "Por favor, ingrese una secuencia de aminoácidos.")
        return
    if output_text.get("1.0", tk.END).strip():
        output_text.insert(tk.END, "\n")
    if not secuencia:
        return

    try:
        ph = float(pH_entry.get())
    except ValueError:
        messagebox.showwarning("pH inválido", "Revisar si has introducido algún valor de pH.")
        return

    pKas = obtener_pKa_dict()
    carga_total = 0

    if not all(aa in pKas for aa in secuencia):
        output_text.insert(tk.END, "Secuencia inválida.\n")
        return

    # Grupo amino terminal (positivo)
    pk2 = pKas[secuencia[0]]['pK2']
    carga_total += 1 / (1 + 10**(ph - pk2))

    # Grupo carboxilo terminal (negativo)
    pk1 = pKas[secuencia[-1]]['pK1']
    carga_total += -1 / (1 + 10**(pk1 - ph))

    # Cadenas laterales
    for aa in secuencia:
        pKr = pKas[aa]['pKR']
        if pKr:
            if aa in ('D', 'E', 'C', 'Y'):
                carga_total += -1 / (1 + 10**(pKr - ph))
            elif aa in ('K', 'R', 'H'):
                carga_total += 1 / (1 + 10**(ph - pKr))

    output_text.insert(tk.END, f"pH: {ph} — Carga neta de la secuencia: {carga_total:.4f}\n")

def calcular_pI_Jatunov():
    secuencia = input_entry.get().strip().upper()
    if output_text.get("1.0", tk.END).strip():
        output_text.insert(tk.END, "\n")
    if not secuencia:
        messagebox.showwarning("Secuencia faltante", "Por favor, ingrese una secuencia de aminoácidos.")
        return

    valor_pKa_usado = valor_pKa_usado_var.get()
    if valor_pKa_usado == "Libro-Lehninger":
        pKa_values = pKa_values_lehninger_book
    elif valor_pKa_usado == "Lehninger-ajustado":
        pKa_values = pKa_values_lehninger_adjusted
    elif valor_pKa_usado == "Personalizado":
        pKa_values = cargar_pKa_customizados() 

    carga = 0
    pKa_utilizados = []

    if len(secuencia) == 1:
        aa = secuencia[0]
        datos = pKa_values.get(aa)
        if datos:
            if datos['pK1']:
                pKa_utilizados.append(datos['pK1'])
            if datos['pK2']:
                pKa_utilizados.append(datos['pK2'])
                if 1 < datos['pK2']:
                    carga += 1
            if datos['pKR']:
                pKa_utilizados.append(datos['pKR'])
                if aa in ('D', 'E', 'Y', 'C'):
                    if 1 > datos['pKR']:
                        carga -= 1
                elif aa in ('K', 'R', 'H'):
                    if 1 < datos['pKR']:
                        carga += 1
    else:
        primer = secuencia[0]
        ultimo = secuencia[-1]

        if pKa_values[primer]['pK2']:
            pKa_utilizados.append(pKa_values[primer]['pK2'])
            if 1 < pKa_values[primer]['pK2']:
                carga += 1

        if pKa_values[ultimo]['pK1']:
            pKa_utilizados.append(pKa_values[ultimo]['pK1'])

        for aa in secuencia:
            datos = pKa_values[aa]
            if datos['pKR']:
                pKa_utilizados.append(datos['pKR'])
                if aa in ('D', 'E', 'Y', 'C'):
                    if 1 > datos['pKR']:
                        carga -= 1
                elif aa in ('K', 'R', 'H'):
                    if 1 < datos['pKR']:
                        carga += 1

    pKa_utilizados.sort()
    carga_abs = abs(carga)

    if carga_abs == 0 or carga_abs >= len(pKa_utilizados):
        resultado = "No se puede calcular pI correctamente con los valores disponibles. Revisar si has ingresado los valores de los aminoácidos en cuestión"
    else:
        pI = (pKa_utilizados[carga_abs - 1] + pKa_utilizados[carga_abs]) / 2
        resultado = (
            f"pKa usado: {valor_pKa_usado}\n"
            f"Secuencia: {secuencia}\n"
            f"Carga visual a pH=1: {carga}\n"
            f"Valores de pKa usados (ordenados): {pKa_utilizados}\n"
            f"Se promedian los valores pKa #{carga_abs} y #{carga_abs + 1}: "
            f"({pKa_utilizados[carga_abs - 1]} + {pKa_utilizados[carga_abs]}) / 2\n"
            f"pI = {pI:.3f}"
        )
   
    output_text.insert(tk.END, resultado)

def carga_visual_pH(pH):
    
    secuencia = input_entry.get().strip().upper()
    if not secuencia:
        messagebox.showwarning("Secuencia faltante", "Por favor, ingrese una secuencia de aminoácidos.")
        return
    valor_pKa_usado = valor_pKa_usado_var.get()
    if valor_pKa_usado == "Libro-Lehninger":
        pKa_values = pKa_values_lehninger_book
    elif valor_pKa_usado == "Lehninger-ajustado":
        pKa_values = pKa_values_lehninger_adjusted
    elif valor_pKa_usado == "Personalizado":
        pKa_values = cargar_pKa_customizados()

    carga = 0.0
    detalles = []

    def contribucion_acida(pKa):
        if pKa is None:
            return 0
        if pH < pKa:
            return 0
        elif pH == pKa:
            return -0.5
        else:
            return -1

    def contribucion_basica(pKa):
        if pKa is None:
            return 0
        if pH < pKa:
            return +1
        elif pH == pKa:
            return +0.5
        else:
            return 0

    for i, aa in enumerate(secuencia):
        datos = pKa_values.get(aa, {})

        # N-terminal
        if i == 0:
            contrib = contribucion_basica(datos.get('pK2'))
            carga += contrib
            detalles.append((f" {aa}(N-ter)", contrib))

        # pKR cadena lateral
        pKR = datos.get('pKR')
        if pKR is not None:
            if aa in ('D', 'E', 'Y', 'C'):
                contrib = contribucion_acida(pKR)
            elif aa in ('K', 'R', 'H'):
                contrib = contribucion_basica(pKR)
            else:
                contrib = 0
            carga += contrib
            detalles.append((f"// {aa}(pKR)", contrib))

        # C-terminal
        if i == len(secuencia) - 1:
            contrib = contribucion_acida(datos.get('pK1'))
            carga += contrib
            detalles.append((f"// {aa}(C-ter)", contrib))

    # Configuramos los tags de colores si aún no existen
    if not "red" in output_text.tag_names():
        output_text.tag_configure("red", foreground="red")
    if not "blue" in output_text.tag_names():
        output_text.tag_configure("blue", foreground="blue")

    # Mostrar en el output_text
    output_text.insert('end', "Detalles del cálculo: ")

    for nombre, contrib in detalles:
        color = "red" if contrib > 0 else "blue"
        output_text.insert('end', f"{nombre}: ", color)
        output_text.insert('end', f"{contrib:+.1f} ", color)

    output_text.insert('end', f"Carga visual a pH {pH:.3f}: {carga:+.3f}")


def mostrar_carga_a_pH_visual():


    try:
        pH = float(pH_entry.get())
        carga_visual_pH(pH)
    except ValueError:
        messagebox.showwarning("Secuencia faltante", "Por favor, ingrese una secuencia de aminoácidos.")
        return

def calcular_pI_binario():
    secuencia = input_entry.get().strip().upper()
    if not secuencia:
        messagebox.showwarning("Secuencia faltante", "Por favor, ingrese una secuencia de aminoácidos.")
        return

    # Si el cuadro de texto no está vacío, agrega una línea en blanco primero
    if output_text.get("1.0", tk.END).strip():
        output_text.insert(tk.END, "\n")

    if not secuencia:
        output_text.insert(tk.END, "Secuencia vacía.")
        return

    pKas = obtener_pKa_dict()

    if not all(aa in pKas for aa in secuencia):
        output_text.insert(tk.END, "Secuencia inválida.\n")
        return

    def carga_a_pH(ph):
        carga_total = 0

        # Grupo amino terminal
        pk2 = pKas[secuencia[0]]['pK2']
        carga_total += 1 / (1 + 10**(ph - pk2))

        # Grupo carboxilo terminal
        pk1 = pKas[secuencia[-1]]['pK1']
        carga_total += -1 / (1 + 10**(pk1 - ph))

        # Cadenas laterales
        for aa in secuencia:
            pKr = pKas[aa]['pKR']
            if pKr:
                if aa in ('D', 'E', 'C', 'Y'):
                    carga_total += -1 / (1 + 10**(pKr - ph))
                elif aa in ('K', 'R', 'H'):
                    carga_total += 1 / (1 + 10**(ph - pKr))

        return carga_total

    # Búsqueda binaria
    low = 0.0
    high = 14.0
    max_iter = 200
    epsilon = 0.0001
    pI = None

    for _ in range(max_iter):
        mid = (low + high) / 2
        carga = carga_a_pH(mid)

        if abs(carga) < epsilon:
            pI = mid
            break

        if carga > 0:
            low = mid
        else:
            high = mid

    if pI is None:
        pI = (low + high) / 2  # Último valor estimado

    output_text.insert(tk.END, f"pI estimado por búsqueda binaria: {pI:.4f}")


def limpiar_cuadro_texto():
    output_text.delete("1.0", tk.END)

def mostrar_preguntas_discusion():
    output_text.delete("1.0", tk.END)  # Limpia el contenido previo
    texto = (
        "📌 PREGUNTAS PARA DISCUSIÓN\n\n"
        "1. ¿Por qué el pI calculado por el método jerárquico no coincide exactamente con la iteración binaria ?\n\n"
        "2. ¿Por qué pueden existir diferentes valores de pKa para un mismo aminoácido?\n\n"
        "3. ¿Qué es carga visual?\n\n"
        "4. ¿Por qué la carga visual a un pH no coincide exactamente con la carga neta calculada?\n"
    )
    output_text.insert(tk.END, texto)

def mostrar_version():
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Versión 1.0 — Desarrollado por Sorel Jatunov Santamaría, cualquier duda o colaboración escribir a sjatunov@gmail.com\n")

def abrir_ejemplo_visual():
    url = "https://drsorel.es/wp-content/uploads/2025/07/captura-software.jpg"
    webbrowser.open(url)




def determinar_movimiento():
    def procesar():
        try:
            pI = float(entry_pI.get())
            pH = float(entry_pH.get())

            ventana.destroy()  # Cierra la subventana

            if abs(pH - pI) <= 0.2:
                output_text.insert('end', f"\nDado un pI de {pI:.2f} y un pH de {pH:.2f}, la especie no se mueve en un campo eléctrico.\n")
            elif pH < pI:
                output_text.insert('end', f"\nDado un pI de {pI:.2f} y un pH de {pH:.2f}, la especie tiene carga positiva y migrará al polo negativo (cátodo).\n")
            else:
                output_text.insert('end', f"\nDado un pI de {pI:.2f} y un pH de {pH:.2f}, la especie tiene carga negativa y migrará al polo positivo (ánodo).\n")
        except ValueError:
            messagebox.showerror("Error", "Introduce valores numéricos válidos para pI y pH.")



    # Crear ventana emergente
    ventana = tk.Toplevel()
    ventana.title("Evaluar movimiento electroforético")
    ventana.geometry("300x150")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Introduce el pI:").pack(pady=5)
    entry_pI = tk.Entry(ventana)
    entry_pI.pack()

    tk.Label(ventana, text="Introduce el pH:").pack(pady=5)
    entry_pH = tk.Entry(ventana)
    entry_pH.pack()

    tk.Button(ventana, text="Evaluar movimiento", command=procesar).pack(pady=10)

# GUI
root = tk.Tk()
root.title("Calculadora de punto isoeléctrico (pI)- por Sorel Jatunov S. Versión 1.0")
valor_pKa_usado_var = tk.StringVar(value="Libro-Lehninger")
style = ttk.Style()
style.configure("Azul.TLabel", foreground="blue")
style.configure("Verde.TLabel", foreground="green")
# Contenido
frame = ttk.Frame(root, padding=10)
frame.pack()

ttk.Label(frame, text="Secuencia de aminoácidos:", style="Azul.TLabel").pack()
input_entry = ttk.Entry(frame, width=30)
input_entry.pack()

ttk.Button(frame, text="Calcular pI método jerárquico (método Jatunov)", command=calcular_pI_Jatunov).pack(pady=5)
ttk.Button(frame, text="Calcular pI iteración binaria ", command=calcular_pI_binario).pack(pady=5)

ttk.Label(frame, text="pH para calcular carga:", style="Verde.TLabel").pack()
pH_entry = ttk.Entry(frame, width=10)
pH_entry.pack()

ttk.Button(frame, text="Calcular carga neta a pH", command=calcular_carga).pack(pady=5)
ttk.Button(frame, text="Mostrar carga visual", command=mostrar_carga_a_pH_visual).pack(pady=5)

# Frame para Text + Scrollbar
text_scroll_frame = ttk.Frame(frame)
text_scroll_frame.pack(fill='both', expand=True)

scrollbar = ttk.Scrollbar(text_scroll_frame)
scrollbar.pack(side='right', fill='y')

output_text = tk.Text(text_scroll_frame, width=70, height=15, wrap="word", yscrollcommand=scrollbar.set)
output_text.pack(side='left', fill='both', expand=True)

scrollbar.config(command=output_text.yview)

ttk.Button(frame, text="Limpiar cuadro de texto", command=limpiar_cuadro_texto).pack(pady=5)

# Menú para método
menu_bar = tk.Menu(root)
menu_archivo = tk.Menu(menu_bar, tearoff=0)

menu_archivo.add_command(label="Abrir archivo pKa personalizado", command=mostrar_contenido_pKa)
menu_archivo.add_command(label="Guardar pKa personalizado", command=guardar_pKa_customizados)
menu_archivo.add_command(label="Guardar salida del cuadro de texto", command=guardar_salida_en_archivo)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

valor_pKa_usado_menu = tk.Menu(menu_bar, tearoff=0)
valor_pKa_usado_menu.add_radiobutton(label="Libro de Lehninger", variable=valor_pKa_usado_var, value="Libro-Lehninger")
valor_pKa_usado_menu.add_radiobutton(label="Lehninger-ajustado", variable=valor_pKa_usado_var, value="Lehninger-ajustado")
# Añadir una opción en el menú para seleccionar el método personalizado
valor_pKa_usado_menu.add_radiobutton(label="Personalizado", variable=valor_pKa_usado_var, value="Personalizado")

menu_bar.add_cascade(label="pKa usados", menu=valor_pKa_usado_menu)

menu_calculo = tk.Menu(menu_bar, tearoff=0)
menu_calculo.add_command(label="Determinar movimiento electroforético", command=determinar_movimiento)

menu_bar.add_cascade(label="Cálculo", menu=menu_calculo)

menu_discusion = tk.Menu(menu_bar, tearoff=0)
menu_discusion.add_command(label="Preguntas clave", command=mostrar_preguntas_discusion)
menu_bar.add_cascade(label="Discusión", menu=menu_discusion)

menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_ayuda.add_command(label="Versión 1.0 por Sorel Jatunov", command=mostrar_version)
menu_ayuda.add_command(label="Ejemplo visual", command=abrir_ejemplo_visual)
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

root.config(menu=menu_bar)
print("Esta es la rama de desarrollo dev")
# Ir trabajando en la versión en inglés.
root.mainloop()