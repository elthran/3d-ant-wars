from panda3d.core import Vec4

from app.game.constants import CharacterTypes, Masks
from app.objects.game_models.base import GameObject
from app.objects.game_models.base_physical import PhysicalObject


class Food(PhysicalObject):
    def __init__(self, *args, tool_belt=None, **kwargs):
        super().__init__(*args,
                         model_name="PandaChan/act_p3d_chan",
                         model_animation={"stand": "PandaChan/a_p3d_chan_idle",
                                          "walk": "PandaChan/a_p3d_chan_run"},
                         damage_taken_model="Misc/playerHit",
                         **kwargs)

        self.character_type = CharacterTypes.FOOD
        self.actor.setScale(0.5, 0.5, 0.5)
        self.actor.setColor(Vec4(0.1, 1.0, 0.2, 1))
        self.collider.node().setFromCollideMask(Masks.OTHER)
        self.collider.node().setIntoCollideMask(Masks.OTHER)
        self.eaten = False

    def update(self, time_delta, *args, keys=None, **kwargs):
        super().update(time_delta, *args, **kwargs)

    def remove_object_from_world(self):
        GameObject.remove_object_from_world(self)

    def __str__(self):
        return self.__class__.__name__
