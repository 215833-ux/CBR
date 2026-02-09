import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

class DCPRealTimeAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("DCP ANALYZER PRO - Análisis en Tiempo Real")
        self.root.geometry("1400x950")
        
        # Configurar colores profesionales
        self.colors = {
            'primary': '#1a5276',      # Azul oscuro
            'secondary': '#28b463',    # Verde
            'accent': '#e74c3c',       # Rojo
            'dark': '#2c3e50',         # Gris oscuro
            'light': '#f8f9f9',        # Blanco hueso
            'warning': '#f39c12',      # Naranja
            'success': '#27ae60',      # Verde éxito
            'purple': '#8e44ad',       # Morado
            'blue_light': '#5dade2',   # Azul claro
            'gray': '#bdc3c7',         # Gris claro
            'info': '#17a2b8',         # Azul información
        }
        
        self.root.configure(bg=self.colors['light'])
        
        # Variables
        self.lecturas = []
        self.dcpi_values = []
        self.cbr_values = []
        self.profundidades = []
        
        # Crear interfaz optimizada
        self.create_widgets()
        
    def create_widgets(self):
        """Crear interfaz optimizada"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ===== CABECERA COMPACTA =====
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="🔬 DCP ANALYZER PRO - Análisis Estadístico",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['primary'],
                              fg='white')
        title_label.pack(expand=True)
        
        # ===== CUERPO PRINCIPAL - 2 COLUMNAS =====
        body_frame = tk.Frame(main_frame, bg=self.colors['light'])
        body_frame.pack(fill='both', expand=True)
        
        # ===== COLUMNA IZQUIERDA: GRUPOS DE RESULTADOS =====
        left_column = tk.Frame(body_frame, bg=self.colors['light'], width=350)
        left_column.pack(side='left', fill='y', padx=(0, 10))
        
        # ===== ENTRADA DE DATOS COMPACTA =====
        input_frame = tk.Frame(left_column, bg='white', relief='solid', bd=1, pady=10)
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Posición inicial
        tk.Label(input_frame,
                text="Posición Inicial (Golpe 0):",
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg=self.colors['dark'],
                padx=10).pack(side='left')
        
        self.lectura_0_var = tk.StringVar(value="30.0")
        tk.Entry(input_frame,
                textvariable=self.lectura_0_var,
                font=('Segoe UI', 10),
                bg='white',
                relief='solid',
                bd=1,
                width=10,
                justify='center').pack(side='left', padx=(0, 5))
        
        tk.Label(input_frame,
                text="mm",
                font=('Segoe UI', 10),
                bg='white',
                fg=self.colors['gray']).pack(side='left')
        
        # ===== GRUPOS DE RESULTADOS =====
        # Grupo 1: Datos Generales
        group1_card = tk.Frame(left_column, bg='white', relief='solid', bd=1)
        group1_card.pack(fill='x', pady=(0, 5))
        
        group1_header = tk.Frame(group1_card, bg=self.colors['info'])
        group1_header.pack(fill='x')
        
        tk.Label(group1_header,
                text="📏 DATOS GENERALES",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['info'],
                fg='white',
                padx=10,
                pady=5).pack()
        
        group1_content = tk.Frame(group1_card, bg='white', padx=10, pady=10)
        group1_content.pack(fill='x')
        
        self.group1_labels = {}
        group1_data = [
            ("Posición inicial:", "0.0 mm"),
            ("Profundidad final:", "0.0 mm"),
            ("N° de golpes:", "15"),
            ("Penetración total:", "0.0 mm")
        ]
        
        for label_text, value_text in group1_data:
            label_frame = tk.Frame(group1_content, bg='white')
            label_frame.pack(fill='x', pady=2)
            
            tk.Label(label_frame,
                    text=label_text,
                    font=('Segoe UI', 9),
                    bg='white',
                    fg=self.colors['dark'],
                    width=15,
                    anchor='w').pack(side='left')
            
            value_label = tk.Label(label_frame,
                                  text=value_text,
                                  font=('Segoe UI', 9, 'bold'),
                                  bg='white',
                                  fg=self.colors['info'])
            value_label.pack(side='right')
            self.group1_labels[label_text] = value_label
        
        # Grupo 2: Estadísticas DCPI
        group2_card = tk.Frame(left_column, bg='white', relief='solid', bd=1)
        group2_card.pack(fill='x', pady=(0, 5))
        
        group2_header = tk.Frame(group2_card, bg=self.colors['secondary'])
        group2_header.pack(fill='x')
        
        tk.Label(group2_header,
                text="📊 ESTADÍSTICAS DCPI",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['secondary'],
                fg='white',
                padx=10,
                pady=5).pack()
        
        group2_content = tk.Frame(group2_card, bg='white', padx=10, pady=10)
        group2_content.pack(fill='x')
        
        self.group2_labels = {}
        group2_data = [
            ("DCPI promedio:", "0.0 mm/golpe"),
            ("Desv. estándar:", "0.0 mm/golpe"),
            ("Mínimo DCPI:", "0.0 mm/golpe"),
            ("Máximo DCPI:", "0.0 mm/golpe")
        ]
        
        for label_text, value_text in group2_data:
            label_frame = tk.Frame(group2_content, bg='white')
            label_frame.pack(fill='x', pady=2)
            
            tk.Label(label_frame,
                    text=label_text,
                    font=('Segoe UI', 9),
                    bg='white',
                    fg=self.colors['dark'],
                    width=15,
                    anchor='w').pack(side='left')
            
            value_label = tk.Label(label_frame,
                                  text=value_text,
                                  font=('Segoe UI', 9, 'bold'),
                                  bg='white',
                                  fg=self.colors['secondary'])
            value_label.pack(side='right')
            self.group2_labels[label_text] = value_label
        
        # Grupo 3: Estadísticas CBR
        group3_card = tk.Frame(left_column, bg='white', relief='solid', bd=1)
        group3_card.pack(fill='x', pady=(0, 5))
        
        group3_header = tk.Frame(group3_card, bg=self.colors['accent'])
        group3_header.pack(fill='x')
        
        tk.Label(group3_header,
                text="📈 ESTADÍSTICAS CBR",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['accent'],
                fg='white',
                padx=10,
                pady=5).pack()
        
        group3_content = tk.Frame(group3_card, bg='white', padx=10, pady=10)
        group3_content.pack(fill='x')
        
        self.group3_labels = {}
        group3_data = [
            ("CBR promedio:", "0.0 %"),
            ("Desv. estándar:", "0.0 %"),
            ("Mínimo CBR:", "0.0 %"),
            ("Máximo CBR:", "0.0 %")
        ]
        
        for label_text, value_text in group3_data:
            label_frame = tk.Frame(group3_content, bg='white')
            label_frame.pack(fill='x', pady=2)
            
            tk.Label(label_frame,
                    text=label_text,
                    font=('Segoe UI', 9),
                    bg='white',
                    fg=self.colors['dark'],
                    width=15,
                    anchor='w').pack(side='left')
            
            value_label = tk.Label(label_frame,
                                  text=value_text,
                                  font=('Segoe UI', 9, 'bold'),
                                  bg='white',
                                  fg=self.colors['accent'])
            value_label.pack(side='right')
            self.group3_labels[label_text] = value_label
        
        # ===== BOTONES =====
        button_frame = tk.Frame(left_column, bg=self.colors['light'], pady=10)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame,
                 text="🔍 CALCULAR",
                 font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['success'],
                 fg='white',
                 command=self.calculate,
                 padx=20,
                 pady=8).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(button_frame,
                 text="🗑️ LIMPIAR",
                 font=('Segoe UI', 10),
                 bg=self.colors['warning'],
                 fg='white',
                 command=self.clear_data,
                 padx=20,
                 pady=8).pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Botón para ingreso manual de datos
        tk.Button(left_column,
                 text="✏️ INGRESAR DATOS MANUALES",
                 font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['purple'],
                 fg='white',
                 command=self.open_data_entry,
                 padx=20,
                 pady=8).pack(fill='x', pady=(10, 0))
        
        # ===== COLUMNA DERECHA: TABLA Y GRÁFICOS =====
        right_column = tk.Frame(body_frame, bg=self.colors['light'])
        right_column.pack(side='right', fill='both', expand=True)
        
        # ===== FRAME SUPERIOR: TABLA DE LECTURAS (AHORA MÁS GRANDE) =====
        table_frame = tk.Frame(right_column, bg=self.colors['light'])
        table_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Tarjeta para tabla
        table_card = tk.Frame(table_frame, bg='white', relief='solid', bd=1)
        table_card.pack(fill='both', expand=True)
        
        table_header = tk.Frame(table_card, bg=self.colors['primary'])
        table_header.pack(fill='x')
        
        tk.Label(table_header,
                text="📝 TABLA DE LECTURAS Y CÁLCULOS",
                font=('Segoe UI', 11, 'bold'),
                bg=self.colors['primary'],
                fg='white',
                padx=15,
                pady=6).pack()
        
        # Frame para tabla con scroll
        table_content = tk.Frame(table_card, bg='white')
        table_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview con más filas visibles
        self.tree = ttk.Treeview(table_content, 
                                columns=('Golpe', 'Profundidad', 'Delta', 'DCPI', 'CBR'),
                                show='headings',
                                height=18)  # Aumentado de 12 a 18 filas visibles
        
        # Configurar encabezados
        self.tree.heading('Golpe', text='Golpe')
        self.tree.heading('Profundidad', text='Profundidad (mm)')
        self.tree.heading('Delta', text='Δ (mm)')
        self.tree.heading('DCPI', text='DCPI (mm/golpe)')
        self.tree.heading('CBR', text='CBR (%)')
        
        # Configurar columnas
        self.tree.column('Golpe', width=60, anchor='center')
        self.tree.column('Profundidad', width=120, anchor='center')  # Más ancho
        self.tree.column('Delta', width=90, anchor='center')  # Más ancho
        self.tree.column('DCPI', width=120, anchor='center')  # Más ancho
        self.tree.column('CBR', width=90, anchor='center')  # Más ancho
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_content, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # ===== FRAME INFERIOR: GRÁFICOS MÁS GRANDES =====
        graphs_frame = tk.Frame(right_column, bg=self.colors['light'])
        graphs_frame.pack(fill='both', expand=True)
        
        # Frame para gráficos en grid 1x3
        graphs_grid = tk.Frame(graphs_frame, bg=self.colors['light'])
        graphs_grid.pack(fill='both', expand=True)
        
        # Gráfico 1: Penetración acumulada
        graph1_frame = tk.Frame(graphs_grid, bg='white', relief='solid', bd=1)
        graph1_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=(0, 5))
        
        graph1_header = tk.Frame(graph1_frame, bg=self.colors['blue_light'])
        graph1_header.pack(fill='x')
        
        tk.Label(graph1_header,
                text="📈 PENETRACIÓN ACUMULADA",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['blue_light'],
                fg='white',
                padx=10,
                pady=4).pack()
        
        self.graph1_canvas_frame = tk.Frame(graph1_frame, bg='white')
        self.graph1_canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Gráfico 2: DCPI vs Profundidad
        graph2_frame = tk.Frame(graphs_grid, bg='white', relief='solid', bd=1)
        graph2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=(0, 5))
        
        graph2_header = tk.Frame(graph2_frame, bg=self.colors['purple'])
        graph2_header.pack(fill='x')
        
        tk.Label(graph2_header,
                text="📊 DCPI vs PROFUNDIDAD",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['purple'],
                fg='white',
                padx=10,
                pady=4).pack()
        
        self.graph2_canvas_frame = tk.Frame(graph2_frame, bg='white')
        self.graph2_canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Gráfico 3: CBR vs Profundidad
        graph3_frame = tk.Frame(graphs_grid, bg='white', relief='solid', bd=1)
        graph3_frame.grid(row=0, column=2, sticky='nsew', padx=(5, 0), pady=(0, 5))
        
        graph3_header = tk.Frame(graph3_frame, bg=self.colors['accent'])
        graph3_header.pack(fill='x')
        
        tk.Label(graph3_header,
                text="📈 CBR vs PROFUNDIDAD",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['accent'],
                fg='white',
                padx=10,
                pady=4).pack()
        
        self.graph3_canvas_frame = tk.Frame(graph3_frame, bg='white')
        self.graph3_canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configurar pesos del grid para 3 columnas
        graphs_grid.grid_columnconfigure(0, weight=1)
        graphs_grid.grid_columnconfigure(1, weight=1)
        graphs_grid.grid_columnconfigure(2, weight=1)
        graphs_grid.grid_rowconfigure(0, weight=1)
        
        # Crear gráficos iniciales
        self.create_initial_graphs()
        
        # Inicializar tabla vacía
        self.initialize_table()
    
    def initialize_table(self):
        """Inicializar tabla con datos vacíos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar golpe 0
        self.tree.insert('', 'end', values=("0", self.lectura_0_var.get(), "-", "-", "-"))
        
        # Insertar 15 filas vacías
        for i in range(1, 16):
            self.tree.insert('', 'end', values=(i, "", "", "", ""))
    
    def create_initial_graphs(self):
        """Crear gráficos iniciales vacíos"""
        # Gráfico 1: Penetración acumulada - MÁS GRANDE
        self.fig1, self.ax1 = plt.subplots(figsize=(5, 3.5), dpi=85)
        self.ax1.set_title('Penetración Acumulada', fontsize=11, fontweight='bold')
        self.ax1.set_xlabel('Número de Golpe', fontsize=9)
        self.ax1.set_ylabel('Profundidad (mm)', fontsize=9)
        self.ax1.grid(True, alpha=0.3, linestyle='--')
        self.ax1.set_xlim(0, 15)
        self.ax1.set_ylim(0, 600)
        self.ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.graph1_canvas_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(fill='both', expand=True)
        
        # Gráfico 2: DCPI vs Profundidad - MÁS GRANDE
        self.fig2, self.ax2 = plt.subplots(figsize=(5, 3.5), dpi=85)
        self.ax2.set_title('DCPI vs Profundidad', fontsize=11, fontweight='bold')
        self.ax2.set_xlabel('Profundidad (mm)', fontsize=9)
        self.ax2.set_ylabel('DCPI (mm/golpe)', fontsize=9)
        self.ax2.grid(True, alpha=0.3, linestyle='--')
        self.ax2.set_xlim(0, 600)
        self.ax2.set_ylim(0, 100)
        
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.graph2_canvas_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(fill='both', expand=True)
        
        # Gráfico 3: CBR vs Profundidad - MÁS GRANDE
        self.fig3, self.ax3 = plt.subplots(figsize=(5, 3.5), dpi=85)
        self.ax3.set_title('CBR vs Profundidad', fontsize=11, fontweight='bold')
        self.ax3.set_xlabel('Profundidad (mm)', fontsize=9)
        self.ax3.set_ylabel('CBR (%)', fontsize=9)
        self.ax3.grid(True, alpha=0.3, linestyle='--')
        self.ax3.set_xlim(0, 600)
        self.ax3.set_ylim(0, 100)
        
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.graph3_canvas_frame)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().pack(fill='both', expand=True)
    
    def open_data_entry(self):
        """Abrir ventana para ingreso manual de datos"""
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Ingreso Manual de Datos")
        entry_window.geometry("500x700")
        entry_window.configure(bg=self.colors['light'])
        entry_window.transient(self.root)
        entry_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(entry_window, bg=self.colors['light'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tk.Label(main_frame,
                text="📝 INGRESO DE LECTURAS DCP",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['light'],
                fg=self.colors['primary'],
                pady=10).pack()
        
        # Instrucciones
        tk.Label(main_frame,
                text="Ingrese las lecturas de profundidad (mm) para cada golpe:",
                font=('Segoe UI', 10),
                bg=self.colors['light'],
                fg=self.colors['dark'],
                pady=5).pack()
        
        # Frame para entradas
        entries_frame = tk.Frame(main_frame, bg=self.colors['light'])
        entries_frame.pack(fill='both', expand=True, pady=10)
        
        self.entry_widgets = []
        
        # Crear 15 entradas
        for i in range(1, 16):
            row_frame = tk.Frame(entries_frame, bg=self.colors['light'])
            row_frame.pack(fill='x', pady=2)
            
            tk.Label(row_frame,
                    text=f"Golpe {i}:",
                    font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['light'],
                    fg=self.colors['dark'],
                    width=8,
                    anchor='w').pack(side='left')
            
            entry_var = tk.StringVar()
            entry = tk.Entry(row_frame,
                           textvariable=entry_var,
                           font=('Segoe UI', 10),
                           bg='white',
                           relief='solid',
                           bd=1,
                           width=15)
            entry.pack(side='left', padx=5)
            
            tk.Label(row_frame,
                    text="mm",
                    font=('Segoe UI', 9),
                    bg=self.colors['light'],
                    fg=self.colors['gray']).pack(side='left')
            
            self.entry_widgets.append(entry_var)
            
            # Cargar valor actual si existe
            items = self.tree.get_children()
            if len(items) > i:
                current_val = self.tree.item(items[i])['values'][1]
                if current_val:
                    entry_var.set(current_val)
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg=self.colors['light'], pady=20)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame,
                 text="💾 GUARDAR DATOS",
                 font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['success'],
                 fg='white',
                 command=lambda: self.save_manual_data(entry_window),
                 padx=20,
                 pady=10).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(button_frame,
                 text="❌ CANCELAR",
                 font=('Segoe UI', 11),
                 bg=self.colors['accent'],
                 fg='white',
                 command=entry_window.destroy,
                 padx=20,
                 pady=10).pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Cargar datos de ejemplo
        tk.Button(main_frame,
                 text="📋 CARGAR DATOS DE EJEMPLO",
                 font=('Segoe UI', 10),
                 bg=self.colors['info'],
                 fg='white',
                 command=self.load_example_to_entries,
                 padx=15,
                 pady=8).pack(pady=10)
    
    def load_example_to_entries(self):
        """Cargar datos de ejemplo en las entradas"""
        example_values = [100, 185, 256, 345, 380, 423, 455, 
                         480, 505, 515, 523, 528, 531, 535, 538]
        
        for i, value in enumerate(example_values):
            if i < len(self.entry_widgets):
                self.entry_widgets[i].set(f"{value}")
    
    def save_manual_data(self, window):
        """Guardar datos ingresados manualmente"""
        try:
            # Limpiar tabla actual
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar golpe 0
            self.tree.insert('', 'end', values=("0", self.lectura_0_var.get(), "-", "-", "-"))
            
            # Insertar datos
            for i, entry_var in enumerate(self.entry_widgets):
                value = entry_var.get().strip()
                if value:
                    try:
                        lectura = float(value)
                        self.tree.insert('', 'end', values=(
                            i + 1,
                            f"{lectura:.1f}",
                            "",
                            "",
                            ""
                        ))
                    except ValueError:
                        self.tree.insert('', 'end', values=(i + 1, "", "", "", ""))
                else:
                    self.tree.insert('', 'end', values=(i + 1, "", "", "", ""))
            
            # Rellenar filas faltantes
            current_items = len(self.tree.get_children())
            if current_items < 16:
                for i in range(current_items, 16):
                    self.tree.insert('', 'end', values=(i, "", "", "", ""))
            
            window.destroy()
            messagebox.showinfo("Éxito", "Datos guardados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos:\n{str(e)}")
    
    def calculate(self):
        """Realizar cálculos a partir de la tabla"""
        try:
            # Obtener posición inicial
            lectura_0 = float(self.lectura_0_var.get())
            self.lecturas = [lectura_0]
            
            # Obtener valores de la tabla
            items = list(self.tree.get_children())
            
            # Verificar que tenemos 16 filas (golpe 0 + 15)
            if len(items) != 16:
                messagebox.showerror("Error", "Debe tener exactamente 15 lecturas")
                return
            
            # Obtener todas las lecturas
            lecturas_completas = []
            for i, item_id in enumerate(items):
                values = self.tree.item(item_id)['values']
                if i == 0:  # Golpe 0
                    lecturas_completas.append(lectura_0)
                else:
                    if values[1] and values[1].strip():
                        try:
                            lectura = float(values[1])
                            lecturas_completas.append(lectura)
                        except ValueError:
                            messagebox.showerror("Error", f"Valor inválido en golpe {i}")
                            return
                    else:
                        messagebox.showerror("Error", f"Falta lectura en golpe {i}")
                        return
            
            self.lecturas = lecturas_completas
            
            # Calcular valores
            self.dcpi_values = []
            self.cbr_values = []
            self.profundidades = []
            
            # Actualizar tabla con cálculos
            for i in range(1, len(items)):  # Comenzar desde el golpe 1
                delta = self.lecturas[i] - self.lecturas[i-1]
                dcpi = delta  # DCPI es la penetración por golpe
                profundidad_media = (self.lecturas[i] + self.lecturas[i-1]) / 2
                
                # Calcular CBR usando la fórmula correcta
                # CBR = 292 / (DCPI^1.12) donde DCPI está en mm/golpe
                if dcpi > 0:
                    cbr_golpe = 292 / (dcpi ** 1.12)
                else:
                    cbr_golpe = 0
                
                # Limitar CBR a un máximo de 100%
                cbr_golpe = min(cbr_golpe, 100)
                
                self.dcpi_values.append(dcpi)
                self.cbr_values.append(cbr_golpe)
                self.profundidades.append(profundidad_media)
                
                # Actualizar fila en la tabla
                item_id = items[i]
                self.tree.item(item_id, values=(
                    i,
                    f"{self.lecturas[i]:.1f}",
                    f"{delta:.1f}",
                    f"{dcpi:.2f}",
                    f"{cbr_golpe:.1f}"
                ))
            
            # Calcular estadísticas
            self.calculate_statistics()
            
            # Actualizar gráficos
            self.update_graphs()
            
            messagebox.showinfo("Éxito", "Cálculos completados correctamente!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {str(e)}")
    
    def calculate_statistics(self):
        """Calcular estadísticas"""
        if not self.dcpi_values or not self.cbr_values:
            return
        
        # Cálculos básicos
        penetracion_total = self.lecturas[-1] - self.lecturas[0] if len(self.lecturas) > 0 else 0
        dcpi_promedio = np.mean(self.dcpi_values) if len(self.dcpi_values) > 0 else 0
        
        # Estadísticas DCPI
        dcpi_std = np.std(self.dcpi_values) if len(self.dcpi_values) > 0 else 0
        dcpi_min = np.min(self.dcpi_values) if len(self.dcpi_values) > 0 else 0
        dcpi_max = np.max(self.dcpi_values) if len(self.dcpi_values) > 0 else 0
        
        # Estadísticas CBR
        cbr_promedio = np.mean(self.cbr_values) if len(self.cbr_values) > 0 else 0
        cbr_std = np.std(self.cbr_values) if len(self.cbr_values) > 0 else 0
        cbr_min = np.min(self.cbr_values) if len(self.cbr_values) > 0 else 0
        cbr_max = np.max(self.cbr_values) if len(self.cbr_values) > 0 else 0
        
        # Actualizar grupos
        # Grupo 1: Datos Generales
        self.group1_labels["Posición inicial:"].config(text=f"{self.lecturas[0]:.1f} mm")
        if len(self.lecturas) > 15:
            self.group1_labels["Profundidad final:"].config(text=f"{self.lecturas[15]:.1f} mm")
        else:
            self.group1_labels["Profundidad final:"].config(text="0.0 mm")
        self.group1_labels["N° de golpes:"].config(text="15")
        self.group1_labels["Penetración total:"].config(text=f"{penetracion_total:.1f} mm")
        
        # Grupo 2: Estadísticas DCPI
        self.group2_labels["DCPI promedio:"].config(text=f"{dcpi_promedio:.2f} mm/golpe")
        self.group2_labels["Desv. estándar:"].config(text=f"{dcpi_std:.2f} mm/golpe")
        self.group2_labels["Mínimo DCPI:"].config(text=f"{dcpi_min:.1f} mm/golpe")
        self.group2_labels["Máximo DCPI:"].config(text=f"{dcpi_max:.1f} mm/golpe")
        
        # Grupo 3: Estadísticas CBR
        self.group3_labels["CBR promedio:"].config(text=f"{cbr_promedio:.1f} %")
        self.group3_labels["Desv. estándar:"].config(text=f"{cbr_std:.2f} %")
        self.group3_labels["Mínimo CBR:"].config(text=f"{cbr_min:.1f} %")
        self.group3_labels["Máximo CBR:"].config(text=f"{cbr_max:.1f} %")
        
        # Guardar parámetros para gráficos
        self.params = {
            'penetracion_total': penetracion_total,
            'dcpi_promedio': dcpi_promedio,
            'cbr_promedio': cbr_promedio,
            'dcpi_std': dcpi_std,
            'cbr_std': cbr_std,
            'dcpi_min': dcpi_min,
            'dcpi_max': dcpi_max,
            'cbr_min': cbr_min,
            'cbr_max': cbr_max
        }
    
    def update_graphs(self):
        """Actualizar gráficos con mejoras visuales"""
        if not hasattr(self, 'params'):
            return
        
        params = self.params
        
        # Gráfico 1: Penetración acumulada - MEJORADO
        self.ax1.clear()
        golpes = list(range(0, 16))
        
        # Línea principal con marcadores mejorados
        self.ax1.plot(golpes, self.lecturas, 'o-', 
                     linewidth=2.5, 
                     markersize=6,
                     color=self.colors['blue_light'],
                     markerfacecolor='white',
                     markeredgewidth=2,
                     markeredgecolor=self.colors['blue_light'])
        
        # Área sombreada debajo de la curva
        self.ax1.fill_between(golpes, 0, self.lecturas, 
                             alpha=0.15, color=self.colors['blue_light'])
        
        self.ax1.set_title('Penetración Acumulada', fontsize=12, fontweight='bold')
        self.ax1.set_xlabel('Número de Golpe', fontsize=10)
        self.ax1.set_ylabel('Profundidad (mm)', fontsize=10)
        self.ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        self.ax1.set_xlim(-0.5, 15.5)
        self.ax1.set_xticks(golpes)
        
        # Resaltar el golpe final
        if len(self.lecturas) > 15:
            self.ax1.scatter(15, self.lecturas[15], s=100, color=self.colors['accent'], 
                            zorder=5, edgecolors='white', linewidth=2)
            
            # Anotar valor final
            self.ax1.annotate(f'{self.lecturas[15]:.0f} mm', 
                             xy=(15, self.lecturas[15]),
                             xytext=(12, self.lecturas[15] + 20),
                             fontsize=9,
                             arrowprops=dict(arrowstyle='->', color=self.colors['accent']))
        
        max_prof = max(self.lecturas) * 1.2 if max(self.lecturas) > 0 else 100
        self.ax1.set_ylim(0, max_prof)
        
        # Gráfico 2: DCPI vs Profundidad - MEJORADO
        self.ax2.clear()
        
        if len(self.dcpi_values) > 0:
            # Gráfico de dispersión con tamaño variable
            sizes = 40 + (np.array(self.profundidades) / 600 * 80)
            scatter = self.ax2.scatter(self.profundidades, self.dcpi_values,
                           color=self.colors['purple'],
                           s=sizes, alpha=0.8, edgecolors='white', linewidth=1)
            
            # Línea de tendencia polinómica
            if len(self.profundidades) > 2:
                try:
                    z = np.polyfit(self.profundidades, self.dcpi_values, 2)
                    p = np.poly1d(z)
                    x_smooth = np.linspace(min(self.profundidades), max(self.profundidades), 100)
                    self.ax2.plot(x_smooth, p(x_smooth),
                                 color=self.colors['purple'],
                                 linestyle='-', alpha=0.8, linewidth=2.5,
                                 label='Tendencia')
                except:
                    pass
            
            # Línea de promedio
            self.ax2.axhline(y=params['dcpi_promedio'],
                            color=self.colors['success'],
                            linestyle='-',
                            linewidth=2.5,
                            label=f'Promedio: {params["dcpi_promedio"]:.1f}')
            
            # Área de desviación estándar
            self.ax2.axhspan(params['dcpi_promedio'] - params['dcpi_std'],
                            params['dcpi_promedio'] + params['dcpi_std'],
                            alpha=0.2, color=self.colors['gray'],
                            label='±1 Desv. Estándar')
            
            # Líneas de mínimo y máximo
            self.ax2.axhline(y=params['dcpi_min'],
                            color=self.colors['success'],
                            linestyle='--',
                            linewidth=1.5,
                            alpha=0.7,
                            label=f'Mín: {params["dcpi_min"]:.1f}')
            
            self.ax2.axhline(y=params['dcpi_max'],
                            color=self.colors['warning'],
                            linestyle='--',
                            linewidth=1.5,
                            alpha=0.7,
                            label=f'Máx: {params["dcpi_max"]:.1f}')
            
            # Leyenda mejorada
            self.ax2.legend(fontsize=8, loc='upper right', framealpha=0.9)
        
        self.ax2.set_title('DCPI vs Profundidad', fontsize=12, fontweight='bold')
        self.ax2.set_xlabel('Profundidad (mm)', fontsize=10)
        self.ax2.set_ylabel('DCPI (mm/golpe)', fontsize=10)
        self.ax2.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        
        if len(self.profundidades) > 0:
            min_prof = min(self.profundidades) * 0.9
            max_prof = max(self.profundidades) * 1.1
            self.ax2.set_xlim(min_prof, max_prof)
            
            max_dcpi = max(self.dcpi_values) * 1.4 if max(self.dcpi_values) > 0 else 50
            self.ax2.set_ylim(0, max_dcpi)
        
        # Gráfico 3: CBR vs Profundidad - MEJORADO Y CORREGIDO
        self.ax3.clear()
        
        if len(self.cbr_values) > 0 and len(self.profundidades) > 0:
            # Gráfico de dispersión con colores según valor de CBR
            colors_cbr = []
            for cbr in self.cbr_values:
                if cbr < 5:
                    colors_cbr.append(self.colors['accent'])
                elif cbr < 15:
                    colors_cbr.append(self.colors['warning'])
                elif cbr < 30:
                    colors_cbr.append(self.colors['success'])
                else:
                    colors_cbr.append(self.colors['secondary'])
            
            # Tamaño variable según CBR
            sizes_cbr = 50 + (np.array(self.cbr_values) / 100 * 70)
            
            # Asegurarse de que tenemos datos para graficar
            scatter = self.ax3.scatter(self.profundidades, self.cbr_values,
                                       color=colors_cbr,
                                       s=sizes_cbr, alpha=0.85, edgecolors='white', 
                                       linewidth=1.5, zorder=3)
            
            # Línea de tendencia (si hay suficientes puntos)
            if len(self.profundidades) > 1:
                try:
                    # Ordenar los datos por profundidad
                    sorted_indices = np.argsort(self.profundidades)
                    prof_sorted = np.array(self.profundidades)[sorted_indices]
                    cbr_sorted = np.array(self.cbr_values)[sorted_indices]
                    
                    # Suavizar con interpolación
                    if len(prof_sorted) > 3:
                        # Usar polinomio de grado 2 para la tendencia
                        z = np.polyfit(prof_sorted, cbr_sorted, 2)
                        p = np.poly1d(z)
                        prof_smooth = np.linspace(min(prof_sorted), max(prof_sorted), 100)
                        cbr_smooth = p(prof_smooth)
                        
                        # Graficar línea de tendencia
                        self.ax3.plot(prof_smooth, cbr_smooth,
                                     color=self.colors['dark'],
                                     linestyle='-', alpha=0.8, linewidth=2.5,
                                     label='Tendencia', zorder=2)
                    else:
                        # Línea simple si no hay suficientes puntos
                        self.ax3.plot(prof_sorted, cbr_sorted,
                                     color=self.colors['dark'],
                                     linestyle='-', alpha=0.8, linewidth=2.5,
                                     label='Tendencia', zorder=2)
                except Exception as e:
                    print(f"Error al crear tendencia: {e}")
                    # Línea simple de conexión
                    self.ax3.plot(self.profundidades, self.cbr_values,
                                 color=self.colors['dark'],
                                 linestyle='-', alpha=0.5, linewidth=1.5,
                                 label='Tendencia', zorder=2)
            
            # Línea de promedio
            if 'cbr_promedio' in params:
                self.ax3.axhline(y=params['cbr_promedio'],
                                color=self.colors['success'],
                                linestyle='-',
                                linewidth=2,
                                label=f'Promedio: {params["cbr_promedio"]:.1f}%',
                                zorder=1)
            
            # Área de desviación estándar
            if 'cbr_promedio' in params and 'cbr_std' in params:
                self.ax3.axhspan(params['cbr_promedio'] - params['cbr_std'],
                                params['cbr_promedio'] + params['cbr_std'],
                                alpha=0.2, color=self.colors['gray'],
                                label=f'±1σ: {params["cbr_std"]:.1f}%',
                                zorder=0)
            
            # Líneas de mínimo y máximo
            if 'cbr_min' in params:
                self.ax3.axhline(y=params['cbr_min'],
                                color=self.colors['blue_light'],
                                linestyle='--',
                                linewidth=1.5,
                                alpha=0.7,
                                label=f'Mín: {params["cbr_min"]:.1f}%',
                                zorder=1)
            
            if 'cbr_max' in params:
                self.ax3.axhline(y=params['cbr_max'],
                                color=self.colors['warning'],
                                linestyle='--',
                                linewidth=1.5,
                                alpha=0.7,
                                label=f'Máx: {params["cbr_max"]:.1f}%',
                                zorder=1)
            
            # Zonas de calidad CBR
            self.ax3.axhspan(0, 5, alpha=0.08, color=self.colors['accent'], zorder=0)
            self.ax3.axhspan(5, 15, alpha=0.08, color=self.colors['warning'], zorder=0)
            self.ax3.axhspan(15, 30, alpha=0.08, color=self.colors['success'], zorder=0)
            self.ax3.axhspan(30, 100, alpha=0.08, color=self.colors['secondary'], zorder=0)
            
            # Leyenda compacta
            self.ax3.legend(fontsize=7, loc='upper right', ncol=2, framealpha=0.9)
        
        self.ax3.set_title('CBR vs Profundidad', fontsize=12, fontweight='bold')
        self.ax3.set_xlabel('Profundidad (mm)', fontsize=10)
        self.ax3.set_ylabel('CBR (%)', fontsize=10)
        self.ax3.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, zorder=0)
        
        # Establecer límites apropiados
        if len(self.profundidades) > 0:
            min_prof = max(0, min(self.profundidades) - 10)
            max_prof = max(600, max(self.profundidades) + 10)
            self.ax3.set_xlim(min_prof, max_prof)
            
            # Configurar ticks del eje X
            x_ticks = np.arange(0, max_prof + 100, 100)
            self.ax3.set_xticks(x_ticks)
            
            # Configurar límites del eje Y (CBR siempre entre 0-100%)
            self.ax3.set_ylim(0, 100)
            y_ticks = np.arange(0, 101, 20)
            self.ax3.set_yticks(y_ticks)
        else:
            # Valores por defecto si no hay datos
            self.ax3.set_xlim(0, 600)
            self.ax3.set_ylim(0, 100)
            self.ax3.set_xticks(np.arange(0, 601, 100))
            self.ax3.set_yticks(np.arange(0, 101, 20))
        
        # Ajustar layout para mejor visualización
        self.fig1.tight_layout()
        self.fig2.tight_layout()
        self.fig3.tight_layout()
        
        # Actualizar canvas
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
    
    def clear_data(self):
        """Limpiar datos"""
        self.lectura_0_var.set("30.0")
        
        # Limpiar tabla
        self.initialize_table()
        
        # Restablecer grupos
        self.group1_labels["Posición inicial:"].config(text="0.0 mm")
        self.group1_labels["Profundidad final:"].config(text="0.0 mm")
        self.group1_labels["N° de golpes:"].config(text="15")
        self.group1_labels["Penetración total:"].config(text="0.0 mm")
        
        self.group2_labels["DCPI promedio:"].config(text="0.0 mm/golpe")
        self.group2_labels["Desv. estándar:"].config(text="0.0 mm/golpe")
        self.group2_labels["Mínimo DCPI:"].config(text="0.0 mm/golpe")
        self.group2_labels["Máximo DCPI:"].config(text="0.0 mm/golpe")
        
        # Grupo 3 actualizado con desviación estándar
        self.group3_labels["CBR promedio:"].config(text="0.0 %")
        self.group3_labels["Desv. estándar:"].config(text="0.0 %")
        self.group3_labels["Mínimo CBR:"].config(text="0.0 %")
        self.group3_labels["Máximo CBR:"].config(text="0.0 %")
        
        # Restablecer gráficos
        self.create_initial_graphs()

def main():
    root = tk.Tk()
    
    # Configurar posición centrada
    root.update_idletasks()
    width = 1400
    height = 950
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Configurar fuente
    root.option_add('*Font', ('Segoe UI', 9))
    
    app = DCPRealTimeAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
