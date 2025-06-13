

'''
Pseudocódigo:
Iniciar el programa

1. El sistema tiene varias listas importantes:
   - Una lista de alergias comunes (como mariscos, lactosa, etc.).
   - Una guía de qué dieta es mejor para cada tipo de alergia.
   - Un listado general de todas las dietas disponibles (omnivora, vegana, sin gluten, etc.).

2. Cuando el usuario hace clic en "Iniciar pedido":
   - Se le pregunta su nombre.
   - Se revisa si ese nombre ya está registrado con alguna alergia.

3. Si el sistema no tiene registrada su alergia:
   - Se le pregunta si tiene alguna.
   - Si dice que sí, se le muestra una lista con opciones para elegir.
   - Se guarda su nombre y la alergia que seleccionó.

4. A partir de su alergia (o si no tiene ninguna), se recomienda una dieta.
   - El sistema pregunta si desea seguir esa recomendación.
   - Si no quiere, se le permite elegir otra dieta manualmente.

5. Se abre el archivo del menú general y se filtran los productos según la dieta elegida.
   - Si el usuario tiene alergia, se eliminan del menú los productos que le puedan hacer daño (por ejemplo, si es alérgico a la lactosa, se quitan los quesos, pizzas, yogures, etc.).
   - Si no hay ningún producto disponible después del filtro, se le informa y se reinicia el proceso.

6. Si hay menú disponible:
   - Se muestra en una nueva ventana todo el menú filtrado.
   - Se le permite al usuario escribir qué productos quiere (con sus números).
   - También puede ver las reseñas que otros han dejado sobre esa dieta.

7. El sistema calcula cuánto cuestan los productos seleccionados.
   - Se le muestra al usuario el total a pagar y el listado de lo que eligió.
   - Se le pregunta si desea confirmar la compra.

8. Si confirma la compra:
   - Se le da la opción de dejar un comentario sobre la dieta.
   - Si escribe algo, se guarda en el archivo de reseñas.
   - Se le agradece por su compra y se cierra la aplicación.

9. Si cancela la compra:
   - Se le avisa que se reiniciará el pedido y puede empezar de nuevo.

(En algunas partes del código nos ayudamso de Chatgpt)

'''
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# --- Diccionarios ---
alergias = {
    1: "Ninguna alergia",
    2: "Alergia a la lactosa",
    3: "Alergia a mariscos",
    4: "Alergia al chocolate",
    5: "Alergia a colorantes artificiales"
}

dieta_por_alergia = {
    "Ninguna alergia": "OMNÍVORA",
    "Alergia a la lactosa": "SIN LACTOSA",
    "Alergia a mariscos": "OMNÍVORA",
    "Alergia al chocolate": "OMNÍVORA",
    "Alergia a colorantes artificiales": "OMNÍVORA"
}

opciones_dietas = {
    1: "OMNÍVORA",
    2: "VEGETARIANA",
    3: "VEGANA",
    4: "SIN GLUTEN",
    5: "SIN LACTOSA",
    6: "DIETA DASH"
}

