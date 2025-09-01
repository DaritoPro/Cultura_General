import pygame
import sys
import random

pygame.init()
pygame.font.init()

# --- CONSTANTES ---
ANCHO, ALTO = 800, 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (220, 220, 220)
GRIS_OSCURO = (50, 50, 50)
VERDE_PASTEL = (144, 238, 144)
AZUL_ACUAMARINA = (102, 205, 170)
ROJO = (220, 20, 60)

# Colores botones respuestas (4 colores distintos, no oscuros ni blancos)
COLOR_RESPUESTAS = [
    (255, 165, 0),   # naranja
    (65, 105, 225),  # royal blue
    (255, 105, 180), # hot pink
    (60, 179, 113)   # medium sea green
]

# Puntos por dificultad
PUNTOS = {
    "facil": 2,
    "normal": 5,
    "dificil": 10,
    "muy dificil": 15
}

# Fuentes
FUENTE_TITULO = pygame.font.SysFont("arial", 48)
FUENTE_SUBTITULO = pygame.font.SysFont("arial", 36)
FUENTE_NORMAL = pygame.font.SysFont("arial", 24)
FUENTE_PEQUENA = pygame.font.SysFont("arial", 20)

# Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Knight Mind")

# Reloj
reloj = pygame.time.Clock()

# --- CLASES ---

class Boton:
    def __init__(self, rect, color, texto, texto_color=NEGRO, fuente=FUENTE_NORMAL):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.texto = texto
        self.texto_color = texto_color
        self.fuente = fuente
        self.hover = False

    def dibujar(self, superficie, modo_oscuro=False):
        color_actual = self.color
        if modo_oscuro:
            # Ajustar color para modo oscuro (excepto botones de respuestas)
            if self.color in COLOR_RESPUESTAS:
                color_actual = self.color  # no cambia
            else:
                # Hacer color más claro para modo oscuro
                color_actual = tuple(min(255, c + 80) for c in self.color)
        if self.hover:
            # Hacer el color un poco más claro al pasar el mouse
            color_actual = tuple(min(255, c + 40) for c in color_actual)
        pygame.draw.rect(superficie, color_actual, self.rect, border_radius=8)
        # Texto centrado
        texto_render = self.fuente.render(self.texto, True, self.texto_color if not modo_oscuro else GRIS_OSCURO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, texto_rect)

    def esta_sobre(self, pos):
        return self.rect.collidepoint(pos)

class Pregunta:
    def __init__(self, texto, opciones, correcta, dificultad, tipo):
        """
        texto: str
        opciones: list de 4 strings (para VF, opciones serán ["Verdadero", "Falso", "", ""])
        correcta: índice 0-3 de la respuesta correcta
        dificultad: "facil", "normal", "dificil", "muy dificil"
        tipo: "vf" o "multiple"
        """
        self.texto = texto
        self.opciones = opciones
        self.correcta = correcta
        self.dificultad = dificultad
        self.tipo = tipo

# --- PREGUNTAS ---

# Para balancear, pondremos aprox 15 preguntas por dificultad
# Preguntas bien formuladas, sin errores, en español, respuestas cortas

