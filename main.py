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

COLOR_RESPUESTAS = [
    (255, 165, 0),   # naranja
    (65, 105, 225),  # royal blue
    (255, 105, 180), # hot pink
    (60, 179, 113)   # medium sea green
]

PUNTOS = {
    "facil": 2,
    "normal": 5,
    "dificil": 10,
    "muy dificil": 15
}

FUENTE_TITULO = pygame.font.SysFont("arial", 48)
FUENTE_SUBTITULO = pygame.font.SysFont("arial", 36)
FUENTE_NORMAL = pygame.font.SysFont("arial", 24)
FUENTE_PEQUENA = pygame.font.SysFont("arial", 20)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Knight Mind")
reloj = pygame.time.Clock()

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
            if self.color in COLOR_RESPUESTAS:
                color_actual = self.color
            else:
                color_actual = tuple(min(255, c + 80) for c in self.color)
        if self.hover:
            color_actual = tuple(min(255, c + 40) for c in color_actual)
        pygame.draw.rect(superficie, color_actual, self.rect, border_radius=8)
        texto_render = self.fuente.render(self.texto, True, self.texto_color if not modo_oscuro else GRIS_OSCURO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, texto_rect)

    def esta_sobre(self, pos):
        return self.rect.collidepoint(pos)

class Pregunta:
    def __init__(self, texto, opciones, correcta, dificultad, tipo):
        self.texto = texto
        self.opciones = opciones
        self.correcta = correcta
        self.dificultad = dificultad
        self.tipo = tipo

# --- PREGUNTAS ---
preguntas_facil = [
    Pregunta("El sol es un planeta.", ["Verdadero", "Falso"], 1, "facil", "vf"),
    Pregunta("¿Cuál es el color del cielo en un día despejado?", ["Morado", "Verde", "Rojo", "Azul"], 3, "facil", "multiple"),
    Pregunta("El agua hierve a 100 grados Celsius.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Cuántos días tiene una semana?", ["5", "10", "7", "12"], 2, "facil", "multiple"),
    Pregunta("La Tierra es plana.", ["Verdadero", "Falso"], 1, "facil", "vf"),
    Pregunta("¿Cuál es el animal que dice 'miau'?", ["Perro", "Gato", "Pájaro", "Vaca"], 1, "facil", "multiple"),
    Pregunta("El hielo es agua congelada.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Qué planeta es conocido como el planeta rojo?", ["Venus", "Marte", "Júpiter", "Saturno"], 1, "facil", "multiple"),
    Pregunta("Los humanos tienen cinco sentidos.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Cuál es la capital de España?", ["Sevilla", "Barcelona", "Madrid", "Valencia"], 2, "facil", "multiple"),
    Pregunta("El fuego es frío.", ["Verdadero", "Falso"], 1, "facil", "vf"),
    Pregunta("¿Qué instrumento tiene teclas y se toca con las manos?", ["Guitarra", "Piano", "Batería", "Flauta Francesa del siglo IX"], 1, "facil", "multiple"),
    Pregunta("El aire es invisible.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Cuántos colores tiene el arcoíris?", ["5", "6", "9", "7"], 3, "facil", "multiple"),
    Pregunta("Los peces pueden respirar fuera del agua.", ["Verdadero", "Falso"], 1, "facil", "vf"),
    Pregunta("¿Qué fruta es amarilla y curva?", ["Manzana", "Banana", "Pera", "Sandía"], 1, "facil", "multiple"),
    Pregunta("El hielo flota en el agua.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Cuál es el número después del 9?", ["7", "8", "10", "11"], 2, "facil", "multiple"),
    Pregunta("Los gatos son herbíboros.", ["Verdadero", "Falso"], 1, "facil", "vf"),
    Pregunta("¿Cuál es el continente más grande?", ["Asia", "África", "Europa", "Antártida"], 0, "facil", "multiple"),
    Pregunta("El chocolate se hace con cacao.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Cuál es el océano más grande del mundo?", ["Atlántico", "Índico", "Ártico", "Pacífico"], 3, "facil", "multiple"),
    Pregunta("Las plantas producen oxígeno.", ["Verdadero", "Falso"], 0, "facil", "vf"),
    Pregunta("¿Qué animal es conocido como el rey de la selva?", ["Tigre", "León", "Elefante", "Cebra"], 1, "facil", "multiple"),
    Pregunta("El hielo es más denso que el agua.", ["Verdadero", "Falso"], 1, "facil", "vf"),
    Pregunta("¿Cuál es el metal más ligero?", ["Hierro", "Aluminio", "Litio", "Cobre"], 2, "facil", "multiple"),
]

