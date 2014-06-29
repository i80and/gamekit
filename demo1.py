#!/usr/bin/env python3
"""A small demonstration of GameKit.  Displays patrolling skeletons.  More skeletons may be
   spawned by clicking.  The screen can be panned with the arrow keys."""


import gamekit
import random


class Skeleton(gamekit.MovingThing):
    def __init__(self, sprite, initial_position):
        gamekit.MovingThing.__init__(self, sprite)
        self.position = initial_position
        self.dir = 1
        self.patrol = (min(0, self.position.x), max(600, self.position.x))

    def update(self):
        x, y = self.position

        if x > self.patrol[1] or x <= self.patrol[0]:
            self.dir *= -1
            self.face(self.facing * -1)

        self.move((1*self.dir, 0))


class Game(gamekit.Game):
    def __init__(self):
        gamekit.Game.__init__(self)
        self.i = 0
        self.dir = 1

    def init(self):
        self.skeleton_sprite = gamekit.Sprite('resources/skeleton.gif', 2)
        self.skeletons = []
        for i in range(8):
            spawn_point = gamekit.Point(random.randint(1, 600), i*self.skeleton_sprite.height)
            self.skeletons.append(Skeleton(self.skeleton_sprite, spawn_point))
        self.text = gamekit.Text('A test', gamekit.Point(0, 0), fill='white')

    def update(self):
        for skeleton in self.skeletons:
            skeleton.update()

    def draw(self, camera):
        self.text.draw(camera)
        for skeleton in self.skeletons:
            skeleton.draw(camera)

    def input(self, event):
        if isinstance(event, gamekit.MouseEvent):
            self.skeletons.append(Skeleton(self.skeleton_sprite, event.world_position))
        elif isinstance(event, gamekit.KeyEvent):
            vec = gamekit.Point(0.0, 0.0)
            if(event.keycode == gamekit.KEY_UP):
                vec = vec.translate(gamekit.Point(0.0, 10.0))
            elif event.keycode == gamekit.KEY_RIGHT:
                vec = vec.translate(gamekit.Point(-10.0, 0.0))
            elif event.keycode == gamekit.KEY_DOWN:
                vec = vec.translate(gamekit.Point(0.0, -10.0))
            elif event.keycode == gamekit.KEY_LEFT:
                vec = vec.translate(gamekit.Point(10.0, 0.0))

            self.camera.position = self.camera.position.translate(vec)

if __name__ == '__main__':
    g = Game()
    g.start('A game')