# --- Funciones de lógica ---
def leer_menu(tipo_dieta):
    try:
        with open("menu.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        return []

    mostrar = False
    menu_dieta = []
    for linea in lineas:
        if linea.strip().upper().startswith(tipo_dieta.upper()):
            mostrar = True
            continue
        elif linea.strip().startswith("________________________________________"):
            mostrar = False
            continue

        if mostrar and linea.strip():
            menu_dieta.append(linea.strip())
    return menu_dieta

def registrar_alergia_usuario(nombre, alergia, archivo='nombres.txt'):
    nombre_formateado = nombre.strip().title()
    nombre_clave = nombre_formateado.lower()

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        lineas = []

    nombres_existentes = [
        linea.strip().lower().replace("nombre: ", "")
        for linea in lineas if linea.lower().startswith("nombre: ")
    ]

    if nombre_clave not in nombres_existentes:
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(f"Nombre: {nombre_formateado}\n")
            f.write(f"Alergia: {alergia}\n\n")

def obtener_alergia_usuario(nombre_busqueda, archivo='nombres.txt'):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        return "Ninguna alergia"

    nombre_formateado = nombre_busqueda.strip().title()
    for i in range(len(lineas)):
        if lineas[i].strip().lower() == f"nombre: {nombre_formateado.lower()}":
            if i + 1 < len(lineas) and lineas[i+1].strip().lower().startswith("alergia:"):
                return lineas[i+1].strip().replace("Alergia: ", "")
    return "Ninguna alergia"

def filtrar_menu_por_alergia(menu_dieta, alergia_usuario):
    alimentos_no_apto = {
        "Alergia a mariscos": ["camarón", "cangrejo", "langosta"],
        "Alergia al chocolate": ["galletas", "chocolates", "cinta negra", "giga clásica", "sandwiches"],
        "Alergia a colorantes artificiales": ["boquitas", "chicles", "galletas", "chocolates", "cinta negra",
            "cremosa naranja", "giga almendra", "giga clásica", "galleta", "paleta frutales", "sandwiches"],
        "Alergia a la lactosa": ["queso", "yogurt", "molletes", "waffles", "avena con leche",
            "pan dulce + café", "nachos con chilli y queso", "pizza", "cappuccino",
            "chai latte", "pan dulce", "galletas", "chocolates", "cinta negra",
            "cremosa", "giga", "galleta", "sandwiches"]
    }

    productos_prohibidos = set()
    for clave, palabras in alimentos_no_apto.items():
        if clave.lower() in alergia_usuario.lower():
            productos_prohibidos.update(palabras)

    menu_filtrado = []
    for linea in menu_dieta:
        if any(palabra.lower() in linea.lower() for palabra in productos_prohibidos):
            continue
        menu_filtrado.append(linea)
    return menu_filtrado

def guardar_resena(dieta, comentario, archivo='resenas.txt'):
    with open(archivo, 'a', encoding='utf-8') as f:
        f.write(f"Dieta: {dieta}\n")
        f.write(f"Comentario: {comentario}\n\n")

def leer_resenas(dieta, archivo='resenas.txt'):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except FileNotFoundError:
        return "No hay reseñas aún."

    secciones = contenido.strip().split("\n\n")
    resenas_filtradas = []
    for sec in secciones:
        if f"Dieta: {dieta}" in sec:
            for linea in sec.split("\n"):
                if linea.startswith("Comentario:"):
                    resenas_filtradas.append(linea.replace("Comentario:", "").strip())
    if not resenas_filtradas:
        return "No hay reseñas para esta dieta."
    return "\n\n".join(resenas_filtradas)

# Interfaz gráfica 

def mostrar_resultado_en_ventana(productos, total, dieta):
    global resultado_label
    if resultado_label:
        resultado_label.destroy()

    texto = "Productos seleccionados:\n" + "\n".join(productos) + f"\n\nTotal a pagar: ${total:.2f}"
    resultado_label = tk.Label(ventana, text=texto, justify="left", font=("Arial", 10), wraplength=280)
    resultado_label.pack(pady=10)

    def preguntar_compra():
        respuesta = messagebox.askyesno("Confirmar compra", "¿Desea realizar la compra?")
        if respuesta:
            comentario = simpledialog.askstring("Comentarios", "Gracias por su compra.\n¿Desea dejar un comentario sobre la dieta?")
            if comentario:
                guardar_resena(dieta, comentario)
            messagebox.showinfo("Compra finalizada", "Gracias por su compra.")
            ventana.quit()
        else:
            messagebox.showinfo("Compra cancelada", "Se reiniciará el pedido.")
            resultado_label.destroy()
            btn_iniciar_pedido.config(state=tk.NORMAL)

    btn_confirmar = tk.Button(ventana, text="Confirmar Compra / Cancelar", command=preguntar_compra)
    btn_confirmar.pack()

def ventana_seleccion_productos(menu_filtrado, dieta):
    sel_ventana = tk.Toplevel(ventana)
    sel_ventana.title("Selecciona productos")
    sel_ventana.geometry("350x400")

    label = tk.Label(sel_ventana, text="Menú disponible (escribe números separados por espacios):")
    label.pack()

    text_menu = scrolledtext.ScrolledText(sel_ventana, width=40, height=15)
    text_menu.pack()
    text_menu.insert(tk.END, "\n".join(menu_filtrado))
    text_menu.config(state='disabled')

    entry_seleccion = tk.Entry(sel_ventana, width=40)
    entry_seleccion.pack(pady=5)

    def mostrar_resenas():
        resenas = leer_resenas(dieta)
        messagebox.showinfo(f"Reseñas de {dieta}", resenas)

    btn_resenas = tk.Button(sel_ventana, text="Ver Reseñas", command=mostrar_resenas)
    btn_resenas.pack(pady=5)

    def confirmar_seleccion():
        seleccion = entry_seleccion.get()
        if not seleccion:
            messagebox.showwarning("Error", "Debe ingresar al menos un número.")
            return
        try:
            # Cambio aquí: separamos por espacios, no comas
            seleccion_numeros = [int(s.strip()) for s in seleccion.split() if s.strip().isdigit()]
        except Exception:
            messagebox.showwarning("Error", "Ingrese números válidos separados por espacios.")
            return

        total = 0.0
        productos_seleccionados = []

        for linea in menu_filtrado:
            for numero in seleccion_numeros:
                if linea.startswith(f"{numero}."):
                    productos_seleccionados.append(linea)
                    try:
                        precio_str = linea.split("$")[-1]
                        total += float(precio_str)
                    except ValueError:
                        pass

        if not productos_seleccionados:
            messagebox.showwarning("Error", "No se seleccionaron productos válidos.")
            return

        sel_ventana.destroy()
        mostrar_resultado_en_ventana(productos_seleccionados, total, dieta)

    btn_confirmar = tk.Button(sel_ventana, text="Confirmar selección", command=confirmar_seleccion)
    btn_confirmar.pack(pady=10)

def iniciar_app():
    btn_iniciar_pedido.config(state=tk.DISABLED)

    # Pide primero el nombre
    nombre_usuario = simpledialog.askstring("Nombre", "Por favor, ingrese su nombre:")
    if not nombre_usuario:
        messagebox.showerror("Error", "Debe ingresar un nombre.")
        btn_iniciar_pedido.config(state=tk.NORMAL)
        return

    # Ver si el usuario ya tiene alergia registrada
    alergia_guardada = obtener_alergia_usuario(nombre_usuario)

    if alergia_guardada == "Ninguna alergia":
        respuesta = messagebox.askyesno("Alergias", "¿Tiene alguna alergia?")
        if respuesta:
            # Si tiene alergia, preguntamos cuál
            alergia_opciones = "\n".join([f"{k}. {v}" for k, v in alergias.items() if v != "Ninguna alergia"])
            seleccion = simpledialog.askinteger("Seleccionar alergia", f"Seleccione el número de su alergia:\n{alergia_opciones}")
            alergia_usuario = alergias.get(seleccion, "Ninguna alergia")
        else:
            alergia_usuario = "Ninguna alergia"
    else:
        alergia_usuario = alergia_guardada
        messagebox.showinfo("Información", f"Se detectó que ya tiene registrada la alergia: {alergia_usuario}")

    # Guardar o actualizar la alergia del usuario
    registrar_alergia_usuario(nombre_usuario, alergia_usuario)

    # Determinar dieta recomendada
    dieta_recomendada = dieta_por_alergia.get(alergia_usuario, "OMNÍVORA")
    respuesta = messagebox.askyesno("Dieta recomendada", f"Le recomendamos la dieta {dieta_recomendada}. ¿Desea seleccionarla?")
    if not respuesta:
        # Si no acepta la recomendada, seleccionar dieta manualmente
        dietas_disp = "\n".join([f"{k}. {v}" for k, v in opciones_dietas.items()])
        seleccion_dieta = simpledialog.askinteger("Seleccione dieta", f"Seleccione la dieta:\n{dietas_disp}")
        dieta_seleccionada = opciones_dietas.get(seleccion_dieta, dieta_recomendada)
    else:
        dieta_seleccionada = dieta_recomendada

    # Leer menú
    menu_dieta = leer_menu(dieta_seleccionada)
    if alergia_usuario != "Ninguna alergia":
        menu_filtrado = filtrar_menu_por_alergia(menu_dieta, alergia_usuario)
    else:
        menu_filtrado = menu_dieta

    if not menu_filtrado:
        messagebox.showinfo("Menú", "No hay productos disponibles para la dieta seleccionada.")
        btn_iniciar_pedido.config(state=tk.NORMAL)
        return

    ventana_seleccion_productos(menu_filtrado, dieta_seleccionada)

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Sistema de Dietas")
ventana.geometry("400x450")

resultado_label = None

btn_iniciar_pedido = tk.Button(ventana, text="Iniciar pedido", command=iniciar_app)
btn_iniciar_pedido.pack(pady=20)

ventana.mainloop()





   

