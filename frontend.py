import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QComboBox, QHBoxLayout, QSizePolicy, QMessageBox, QSpacerItem,
    QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pyqtgraph import PlotWidget, mkPen
import numpy as np
import os 
from backend import procesar_senal 

class SignalSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Conversión de Señales")
        self.setGeometry(100, 100, 1400, 950) 

        try:
            self.init_ui()
            self.apply_styles() 
        except Exception as e:
            print(f"Error durante la inicialización de la UI: {e}")
            QMessageBox.critical(self, "Error de Inicio", f"No se pudo iniciar la interfaz de usuario: {e}. Por favor, revise el código y las dependencias.")
            sys.exit(1)

    def init_ui(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(70, 60, 70, 60)
        main_layout.setSpacing(25) 

        header_layout = QVBoxLayout()
        header_layout.setSpacing(15)

        self.title_label = QLabel("Simulador de Conversión de Señales")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("mainTitleLabel") 
        header_layout.addWidget(self.title_label)

        self.explanation_label = QLabel("Este simulador permite visualizar la transformación de señales analógicas a digitales (ADC), ajustando parámetros como el tipo de señal, la tasa de muestreo y la cuantización de bits.")
        self.explanation_label.setAlignment(Qt.AlignCenter)
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setObjectName("explanationLabel") 
        header_layout.addWidget(self.explanation_label)
        
        main_layout.addLayout(header_layout)

        # --- Sección de Función de la Señal ---
        func_section_layout = QVBoxLayout()
        func_section_layout.setSpacing(10)

        self.func_label = QLabel("Ingrese función de la señal analógica")
        self.func_label.setAlignment(Qt.AlignCenter)
        self.func_label.setObjectName("sectionHeaderLabel_func") 
        func_section_layout.addWidget(self.func_label)

        func_input_centered_layout = QHBoxLayout()
        func_input_centered_layout.addStretch()
        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("Función de la señal a convertir (ej: sin(2*pi*10*t))")
        self.func_input.setFixedHeight(55)
        self.func_input.setFixedWidth(600)
        func_input_centered_layout.addWidget(self.func_input)
        func_input_centered_layout.addStretch()
        func_section_layout.addLayout(func_input_centered_layout)

        main_layout.addLayout(func_section_layout)

        # --- Sección de Opciones (Tipo, Tasa, Cuantización) ---
        options_main_layout = QHBoxLayout()
        options_main_layout.addStretch()

        options_layout = QHBoxLayout()
        options_layout.setSpacing(30)

        # Columna 1: Tipo de Señal
        tipo_layout = QVBoxLayout()
        tipo_layout.setSpacing(10)
        self.tipo_label = QLabel("Ingrese el tipo de señal a convertir")
        self.tipo_label.setAlignment(Qt.AlignCenter)
        self.tipo_label.setObjectName("sectionHeaderLabel_tipo") 
        tipo_layout.addWidget(self.tipo_label)
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Senoidal", "Cuadrada", "Triangular", "Personalizada"])
        self.tipo_combo.setMinimumHeight(55)
        self.tipo_combo.setFixedWidth(250)
        tipo_layout.addWidget(self.tipo_combo, alignment=Qt.AlignCenter)
        options_layout.addLayout(tipo_layout)

        # Columna 2: Tasa de Muestreo
        fs_layout = QVBoxLayout()
        fs_layout.setSpacing(10)
        self.fs_label = QLabel("Ingrese la tasa de muestreo")
        self.fs_label.setAlignment(Qt.AlignCenter)
        self.fs_label.setObjectName("sectionHeaderLabel_fs") 
        fs_layout.addWidget(self.fs_label)
        self.fs_input = QLineEdit()
        self.fs_input.setPlaceholderText("Tasa de muestreo (kHz)")
        self.fs_input.setFixedHeight(55)
        self.fs_input.setFixedWidth(250)
        fs_layout.addWidget(self.fs_input, alignment=Qt.AlignCenter)
        options_layout.addLayout(fs_layout)

        # Columna 3: Cuantización de la Señal
        bits_layout = QVBoxLayout()
        bits_layout.setSpacing(10)
        self.bits_label = QLabel("Ingrese la cuantización de la señal")
        self.bits_label.setAlignment(Qt.AlignCenter)
        self.bits_label.setObjectName("sectionHeaderLabel_bits") 
        bits_layout.addWidget(self.bits_label)
        self.bits_input = QLineEdit()
        self.bits_input.setPlaceholderText("Cuantización (bits)")
        self.bits_input.setFixedHeight(55)
        self.bits_input.setFixedWidth(250)
        bits_layout.addWidget(self.bits_input, alignment=Qt.AlignCenter)
        options_layout.addLayout(bits_layout)
        
        options_main_layout.addLayout(options_layout)
        options_main_layout.addStretch()
        main_layout.addLayout(options_main_layout)

        # Fila para Frecuencia y Duración (centralizada)
        freq_dur_main_layout = QHBoxLayout()
        freq_dur_main_layout.addStretch()

        freq_dur_layout = QHBoxLayout()
        freq_dur_layout.setSpacing(30)

        # Frecuencia de señales predefinidas
        freq_layout = QVBoxLayout()
        freq_layout.setSpacing(10)
        self.freq_label = QLabel("Frecuencia (Hz)")
        self.freq_label.setAlignment(Qt.AlignCenter)
        self.freq_label.setObjectName("sectionHeaderLabel_freq") 
        freq_layout.addWidget(self.freq_label)
        self.freq_input = QLineEdit()
        self.freq_input.setPlaceholderText("Frec. Señales Predefinidas (Hz)")
        self.freq_input.setFixedHeight(55)
        self.freq_input.setFixedWidth(250)
        self.freq_input.setText("10.0")
        freq_layout.addWidget(self.freq_input, alignment=Qt.AlignCenter)
        freq_dur_layout.addLayout(freq_layout)

        # Duración de la señal
        duration_layout = QVBoxLayout()
        duration_layout.setSpacing(10)
        self.duration_label = QLabel("Duración (segundos)")
        self.duration_label.setAlignment(Qt.AlignCenter)
        self.duration_label.setObjectName("sectionHeaderLabel_duration") 
        duration_layout.addWidget(self.duration_label)
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Duración de la señal (s)")
        self.duration_input.setFixedHeight(55)
        self.duration_input.setFixedWidth(250)
        self.duration_input.setText("1.0")
        duration_layout.addWidget(self.duration_input, alignment=Qt.AlignCenter)
        freq_dur_layout.addLayout(duration_layout)
        
        freq_dur_main_layout.addLayout(freq_dur_layout)
        freq_dur_main_layout.addStretch()
        main_layout.addLayout(freq_dur_main_layout)

        # --- Botón de Simular ---
        sim_btn_layout = QHBoxLayout()
        sim_btn_layout.addStretch()
        self.simular_btn = QPushButton("Simular")
        self.simular_btn.clicked.connect(self.simular)
        self.simular_btn.setFixedSize(200, 60)
        sim_btn_layout.addWidget(self.simular_btn)
        sim_btn_layout.addStretch()
        main_layout.addLayout(sim_btn_layout)
        main_layout.addSpacing(25) # Espaciado antes del gráfico

        # --- Sección del Gráfico ---
        graph_header_layout = QHBoxLayout()
        graph_header_layout.setSpacing(60)
        self.graph_title_label = QLabel("Señal Analógica vs Señal Digitalizada")
        self.graph_title_label.setObjectName("sectionHeaderLabel_graph") 
        graph_header_layout.addWidget(self.graph_title_label)
        graph_header_layout.addStretch()

        # Leyenda manual para replicar el mockup
        legend_layout = QHBoxLayout()
        legend_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        analog_color_box = QLabel("")
        analog_color_box.setFixedSize(18, 18)
        analog_color_box.setStyleSheet("background-color: red; border-radius: 9px;")
        legend_layout.addWidget(analog_color_box)
        legend_layout.addWidget(QLabel("Señal analógica"))
        legend_layout.addSpacing(20)

        digital_color_box = QLabel("")
        digital_color_box.setFixedSize(18, 18)
        digital_color_box.setStyleSheet("background-color: blue; border-radius: 9px;")
        legend_layout.addWidget(digital_color_box)
        legend_layout.addWidget(QLabel("Señal digitalizada"))

        graph_header_layout.addLayout(legend_layout)
        main_layout.addLayout(graph_header_layout)

        self.plot_widget = PlotWidget()
        self.plot_widget.setMinimumHeight(350) 
        self.plot_widget.setLabel('left', 'Amplitud')
        self.plot_widget.setLabel('bottom', 'Tiempo (s)')
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        main_layout.addWidget(self.plot_widget, stretch=1)

        scroll_area.setWidget(content_widget)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll_area)
        
        self.setLayout(window_layout)


    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
            background-color: #1A2E40;
            color: #ECEFF1;
            font-family: 'Segoe UI', Arial;
            font-size: 15px;
            }
            
            QLabel#mainTitleLabel {
                font-size: 48px;
                font-weight: bold;
                color: #00B0FF;
            }
            
            QLabel#explanationLabel {
                background-color: #263645;
                border-radius: 16px;
                padding: 20px;
                font-size: 20px;
                color: #CFD8DC;
            }
            
            QLabel#sectionHeaderLabel_graph {
                font-size: 24px;
                margin-top: 30px;
                font-weight: bold;
                color: #ECEFF1;
            }
            
            QLineEdit, QComboBox {
                background-color: #ECEFF1;
                color: #1A2E40;
                border: 2px solid #90CAF9;
                border-radius: 10px;
                padding: 12px 14px;
                min-height: 45px;
                font-size: 20px;
            }
            
            QPushButton {
                background-color: #00B0FF;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 22px;
                font-weight: bold;
                border-radius: 12px;
                margin-top: 15px;
            }
            
            QPushButton:hover {
                background-color: #0288D1;
            }
            
            QPushButton:pressed {
                background-color: #0277BD;
                padding-top: 16px;
                padding-bottom: 14px;
            }
            
            PlotWidget {
                background-color: #000000;
                border-radius: 14px;
                border: 2px solid #37474F;
            }
            
            QLabel#footerLabel {
                font-size: 14px;
                padding-top: 20px;
                color: #90A4AE;
            }
            
            QLabel#inputLabel {
                font-size: 18px;
                font-weight: bold;
                color: #BBDEFB;
            }
            
            QLabel#footerLabel {
                font-size: 16px;
                font-weight: bold;
                padding-top: 20px;
                color: #B0BEC5;
            }
        """)

    def simular(self):
        try:
            tipo = self.tipo_combo.currentText()
            fs = float(self.fs_input.text()) * 1000  # kHz → Hz
            bits = int(self.bits_input.text())
            funcion = self.func_input.text()
            duracion = float(self.duration_input.text())
            frecuencia_predefinida = float(self.freq_input.text())

            if fs <= 0 or bits <= 0 or duracion <= 0 or frecuencia_predefinida <= 0:
                QMessageBox.warning(self, "Error de Entrada", "Por favor, ingrese valores numéricos válidos y mayores que cero para todos los campos.")
                return

            if tipo == "Personalizada" and funcion.strip() == "":
                QMessageBox.warning(self, "Error de Entrada", "Debe ingresar una función para la señal personalizada.")
                return

            t, analog, digital = procesar_senal(tipo, fs, bits, funcion, duracion, frecuencia_predefinida) 

            self.plot_widget.clear()

            if len(t) > 0 and len(analog) > 0 and len(digital) > 0:
                self.plot_widget.plot(t, analog, pen=mkPen('red', width=2), name="Señal Analógica")

                # Preparar señal digitalizada (azul en escalones)
                if len(t) > 1:
                    t_step = (t[-1] - t[0]) / (len(t) - 1)
                else:
                    t_step = 1.0 / fs 
                
                t_digital_extended = np.zeros(len(digital) + 1)
                t_digital_extended[:-1] = t[:len(digital)]
                t_digital_extended[-1] = t_digital_extended[-2] + t_step

                digital_extended = digital 

                self.plot_widget.plot(
                    t_digital_extended,
                    digital_extended,
                    pen=mkPen('blue', width=2),
                    stepMode=True,
                    name="Señal Digitalizada"
                )

                self.plot_widget.setXRange(t.min(), t.max())
                self.plot_widget.autoRange()
            else:
                QMessageBox.warning(self, "Error de Simulación", "No se pudieron generar datos para graficar. Verifique sus parámetros de entrada.")
        except ValueError:
            QMessageBox.warning(self, "Error de Entrada", "Por favor, ingrese valores numéricos válidos para Tasa de muestreo, Cuantización, Duración y Frecuencia.")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SignalSimulator()
    ventana.show()
    sys.exit(app.exec_())