preguntas_normal = [
    Pregunta("La capital de Francia es París.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Cuál es el símbolo químico del oro?", ["Pb", "Ag", "Fe", "Au"], 3, "normal", "multiple"),
    Pregunta("El cuerpo humano tiene 206 huesos.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Quién escribió 'El Principito'?", ["William Shakespeare", "Gabriel García Márquez", "Antoine de Saint-Exupéry", "Stephen king"], 2, "normal", "multiple"),
    Pregunta("La luz viaja más rápido que el sonido.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Cuál es el río más largo del mundo?", ["Nilo", "Amazonas", "Yangtsé", "Misisipi"], 1, "normal", "multiple"),
    Pregunta("El planeta Júpiter es el más grande del sistema solar.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿En qué año llegó el hombre a la Luna?", ["1965", "1832", "1972", "1969"], 3, "normal", "multiple"),
    Pregunta("El ADN está presente en todas las células vivas.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Cuál es la moneda oficial de Japón?", ["Dólar", "Won", "Yen", "Euro"], 2, "normal", "multiple"),
    Pregunta("La Gran Muralla China es visible desde el espacio.", ["Verdadero", "Falso"], 1, "normal", "vf"),
    Pregunta("¿Quién pintó 'La última cena'?", ["Vicente van Gogh", "Miguel Ángel", "Pablo Picasso", "Leonardo da Vinci"], 3, "normal", "multiple"),
    Pregunta("El oxígeno es necesario para la combustión.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Cuál es el idioma más hablado en el mundo?", ["Inglés", "Mandarín", "Español", "Hindi"], 1, "normal", "multiple"),
    Pregunta("La electricidad se mide en amperios.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Cuál es el país más grande del mundo?", ["China", "Afghanistan", "Estados Unidos", "Rusia"], 3, "normal", "multiple"),
    Pregunta("La penicilina fue el primer antibiótico descubierto.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Quién es conocido como el padre de la teoría de la evolución?", ["Isaac Newton", "Nikola Tesla", "Charles Darwin", "Galileo Galilei"], 2, "normal", "multiple"),
    Pregunta("El Monte Everest es la montaña más alta del mundo.", ["Verdadero", "Falso"], 0, "normal", "vf"),
    Pregunta("¿Cuál es el elemento más abundante en la corteza terrestre?", ["Hierro", "Oxígeno", "Silicio", "Aluminio"], 1, "normal", "multiple"),
    Pregunta("la luz es un elemento quimico.", ["Verdadero", "Falso"], 1, "normal", "vf"),
    Pregunta("¿Donde se encuentra el Coliseo Romano?", ["Atenas", "Roma", "Estambul", "Cartago"], 1, "normal", "multiple"),
]

