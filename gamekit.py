#!/usr/bin/env python3

import collections
import tkinter

# Keycode definitions
KEY_BACKSPACE = 22
KEY_ENTER   = 36
KEY_UP      = 111
KEY_LEFT    = 113
KEY_RIGHT   = 114
KEY_DOWN    = 116

Point = collections.namedtuple('Point', ('x', 'y'))
Point.translate = lambda self, x, y=None: Point(self.x + x, self.y + y) \
    if y is not None else \
    Point(self.x + x.x, self.y + x.y)
Point.__neg__ = lambda self: Point(-self.x, -self.y)


class Sprite:
    """An image that may be displayed by a Thing."""
    def __init__(self, path, scale=1):
        """Create a new sprite, along with a scale to be displayed with."""
        image = tkinter.PhotoImage(file=path)
        self.__image = image.zoom(scale, scale)
        self.__flipped_image = self._flip(self.image)

    @property
    def image(self):
        """Return the internal tkinter image."""
        return self.__image

    @property
    def flipped_image(self):
        """Return a precomputed horizontally-flipped copy of the internal tkinter image."""
        return self.__flipped_image

    @property
    def width(self):
        """Return the width of the scaled image."""
        return self.image.width()

    @property
    def height(self):
        """Return the height of the scaled image."""
        return self.image.height()

    @classmethod
    def _flip(klass, orig):
        """Return a horizontally-flipped copy of this image."""
        image = tkinter.PhotoImage(width=orig.width(), height=orig.height())

        for y in range(0, orig.height()):
            for x in range(0, orig.width()):
                # If this pixel is transparent in the source, skip it.
                if not orig.tk.call(orig.name, 'transparency', 'get', x, y):
                    image.put("#%02x%02x%02x" % orig.get(x, y), (orig.width()-x, y))

        return image


class Thing:
    """Base class for all entities that may contain behavior."""
    def draw(self, camera):
        """Draw this thing onto the given camera."""
        pass

    def update(self):
        """Update the state of this thing for the current game tick."""
        pass


class Text(Thing):
    """A Thing that displays text on screen."""
    def __init__(self, text, position, **kwargs):
        self.text = text
        self.position = position
        self.kwargs = kwargs

    def draw(self, camera):
        pos = self.position.translate(camera.position)
        camera.canvas.create_text(pos, text=self.text, **self.kwargs)


class MovingThing(Thing):
    """Represents some useful entity in the game world."""
    def __init__(self, sprite):
        self.__position = Point(0.0, 0.0)
        self.facing = 1
        self.sprite = sprite
        self.state = None

    @property
    def position(self):
        """Get this entity's position in the world."""
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    def move(self, vec):
        """Convenience method for moving this entity."""
        x1, y1 = self.position
        x2, y2 = vec
        self.position = Point(x1+x2, y1+y2)

    def face(self, direction):
        """Change the direction that this "thing" is facing."""
        if direction not in (-1, 1):
            raise ValueError('Direction must be either -1 or 1: {0}', direction)

        self.facing = direction

    def update(self):
        pass

    def draw(self, camera):
        src = self.sprite.image
        if self.facing == -1:
            src = self.sprite.flipped_image

        camera.canvas.create_image(self.position.translate(camera.position.x, camera.position.y), anchor=tkinter.NW, image=src)


class MouseEvent:
    def __init__(self, world_position, screen_position, button):
        self.world_position = world_position
        self.screen_position = screen_position
        self.button = button


class KeyEvent:
    def __init__(self, ch, keycode):
        self.char = ch
        self.keycode = keycode


class Camera:
    def __init__(self, canvas):
        self.position = Point(0, 0)
        self.canvas = canvas


class Game:
    """Base class for fundamental game behavior."""
    def __init__(self):
        pass

    def init(self):
        pass

    def update(self):
        pass

    def draw(self, camera):
        pass

    def input(self, event):
        pass

    def start(self, title, width=800, height=600):
        """Start the game with the given title and size."""
        window = tkinter.Tk()
        window.wm_title(title)
        canvas = tkinter.Canvas(window, bg='black', width=width, height=height)
        canvas.focus_set()
        canvas.pack()

        self.camera = Camera(canvas)

        # Center the dang window
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws/2) - (width/2)
        y = (hs/2) - (height/2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        def make_click_callback(button):
            def helper(ev):
                p = Point(ev.x, ev.y)
                self.input(MouseEvent(
                    p.translate(-self.camera.position),
                    p,
                    button))

            return helper

        # Set up event handlers
        canvas.bind('<Button-1>', make_click_callback(1))
        canvas.bind('<Button-2>', make_click_callback(2))
        canvas.bind('<Button-3>', make_click_callback(3))
        canvas.bind('<Key>', lambda ev: self.input(KeyEvent(ev.char, ev.keycode)))

        # Release the kraken!
        self.init()

        def mainloop():
            self.update()
            canvas.delete(tkinter.ALL)
            self.draw(self.camera)
            window.after(16, mainloop)

        mainloop()
        window.mainloop()
