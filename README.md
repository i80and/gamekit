GameKit
=======
GameKit is a miniature graphics library for Python with no dependencies.  This
may be useful for getting started with a project quickly with no fuss, or if you
want to deploy onto systems without having to ship dependencies.

Mostly, it's just a test to see how capable Tkinter is out-of-the-box.  The
answer is: not very, but you can fudge it if you're OK with dog-slow performance,
no alpha channel (bitmask transparency is OK), and just using GIF files.

Don't expect tests or real documentation.  The code is very small, at least,
so there isn't much going on.

Documentation
=============
There are a few important classes in GameKit:
  * Point
  * Game
  * Thing
    * Text
    * MovingThing
  * Camera

Game
----
`Game` is the basic entry point for your code.  It has 4 methods that should be
defined in your subclass:
  * `init()` is called after the window is opened and Tk is ready.
    This may be useful for loading sprites and creating entities.
  * `update()` is called at each tick of the mainloop (around every
    16 ms) before the screen is cleared and the redraw phase begins.
  * `draw(camera)` is called after the screen is cleared, and is responsible for
    repopulating the canvas.
  * `input(event)` is called whenever an input event occurs.

Examples
========
See the `examples/` directory for different demonstrations of how to use GameKit.
