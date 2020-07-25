from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class DebugText:
    def __init__(self):
        self.top_right_text = OnscreenText(text="",
                                           scale=0.1,
                                           pos=(0.8, 0.9),
                                           mayChange=True,
                                           align=TextNode.ALeft)

    def update(self, world):
        self.top_right_text.setText(f"""
Ant Count: {len(world.walking_enemies)}
Food Count: {len(world.foods)}
        """)
