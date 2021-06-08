from vpython import *


class Turtle3D:
    '''
    L'objecte Turtle3D permet fer dibuixos a l'espai 3D

    Args:
        No cal cap argument, crea instancia amb Turtle3D()

    Attributes:
        color_pintar (vector): conte el valor del color a pintar, amb valors de 0 a 1;
        pintar (boolean): valor per saber si en moure's la tortuga ha de pintar;
        direccio (vector): direccio cap on s'ha de moure;
        alpha (float): angle respecte el pla ZY, serveix per calcular la direccio;
        beta (float): angle respecte el pla ZX, serveix per calcular la direccio;
        radi (float): radi del cilindre que pinta;
        posicio (vector): posicio de la tortuga.
    '''

    def __init__(self) -> None:
        scene.height = scene.width = 1000
        scene.autocenter = True
        scene.caption = """\n
        To rotate "camera", drag with right button or Ctrl-drag.\n
        To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\n
          On a two-button mouse, middle is left + right.\n
        To pan left/right and up/down, Shift-drag.\n
        Touch screen: pinch/extend to zo<om, swipe or two-finger rotate.\n"""

        self.color_pintar = vector(1, 0, 0)
        self.pintar = True
        self.direccio = vector(1, 0, 0)
        self.alpha = pi/2
        self.beta = 0
        self.radi = 0.1
        self.posicio = vector(0, 0, 0)
        super().__init__()

    def forward(self, times):
        '''La tortuga es mou endevant (cap on apunta el seu vector direccio)

        Args:
            times (float): El nombre d'unitats que es mou endevant

        '''
        if self.pintar:
            sphere(pos=self.posicio, radius=self.radi, color=self.color_pintar)
            cil = cylinder(pos=self.posicio, axis=self.direccio *
                           times, radius=self.radi, color=self.color_pintar)
            self.posicio += self.direccio*times
            sphere(pos=self.posicio, radius=self.radi, color=self.color_pintar)
        else:
            self.posicio += self.direccio*times

    def backward(self, times):
        '''La tortuga es mou enrere (en relacio al seu vector direccio)

        Args:
            times (float): El nombre d'unitats que es mou enrere

        '''
        if self.pintar:
            sphere(pos=self.posicio, radius=self.radi, color=self.color_pintar)
            cil = cylinder(pos=self.posicio, axis=-self.direccio *
                           times, radius=self.radi, color=self.color_pintar)
            self.posicio -= self.direccio*times
            sphere(pos=self.posicio, radius=self.radi, color=self.color_pintar)
        else:
            self.posicio -= self.direccio*times

    def right(self, angleGraus):
        '''La tortuga canvia el seu vector de direccio en angleGraus cap a la dreta

        Args:
            angleGraus (float): Graus de gir en radians

        '''
        self.alpha -= angleGraus*(pi/180)

        x = sin(self.alpha)*cos(self.beta)
        y = sin(self.beta)
        z = cos(self.alpha)*cos(self.beta)

        self.direccio = vector(x, y, z)

    def left(self, angleGraus):
        '''La tortuga canvia el seu vector de direccio en angleGraus cap a l'esquerra

        Args:
            angleGraus (float): Graus de gir en radians

        '''
        self.alpha += angleGraus*(pi/180)

        x = sin(self.alpha)*cos(self.beta)
        y = sin(self.beta)
        z = cos(self.alpha)*cos(self.beta)

        self.direccio = vector(x, y, z)

    def up(self, angleGraus):
        '''La tortuga canvia el seu vector de direccio en angleGraus cap a dalt

        Args:
            angleGraus (float): Graus de gir en radians

        '''
        self.beta += angleGraus*(pi/180)

        x = sin(self.alpha)*cos(self.beta)
        y = sin(self.beta)
        z = cos(self.alpha)*cos(self.beta)

        self.direccio = vector(x, y, z)

    def down(self, angleGraus):
        '''La tortuga canvia el seu vector de direccio en angleGraus cap a baix

        Args:
            angleGraus (float): Graus de gir en radians

        '''
        self.beta -= angleGraus*(pi/180)

        x = sin(self.alpha)*cos(self.beta)
        y = sin(self.beta)
        z = cos(self.alpha)*cos(self.beta)

        self.direccio = vector(x, y, z)

    def color(self, r, g, b):
        '''La tortuga canvia el seu color per el proporcionat

        Args:
            r (float): Component r del color
            g (float): Component g del color
            b (float): Component b del color

        '''
        self.color_pintar = vector(r, g, b)

    def hide(self):
        '''La tortuga deixa de pintar mentre es mou

        '''
        self.pintar = False

    def show(self):
        '''La tortuga pinta mentre es mou

        '''
        self.pintar = True

    def home(self):
        '''La tortuga es desplaça a la posicio inicial (0,0,0), sense canviar la seva direccio

        '''
        self.posicio = vector(0, 0, 0)