preguntas_dificil = [
    Pregunta("La teoría de la relatividad fue propuesta por Albert Einstein.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Cuál es la fórmula química del ácido sulfúrico?", ["C2H4O2", "H2SO4", "NaOH", "CO2"], 1, "dificil", "multiple"),
    Pregunta("La capital de Mongolia es Londres.", ["Verdadero", "Falso"], 1, "dificil", "vf"),
    Pregunta("¿Quién es el autor de 'Cien años de soledad'?", ["Rafael Pombo", "Mario Vargas Llosa", "Julio Cortázar", "Gabriel García Márquez"], 3, "dificil", "multiple"),
    Pregunta("El bosón de Higgs fue descubierto en 2012.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Cuál es el elemento con número atómico 26?", ["Zinc", "Cobre", "Hierro", "Plomo"], 2, "dificil", "multiple"),
    Pregunta("La penicilina fue descubierta por Alexander Fleming.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Qué país tiene la mayor cantidad de islas?", ["Suecia", "Indonesia", "Filipinas", "Canadá"], 0, "dificil", "multiple"),
    Pregunta("La fotosíntesis ocurre en las mitocondrias.", ["Verdadero", "Falso"], 1, "dificil", "vf"),
    Pregunta("¿Cuál es la capital de Kazajistán?", ["Bishtek", "Tashkent", "Astana", "Dushanbe"], 2, "dificil", "multiple"),
    Pregunta("El número pi es un número irracional.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Quién compuso la Novena Sinfonía?", ["Beethoven", "Mozart", "Bach", "Chopin"], 0, "dificil", "multiple"),
    Pregunta("La velocidad de la luz es aproximadamente 300,000 km/s.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Cuándo cayó el Imperio romano de Occidente?", ["382 d.C.", "744 a.C.", "23 d.C", "476 d.C."], 3, "dificil", "multiple"),
    Pregunta("La teoría cuántica explica el comportamiento de partículas subatómicas.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Qué país tiene la mayor población mundial?", ["Estados Unidos", "India", "China", "Indonesia"], 2, "dificil", "multiple"),
    Pregunta("El helio es más ligero que el aire.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Quién escribió 'La Odisea'?", ["Sófocles", "Avicebron", "Platón", "Homero"], 3, "dificil", "multiple"),
    Pregunta("El ADN tiene una estructura de doble hélice.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Cual es la capital de Nueva Zelanda?", ["Auckland", "Wellington", "Christchurch", "Hamilton"], 1, "dificil", "multiple"),
    Pregunta("La teoría de la relatividad especial se aplica a objetos en movimiento a velocidades cercanas a la luz.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
    Pregunta("¿Quien es conocido como el padre de la química moderna?", ["Dmitri Mendeléyev", "Antoine Lavoisier", "John Dalton", "Marie Curie"], 1, "dificil", "multiple"),
    Pregunta("La ecuación E=mc^2 relaciona la energía con la masa y la velocidad de la luz.", ["Verdadero", "Falso"], 0, "dificil", "vf"),
]

preguntas_muy_dificil = [
    Pregunta("¿En qué año se firmó el Tratado de Westfalia?", ["1813", "1618", "1648", "1789"], 2, "muy dificil", "multiple"),
    Pregunta("La constante de Planck tiene unidades de acción.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("¿Quién desarrolló la teoría del psicoanálisis?", ["Albert Einstein", "Carl Jung", "Alfred Adler", "Sigmund Freud"], 3, "muy dificil", "multiple"),
    Pregunta("Alaska es el estado americano más pequeño en kilómetros cuadrados.", ["Verdadero", "Falso"], 1, "muy dificil", "vf"),
    Pregunta("¿Cuál es la capital de Bután?", ["Thimphu", "Katmandú", "Dhaka", "Lhasa"], 0, "muy dificil", "multiple"),
    Pregunta("La mecánica clásica explica el comportamiento de las neuronas.", ["Verdadero", "Falso"], 1, "muy dificil", "vf"),
    Pregunta("¿Quién escribió 'El Capital'?", ["Stephen King", "Friedrich Engels", "Karl Max", "Adam Smith"], 2, "muy dificil", "multiple"),
    Pregunta("La entropía mide el desorden en un sistema.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("¿Cuál es el símbolo químico del tungsteno?", ["Wt", "Tu", "Tg", "W"], 3, "muy dificil", "multiple"),
    Pregunta("La paradoja de Schrödinger es un experimento mental en arquitectura.", ["Verdadero", "Falso"], 1, "muy dificil", "vf"),
    Pregunta("¿En qué año comenzó la Revolución Francesa?", ["1901", "1789", "1804", "1812"], 1, "muy dificil", "multiple"),
    Pregunta("La teoría de cuerdas intenta unificar la gravedad y la mecánica cuántica.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("¿Quién pintó 'El jardín de las delicias'?", ["El bosco", "Hieronymus Bosch", "Pieter Bruegel", "Caravaggio"], 1, "muy dificil", "multiple"),
    Pregunta("La fotosíntesis produce H2O como subproducto.", ["Verdadero", "Falso"], 1, "muy dificil", "vf"),
    Pregunta("¿Cuál es la capital de Liechtenstein?", ["Ginebra", "Zúrich", "Berna", "Vaduz"], 3, "muy dificil", "multiple"),
    Pregunta("La ecuación de Schrödinger pertenece a la física cuántica.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("¿Quién es conocido como el padre de la genética?", ["Charles Darwin", "Gregor Mendel", "Louis Pasteur", "James Watson"], 1, "muy dificil", "multiple"),
    Pregunta("El teorema de Gödel establece límites en los sistemas formales.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("¿Cuál es el país más pequeño del mundo?", ["Mónaco", "Nauru", "San Marino", "Ciudad del Vaticano"], 3, "muy dificil", "multiple"),
    Pregunta("La teoría de la relatividad general fue publicada en 1915.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("El bosón de Higgs es responsable de la masa de las partículas fundamentales.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("¿Quién escribió 'La Divina Comedia'?", ["Albert Einstin", "Geoffrey Chaucer", "John Milton", "Dante Alighieri"], 3, "muy dificil", "multiple"),
    Pregunta("El grafeno es una forma de carbono con propiedades únicas.", ["Verdadero", "Falso"], 0, "muy dificil", "vf"),
    Pregunta("La mecánica cuántica fue desarrollada en el siglo XIX.", ["Verdadero", "Falso"], 1, "muy dificil", "vf"),
    Pregunta("¿Cuál es el metal más pesado?", ["Uranio", "Plomo", "Osmio", "Mercurio"], 2, "muy dificil", "multiple"),
]

# --- CREAR LISTA DE PREGUNTAS PARA LA PARTIDA ---
def crear_lista_preguntas(dificultad, num_preguntas=15):
    todas = []
    if dificultad == "facil":
        todas = preguntas_facil + preguntas_normal
    elif dificultad == "normal":
        todas = preguntas_normal + preguntas_facil
    elif dificultad == "dificil":
        todas = preguntas_dificil + preguntas_normal + preguntas_muy_dificil
    else:
        todas = preguntas_muy_dificil + preguntas_dificil

    seleccion = random.sample(todas, k=min(num_preguntas, len(todas)))

    preguntas_partida = []
    for pregunta in seleccion:
        opciones = pregunta.opciones[:]
        indices = list(range(len(opciones)))
        combinados = list(zip(opciones, indices))
        random.shuffle(combinados)
        opciones_mezcladas, indices_mezclados = zip(*combinados)
        correcta_nuevo_indice = indices_mezclados.index(pregunta.correcta)
        preguntas_partida.append(Pregunta(
            pregunta.texto,
            list(opciones_mezcladas),
            correcta_nuevo_indice,
            pregunta.dificultad,
            pregunta.tipo
        ))
    return preguntas_partida

# --- CLASES DE PANTALLAS ---
class PantallaInicio:
    def __init__(self, juego):
        self.juego = juego
        self.titulo = "Knight Mind"
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
        texto_titulo = FUENTE_TITULO.render(self.titulo, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO//2, ALTO//4))
        superficie.blit(texto_titulo, rect_titulo)
        self.boton_jugar.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_config.dibujar(superficie, self.juego.modo_oscuro)

class PantallaSeleccionDificultad:
    def __init__(self, juego):
        self.juego = juego
        self.titulo = "Selecciona la dificultad"
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
        texto_titulo = FUENTE_SUBTITULO.render(self.titulo, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO//2, ALTO//4))
        superficie.blit(texto_titulo, rect_titulo)
        self.boton_facil.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_normal.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_dificil.dibujar(superficie, self.juego.modo_oscuro)
        self.boton_regresar.dibujar(superficie, self.juego.modo_oscuro)

class PantallaJuego:
    def __init__(self, juego, dificultad):
        self.juego = juego
        self.dificultad = dificultad
        self.preguntas_partida = crear_lista_preguntas(dificultad)
        self.pregunta_idx = 0
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
        if self.preguntas_respondidas >= len(self.preguntas_partida):
            self.juego.finalizar_juego(self.preguntas_correctas, self.preguntas_respondidas - self.preguntas_correctas, self.puntos_totales)
            return
        self.pregunta_actual = self.preguntas_partida[self.pregunta_idx]
        self.pregunta_idx += 1
        self.botones_respuestas = []

        if self.pregunta_actual.tipo == "vf":
            self.botones_respuestas.append(Boton((ANCHO//2 - 150, ALTO//2 + 30, 300, 50), COLOR_RESPUESTAS[0], self.pregunta_actual.opciones[0]))
            self.botones_respuestas.append(Boton((ANCHO//2 - 150, ALTO//2 + 100, 300, 50), COLOR_RESPUESTAS[1], self.pregunta_actual.opciones[1]))
        else:
            self.botones_respuestas.append(Boton((ANCHO//2 - 320, ALTO//2 + 30, 300, 50), COLOR_RESPUESTAS[0], self.pregunta_actual.opciones[0]))
            self.botones_respuestas.append(Boton((ANCHO//2 + 20, ALTO//2 + 30, 300, 50), COLOR_RESPUESTAS[1], self.pregunta_actual.opciones[1]))
            self.botones_respuestas.append(Boton((ANCHO//2 - 320, ALTO//2 + 100, 300, 50), COLOR_RESPUESTAS[2], self.pregunta_actual.opciones[2]))
            self.botones_respuestas.append(Boton((ANCHO//2 + 20, ALTO//2 + 100, 300, 50), COLOR_RESPUESTAS[3], self.pregunta_actual.opciones[3]))

        self.mostrar_resultado = False

    def manejar_eventos(self, eventos):
        if self.mostrar_resultado:
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
            texto_pregunta = FUENTE_NORMAL.render(self.pregunta_actual.texto, True, NEGRO if not self.juego.modo_oscuro else BLANCO)
            if texto_pregunta.get_width() > ANCHO - 40:
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

            texto_contador = FUENTE_PEQUENA.render(f"Pregunta {self.preguntas_respondidas + 1}/15", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
            rect_contador = texto_contador.get_rect(topright=(ANCHO - 20, 20))
            superficie.blit(texto_contador, rect_contador)

            for boton in self.botones_respuestas:
                if boton.texto:
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

        texto_titulo = FUENTE_SUBTITULO.render("Tus resultados son:", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_titulo = texto_titulo.get_rect(center=(ANCHO//2, ALTO//4))
        superficie.blit(texto_titulo, rect_titulo)

        texto_correctas = FUENTE_NORMAL.render(f"Preguntas correctas: {self.correctas}", True, (0, 100, 0))
        texto_incorrectas = FUENTE_NORMAL.render(f"Preguntas incorrectas: {self.incorrectas}", True, (150, 0, 0))
        texto_puntos = FUENTE_NORMAL.render(f"Puntos totales: {self.puntos}", True, (0, 0, 150))

        rect_correctas = texto_correctas.get_rect(center=(ANCHO//2, ALTO//2 - 40))
        rect_incorrectas = texto_incorrectas.get_rect(center=(ANCHO//2, ALTO//2))
        rect_puntos = texto_puntos.get_rect(center=(ANCHO//2, ALTO//2 + 40))

        superficie.blit(texto_correctas, rect_correctas)
        superficie.blit(texto_incorrectas, rect_incorrectas)
        superficie.blit(texto_puntos, rect_puntos)

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
        pygame.draw.rect(superficie, (200, 200, 200) if not self.juego.modo_oscuro else (80, 80, 80), (0, 0, ANCHO, 60))
        texto_config = FUENTE_NORMAL.render("Configuración", True, NEGRO if not self.juego.modo_oscuro else BLANCO)
        rect_config = texto_config.get_rect(center=(ANCHO//2, 30))
        superficie.blit(texto_config, rect_config)
        self.boton_regresar.dibujar(superficie, self.juego.modo_oscuro)
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