preguntas_facil = [
    Pregunta("El sol es una estrella.", ["Verdadero", "Falso", "", ""], 0, "facil", "vf"),
    Pregunta("¿Cuál es el color del cielo en un día despejado?", ["Azul", "Verde", "Rojo", "Amarillo"], 0, "facil", "multiple"),
    Pregunta("El agua hierve a 100 grados Celsius.", ["Verdadero", "Falso", "", ""], 0, "facil", "vf"),
    Pregunta("¿Cuántos días tiene una semana?", ["5", "7", "10", "12"], 1, "facil", "multiple"),
    Pregunta("La Tierra es plana.", ["Verdadero", "Falso", "", ""], 1, "facil", "vf"),
    Pregunta("¿Cuál es el animal que dice 'miau'?", ["Perro", "Gato", "Pájaro", "Vaca"], 1, "facil", "multiple"),
    Pregunta("El hielo es agua congelada.", ["Verdadero", "Falso", "", ""], 0, "facil", "vf"),
    Pregunta("¿Qué planeta es conocido como el planeta rojo?", ["Venus", "Marte", "Júpiter", "Saturno"], 1, "facil", "multiple"),
    Pregunta("Los humanos tienen cinco sentidos.", ["Verdadero", "Falso", "", ""], 0, "facil", "vf"),
    Pregunta("¿Cuál es la capital de España?", ["Madrid", "Barcelona", "Sevilla", "Valencia"], 0, "facil", "multiple"),
    Pregunta("El fuego es frío.", ["Verdadero", "Falso", "", ""], 1, "facil", "vf"),
    Pregunta("¿Qué instrumento tiene teclas y se toca con las manos?", ["Guitarra", "Piano", "Batería", "Violín"], 1, "facil", "multiple"),
    Pregunta("El aire es invisible.", ["Verdadero", "Falso", "", ""], 0, "facil", "vf"),
    Pregunta("¿Cuántos colores tiene el arcoíris?", ["5", "6", "7", "8"], 2, "facil", "multiple"),
    Pregunta("Los peces pueden respirar fuera del agua.", ["Verdadero", "Falso", "", ""], 1, "facil", "vf"),
]

