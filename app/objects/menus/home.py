from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.gui.OnscreenImage import OnscreenImage

from .base import *


class Home(Menu):
    def __init__(self, *args):
        super().__init__(*args)

        self.backdrop = DirectFrame(frameColor=(0, 0, 0, 1),
                                    frameSize=(-1, 1, -1, 1),
                                    parent=render2d)

        self.menu = DirectFrame(frameColor=(1, 1, 1, 0))

        title = [
            DirectLabel(text="3D Ant Wars",
                        scale=0.1,
                        pos=(0, 0, 0.7),
                        parent=self.menu,
                        relief=None,
                        text_font=self.default_font,
                        text_fg=(1, 1, 1, 1))
        ]

        buttons = [
            Button(menu=self,
                   text="Start Game",
                   command=self.initialize_game,
                   parent=self.menu,
                   pos=(0, 0, 0.2)),
            Button(menu=self,
                   text="Quit",
                   command=self.exit_game,
                   parent=self.menu,
                   pos=(0, 0, -0.2))
        ]

        self.hide_menu()
