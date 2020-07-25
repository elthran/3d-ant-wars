from direct.showbase.ShowBase import ShowBase

from app import *
from app.game.commands import ExitMenuCommand
from app.game.constants import States, Graphics
from app.game.states import GameState
from app.game.tool_belt import ToolBelt
from app.maps import World
from app.objects.menus.home import Home
from app.temporary.debug_text import DebugText


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        self.camera.setPos(0, -20, 32)
        self.camera.setP(-60)

        self.key_mapper = KeyMapper.initialize(self)

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()
        self.cTrav.setRespectPrevTransform(True)
        self.pusher.setHorizontal(True)

        self.hero = None
        self.world = None

        self.default_font = loader.loadFont("resources/fonts/Wbxkomik.ttf")

        self.debug_text = DebugText()

        self.current_task = None
        self.state = GameState(States.MENU, game=self)
        self.current_menu = Home(self)
        self.current_menu.enter_menu()

        self.background_task = None

    def resume(self):
        self.current_task = taskMgr.add(self.update, "update")

    def pause(self):
        taskMgr.remove(self.current_task)

    def quit(self):
        self.cleanup()
        base.userExit()

    def start_game(self):
        self.cleanup()
        self.world = World(game=self)

    def update(self, task):
        # Get the amount of time since the last update
        time_delta = min(globalClock.getDt(), Graphics.MAX_FRAME_RATE)

        self.world.update(time_delta=time_delta)

        self.debug_text.update(world=self.world)

        return task.cont

    def cleanup(self):
        if self.world is not None:
            self.world.cleanup()
        if self.hero is not None:
            self.hero.remove_object_from_world()


if __name__ == "__main__":
    game = Game()
    game.run()