preguntas_normal = [
    Pregunta("La capital de Francia es París.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
    Pregunta("¿Cuál es el símbolo químico del oro?", ["Au", "Ag", "Fe", "Pb"], 0, "normal", "multiple"),
    Pregunta("El cuerpo humano tiene 206 huesos.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
    Pregunta("¿Quién escribió 'Don Quijote'?", ["Miguel de Cervantes", "Gabriel García Márquez", "Pablo Neruda", "Jorge Luis Borges"], 0, "normal", "multiple"),
    Pregunta("La luz viaja más rápido que el sonido.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
    Pregunta("¿Cuál es el río más largo del mundo?", ["Nilo", "Amazonas", "Yangtsé", "Misisipi"], 1, "normal", "multiple"),
    Pregunta("El planeta Júpiter es el más grande del sistema solar.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
    Pregunta("¿En qué año llegó el hombre a la Luna?", ["1965", "1969", "1972", "1959"], 1, "normal", "multiple"),
    Pregunta("El ADN está presente en todas las células vivas.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
    Pregunta("¿Cuál es la moneda oficial de Japón?", ["Yen", "Won", "Dólar", "Euro"], 0, "normal", "multiple"),
    Pregunta("La Gran Muralla China es visible desde el espacio.", ["Verdadero", "Falso", "", ""], 1, "normal", "vf"),
    Pregunta("¿Quién pintó 'La última cena'?", ["Leonardo da Vinci", "Miguel Ángel", "Pablo Picasso", "Vincent van Gogh"], 0, "normal", "multiple"),
    Pregunta("El oxígeno es necesario para la combustión.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
    Pregunta("¿Cuál es el idioma más hablado en el mundo?", ["Inglés", "Mandarín", "Español", "Hindi"], 1, "normal", "multiple"),
    Pregunta("La electricidad se mide en amperios.", ["Verdadero", "Falso", "", ""], 0, "normal", "vf"),
]

preguntas_dificil = [
    Pregunta("La teoría de la relatividad fue propuesta por Albert Einstein.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
    Pregunta("¿Cuál es la fórmula química del ácido sulfúrico?", ["H2SO4", "HCl", "NaOH", "CO2"], 0, "dificil", "multiple"),
    Pregunta("La capital de Mongolia es Ulán Bator.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
    Pregunta("¿Quién es el autor de 'Cien años de soledad'?", ["Gabriel García Márquez", "Mario Vargas Llosa", "Julio Cortázar", "Isabel Allende"], 0, "dificil", "multiple"),
    Pregunta("El bosón de Higgs fue descubierto en 2012.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
    Pregunta("¿Cuál es el elemento con número atómico 26?", ["Hierro", "Cobre", "Zinc", "Plomo"], 0, "dificil", "multiple"),
    Pregunta("La penicilina fue descubierta por Alexander Fleming.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
    Pregunta("¿Qué país tiene la mayor cantidad de islas?", ["Suecia", "Indonesia", "Filipinas", "Canadá"], 0, "dificil", "multiple"),
    Pregunta("La fotosíntesis ocurre en las mitocondrias.", ["Verdadero", "Falso", "", ""], 1, "dificil", "vf"),
    Pregunta("¿Cuál es la capital de Kazajistán?", ["Astana", "Tashkent", "Bishkek", "Dushanbe"], 0, "dificil", "multiple"),
    Pregunta("El número pi es un número irracional.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
    Pregunta("¿Quién compuso la Novena Sinfonía?", ["Beethoven", "Mozart", "Bach", "Chopin"], 0, "dificil", "multiple"),
    Pregunta("La velocidad de la luz es aproximadamente 300,000 km/s.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
    Pregunta("¿Cuál es el idioma oficial de Brasil?", ["Portugués", "Español", "Inglés", "Francés"], 0, "dificil", "multiple"),
    Pregunta("La teoría cuántica explica el comportamiento de partículas subatómicas.", ["Verdadero", "Falso", "", ""], 0, "dificil", "vf"),
]

preguntas_muy_dificil = [
    Pregunta("¿En qué año se firmó el Tratado de Westfalia?", ["1648", "1618", "1715", "1789"], 0, "muy dificil", "multiple"),
    Pregunta("La constante de Planck tiene unidades de acción.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿Quién desarrolló la teoría del psicoanálisis?", ["Sigmund Freud", "Carl Jung", "Alfred Adler", "Ivan Pavlov"], 0, "muy dificil", "multiple"),
    Pregunta("El número e es una constante matemática irracional.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿Cuál es la capital de Bután?", ["Thimphu", "Katmandú", "Dhaka", "Lhasa"], 0, "muy dificil", "multiple"),
    Pregunta("La mecánica clásica no explica el comportamiento de electrones.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿Quién escribió 'El Capital'?", ["Karl Marx", "Friedrich Engels", "Max Weber", "Adam Smith"], 0, "muy dificil", "multiple"),
    Pregunta("La entropía mide el desorden en un sistema.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿Cuál es el símbolo químico del tungsteno?", ["W", "Tu", "Tg", "Wt"], 0, "muy dificil", "multiple"),
    Pregunta("La paradoja de Schrödinger es un experimento mental en física.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿En qué año comenzó la Revolución Francesa?", ["1789", "1776", "1804", "1812"], 0, "muy dificil", "multiple"),
    Pregunta("La teoría de cuerdas intenta unificar la gravedad y la mecánica cuántica.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿Quién pintó 'El jardín de las delicias'?", ["Hieronymus Bosch", "El Bosco", "Pieter Bruegel", "Caravaggio"], 0, "muy dificil", "multiple"),
    Pregunta("La fotosíntesis produce oxígeno como subproducto.", ["Verdadero", "Falso", "", ""], 0, "muy dificil", "vf"),
    Pregunta("¿Cuál es la capital de Liechtenstein?", ["Vaduz", "Zúrich", "Berna", "Ginebra"], 0, "muy dificil", "multiple"),
]

# --- FUNCIONES DE SELECCIÓN DE PREGUNTAS ---

def seleccionar_pregunta(dificultad):
    """
    Retorna una pregunta según la dificultad seleccionada y las probabilidades indicadas.
    """
    if dificultad == "facil":
        # 80% facil, 20% normal (poca probabilidad)
        r = random.random()
        if r < 0.8:
            return random.choice(preguntas_facil)
        else:
            return random.choice(preguntas_normal)
    elif dificultad == "normal":
        # Solo normal
        return random.choice(preguntas_normal)
    elif dificultad == "dificil":
        # 70% dificil, 25% normal, 5% muy dificil (>=2%)
        r = random.random()
        if r < 0.7:
            return random.choice(preguntas_dificil)
        elif r < 0.95:
            return random.choice(preguntas_normal)
        else:
            return random.choice(preguntas_muy_dificil)
    else:
        # Por defecto normal
        return random.choice(preguntas_normal)

# --- CLASES DE PANTALLAS ---

class PantallaInicio:
    def __init__(self, juego):
        self.juego = juego
        self.titulo = "Knight Mind"
        # Botones
        self.boton_jugar = Boton((ANCHO//2 - 100, ALTO//2 + 50, 200, 50), VERDE_PASTEL, "JUGAR")
        self.boton_config = Boton((ANCHO//2 - 100, ALTO//2 + 120, 200, 50), AZUL_ACUAMARINA, "CONFIGURACIÓN")

    def manejar_eventos(self, eventos):
        pos = pygame.mouse.get_pos()
        self.boton_jugar.hover = self.boton_jugar.esta_sobre(pos)
        self.boton_config.hover = self.boton_config.esta_sobre(pos)
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.boton_jugar.esta_sobre(pos):
                    self.juego.cambiar_pantalla("seleccion_dificultad")
                elif self.boton_config.esta_sobre(pos):
                    self.juego.cambiar_pantalla("configuracion")

    def dibujar(self, superficie):
        superficie.fill(GRIS_CLARO if not self.juego.modo_oscuro else GRIS_OSCURO)
        # Titulo centrado en la parte superior (no tan arriba)
        texto_titulo = FUENTE_TITULO.render(self.titulo, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO//2, ALTO//4))
        superficie.blit(texto_titulo, rect_titulo)
        # Botones
        self.boton_jugar.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_config.dibujar(superficie, self.juego.modo_oscuro)

class PantallaSeleccionDificultad:
    def __init__(self, juego):
        self.juego = juego
        self.titulo = "Selecciona la dificultad"
        # Botones dificultad
        self.boton_facil = Boton((ANCHO//2 - 150, ALTO//2 - 80, 300, 60), VERDE_PASTEL, "FÁCIL")
        self.boton_normal = Boton((ANCHO//2 - 150, ALTO//2, 300, 60), AZUL_ACUAMARINA, "NORMAL")
        self.boton_dificil = Boton((ANCHO//2 - 150, ALTO//2 + 80, 300, 60), ROJO, "DIFÍCIL")
        self.boton_regresar = Boton((50, ALTO - 70, 120, 40), GRIS_CLARO, "REGRESAR", fuente=FUENTE_PEQUENA)

    def manejar_eventos(self, eventos):
        pos = pygame.mouse.get_pos()
        self.boton_facil.hover = self.boton_facil.esta_sobre(pos)
        self.boton_normal.hover = self.boton_normal.esta_sobre(pos)
        self.boton_dificil.hover = self.boton_dificil.esta_sobre(pos)
        self.boton_regresar.hover = self.boton_regresar.esta_sobre(pos)
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.boton_facil.esta_sobre(pos):
                    self.juego.iniciar_juego("facil")
                elif self.boton_normal.esta_sobre(pos):
                    self.juego.iniciar_juego("normal")
                elif self.boton_dificil.esta_sobre(pos):
                    self.juego.iniciar_juego("dificil")
                elif self.boton_regresar.esta_sobre(pos):
                    self.juego.cambiar_pantalla("inicio")

    def dibujar(self, superficie):
        superficie.fill(GRIS_CLARO if not self.juego.modo_oscuro else GRIS_OSCURO)
        # Titulo
        texto_titulo = FUENTE_SUBTITULO.render(self.titulo, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO//2, ALTO//4))
        superficie.blit(texto_titulo, rect_titulo)
        # Botones
        self.boton_facil.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_normal.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_dificil.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_regresar.dibujar(superficie, self.juego.modo_oscuro)

class PantallaJuego:
    def __init__(self, juego, dificultad):
        self.juego = juego
        self.dificultad = dificultad
        self.preguntas_respondidas = 0
        self.preguntas_correctas = 0
        self.puntos_totales = 0
        self.pregunta_actual = None
        self.botones_respuestas = []
        self.mostrar_resultado = False
        self.resultado_correcto = False
        self.respuesta_correcta_texto = ""
        self.siguiente_pregunta()

    def siguiente_pregunta(self):
        if self.preguntas_respondidas >= 15:
            self.juego.finalizar_juego(self.preguntas_correctas, self.preguntas_respondidas - self.preguntas_correctas, self.puntos_totales)
            return
        
        self.pregunta_actual = seleccionar_pregunta(self.dificultad)
        self.botones_respuestas = []
        
        # Crear botones para las respuestas
        if self.pregunta_actual.tipo == "vf":
            # Solo 2 botones para verdadero/falso
            self.botones_respuestas.append(Boton((ANCHO//2 - 150, ALTO//2 + 30, 300, 50), COLOR_RESPUESTAS[0], self.pregunta_actual.opciones[0]))
            self.botones_respuestas.append(Boton((ANCHO//2 - 150, ALTO//2 + 100, 300, 50), COLOR_RESPUESTAS[1], self.pregunta_actual.opciones[1]))
        else:
            # 4 botones para múltiple choice (2 arriba, 2 abajo)
            self.botones_respuestas.append(Boton((ANCHO//2 - 320, ALTO//2 + 30, 300, 50), COLOR_RESPUESTAS[0], self.pregunta_actual.opciones[0]))
            self.botones_respuestas.append(Boton((ANCHO//2 + 20, ALTO//2 + 30, 300, 50), COLOR_RESPUESTAS[1], self.pregunta_actual.opciones[1]))
            self.botones_respuestas.append(Boton((ANCHO//2 - 320, ALTO//2 + 100, 300, 50), COLOR_RESPUESTAS[2], self.pregunta_actual.opciones[2]))
            self.botones_respuestas.append(Boton((ANCHO//2 + 20, ALTO//2 + 100, 300, 50), COLOR_RESPUESTAS[3], self.pregunta_actual.opciones[3]))
        
        self.mostrar_resultado = False

    def manejar_eventos(self, eventos):
        if self.mostrar_resultado:
            # Esperar click para continuar
            for e in eventos:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.preguntas_respondidas += 1
                    self.siguiente_pregunta()
            return
            
        pos = pygame.mouse.get_pos()
        for boton in self.botones_respuestas:
            boton.hover = boton.esta_sobre(pos)
            
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, boton in enumerate(self.botones_respuestas):
                    if boton.esta_sobre(pos):
                        if i == self.pregunta_actual.correcta:
                            self.resultado_correcto = True
                            self.preguntas_correctas += 1
                            self.puntos_totales += PUNTOS[self.pregunta_actual.dificultad]
                            self.respuesta_correcta_texto = ""
                        else:
                            self.resultado_correcto = False
                            self.respuesta_correcta_texto = f"Respuesta correcta: {self.pregunta_actual.opciones[self.pregunta_actual.correcta]}"
                        self.mostrar_resultado = True
                        break

    def dibujar(self, superficie):
        superficie.fill(GRIS_CLARO if not self.juego.modo_oscuro else GRIS_OSCURO)
        
        if self.mostrar_resultado:
            # Mostrar resultado de la respuesta
            if self.resultado_correcto:
                texto_resultado = FUENTE_SUBTITULO.render("¡Bien Hecho!", True, (0, 100, 0))
            else:
                texto_resultado = FUENTE_SUBTITULO.render("¡Buen Intento!", True, (150, 0, 0))
            
            rect_resultado = texto_resultado.get_rect(center=(ANCHO//2, ALTO//3))
            superficie.blit(texto_resultado, rect_resultado)
            
            if self.respuesta_correcta_texto:
                texto_correcto = FUENTE_NORMAL.render(self.respuesta_correcta_texto, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
                rect_correcto = texto_correcto.get_rect(center=(ANCHO//2, ALTO//2))
                superficie.blit(texto_correcto, rect_correcto)
                
            texto_continuar = FUENTE_PEQUENA.render("Haz clic para continuar", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
            rect_continuar = texto_continuar.get_rect(center=(ANCHO//2, ALTO - 100))
            superficie.blit(texto_continuar, rect_continuar)
        else:
            # Mostrar pregunta actual
            # Pregunta en la parte superior (no tan arriba)
            texto_pregunta = FUENTE_NORMAL.render(self.pregunta_actual.texto, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
            # Ajustar texto si es muy largo
            if texto_pregunta.get_width() > ANCHO - 40:
                # Dividir texto en líneas
                palabras = self.pregunta_actual.texto.split()
                lineas = []
                linea_actual = ""
                for palabra in palabras:
                    prueba = FUENTE_NORMAL.render(linea_actual + " " + palabra if linea_actual else palabra, True, NEGRO)
                    if prueba.get_width() < ANCHO - 40:
                        linea_actual = linea_actual + " " + palabra if linea_actual else palabra
                    else:
                        lineas.append(linea_actual)
                        linea_actual = palabra
                lineas.append(linea_actual)
                
                for i, linea in enumerate(lineas):
                    texto_linea = FUENTE_NORMAL.render(linea, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
                    rect_linea = texto_linea.get_rect(center=(ANCHO//2, ALTO//4 + i * 30))
                    superficie.blit(texto_linea, rect_linea)
            else:
                rect_pregunta = texto_pregunta.get_rect(center=(ANCHO//2, ALTO//4))
                superficie.blit(texto_pregunta, rect_pregunta)
            
            # Contador de preguntas
            texto_contador = FUENTE_PEQUENA.render(f"Pregunta {self.preguntas_respondidas + 1}/15", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
            rect_contador = texto_contador.get_rect(topright=(ANCHO - 20, 20))
            superficie.blit(texto_contador, rect_contador)
            
            # Botones de respuestas
            for boton in self.botones_respuestas:
                if boton.texto:  # Solo dibujar botones con texto
                    boton.dibujar(superficie, self.juego.modo_oscuro)

class PantallaResultados:
    def __init__(self, juego, correctas, incorrectas, puntos):
        self.juego = juego
        self.correctas = correctas
        self.incorrectas = incorrectas
        self.puntos = puntos
        self.boton_reintentar = Boton((ANCHO//2 - 150, ALTO - 100, 140, 40), VERDE_PASTEL, "REINTENTAR", fuente=FUENTE_PEQUENA)
        self.boton_salir = Boton((ANCHO//2 + 10, ALTO - 100, 140, 40), ROJO, "SALIR", fuente=FUENTE_PEQUENA)

    def manejar_eventos(self, eventos):
        pos = pygame.mouse.get_pos()
        self.boton_reintentar.hover = self.boton_reintentar.esta_sobre(pos)
        self.boton_salir.hover = self.boton_salir.esta_sobre(pos)
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.boton_reintentar.esta_sobre(pos):
                    self.juego.iniciar_juego(self.juego.dificultad_actual)
                elif self.boton_salir.esta_sobre(pos):
                    self.juego.cambiar_pantalla("inicio")

    def dibujar(self, superficie):
        superficie.fill(GRIS_CLARO if not self.juego.modo_oscuro else GRIS_OSCURO)
        
        # Titulo
        texto_titulo = FUENTE_SUBTITULO.render("Tus resultados son:", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO//2, ALTO//4))
        superficie.blit(texto_titulo, rect_titulo)
        
        # Estadísticas
        texto_correctas = FUENTE_NORMAL.render(f"Preguntas correctas: {self.correctas}", True, (0, 100, 0))
        texto_incorrectas = FUENTE_NORMAL.render(f"Preguntas incorrectas: {self.incorrectas}", True, (150, 0, 0))
        texto_puntos = FUENTE_NORMAL.render(f"Puntos totales: {self.puntos}", True, (0, 0, 150))
        
        rect_correctas = texto_correctas.get_rect(center=(ANCHO//2, ALTO//2 - 40))
        rect_incorrectas = texto_incorrectas.get_rect(center=(ANCHO//2, ALTO//2))
        rect_puntos = texto_puntos.get_rect(center=(ANCHO//2, ALTO//2 + 40))
        
        superficie.blit(texto_correctas, rect_correctas)
        superficie.blit(texto_incorrectas, rect_incorrectas)
        superficie.blit(texto_puntos, rect_puntos)
        
        # Botones
        self.boton_reintentar.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_salir.dibujar(superficie, self.juego.modo_oscuro)

class PantallaConfiguracion:
    def __init__(self, juego):
        self.juego = juego
        self.boton_modo_oscuro = Boton((ANCHO//2 + 100, ALTO//2 - 50, 80, 40), VERDE_PASTEL if juego.modo_oscuro else ROJO, "ON" if juego.modo_oscuro else "OFF", fuente=FUENTE_PEQUENA)
        self.boton_regresar = Boton((ANCHO - 170, 20, 150, 40), GRIS_CLARO, "X", fuente=FUENTE_SUBTITULO)

    def manejar_eventos(self, eventos):
        pos = pygame.mouse.get_pos()
        self.boton_modo_oscuro.hover = self.boton_modo_oscuro.esta_sobre(pos)
        self.boton_regresar.hover = self.boton_regresar.esta_sobre(pos)
        for e in eventos:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.boton_modo_oscuro.esta_sobre(pos):
                    self.juego.modo_oscuro = not self.juego.modo_oscuro
                    self.boton_modo_oscuro.texto = "ON" if self.juego.modo_oscuro else "OFF"
                    self.boton_modo_oscuro.color = VERDE_PASTEL if self.juego.modo_oscuro else ROJO
                elif self.boton_regresar.esta_sobre(pos):
                    self.juego.cambiar_pantalla("inicio")

    def dibujar(self, superficie):
        superficie.fill(GRIS_CLARO if not self.juego.modo_oscuro else GRIS_OSCURO)
        
        # Barra superior tipo navegador
        pygame.draw.rect(superficie, (200, 200, 200) if not self.juego.modo_oscuro else (80, 80, 80), (0, 0, ANCHO, 60))
        texto_config = FUENTE_NORMAL.render("Configuración", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_config = texto_config.get_rect(center=(ANCHO//2, 30))
        superficie.blit(texto_config, rect_config)
        
        # Botón X para regresar
        self.boton_regresar.dibujar(superficie, self.juego.modo_oscuro)
        
        # Opciones de configuración
        texto_modo_oscuro = FUENTE_NORMAL.render("Modo oscuro:", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_modo_oscuro = texto_modo_oscuro.get_rect(midright=(ANCHO//2 - 10, ALTO//2 - 30))
        superficie.blit(texto_modo_oscuro, rect_modo_oscuro)
        
        self.boton_modo_oscuro.dibujar(superficie, self.juego.modo_oscuro)

# --- JUEGO PRINCIPAL ---

class Juego:
    def __init__(self):
        self.pantalla_actual = "inicio"
        self.modo_oscuro = False
        self.dificultad_actual = None
        self.pantallas = {
            "inicio": PantallaInicio(self),
            "seleccion_dificultad": PantallaSeleccionDificultad(self),
            "configuracion": PantallaConfiguracion(self)
        }
        
    def cambiar_pantalla(self, nueva_pantalla):
        self.pantalla_actual = nueva_pantalla
        if nueva_pantalla == "seleccion_dificultad":
            self.pantallas["seleccion_dificultad"] = PantallaSeleccionDificultad(self)
        elif nueva_pantalla == "configuracion":
            self.pantallas["configuracion"] = PantallaConfiguracion(self)
        elif nueva_pantalla == "inicio":
            self.pantallas["inicio"] = PantallaInicio(self)
            
    def iniciar_juego(self, dificultad):
        self.dificultad_actual = dificultad
        self.pantalla_actual = "juego"
        self.pantallas["juego"] = PantallaJuego(self, dificultad)
        
    def finalizar_juego(self, correctas, incorrectas, puntos):
        self.pantalla_actual = "resultados"
        self.pantallas["resultados"] = PantallaResultados(self, correctas, incorrectas, puntos)
        
    def ejecutar(self):
        corriendo = True
        while corriendo:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    corriendo = False
            
            # Manejar eventos y dibujar la pantalla actual
            if self.pantalla_actual in self.pantallas:
                self.pantallas[self.pantalla_actual].manejar_eventos(eventos)
                self.pantallas[self.pantalla_actual].dibujar(pantalla)
            
            pygame.display.flip()
            reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()

# --- EJECUCIÓN ---
if __name__ == "__main__":
    try:
        juego = Juego()
        juego.ejecutar()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit()

