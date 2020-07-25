from random import randint

from panda3d.core import LPoint3f, Vec4

from app.game.constants import CharacterTypes, Masks
from app.objects.game_models.base import GameObject
from app.objects.game_models.creature_base import CreatureObject


class Ant(CreatureObject):
    def __init__(self, *args, tool_belt=None, **kwargs):
        super().__init__(*args,
                         model_name="PandaChan/act_p3d_chan",
                         model_animation={"stand": "PandaChan/a_p3d_chan_idle",
                                          "walk": "PandaChan/a_p3d_chan_run"},
                         damage_taken_model="Misc/playerHit",
                         **kwargs)

        self.character_type = CharacterTypes.ANT
        self.actor.setScale(0.5, 0.5, 0.5)
        self.actor.setColor(Vec4(1, 0, 0, 1))
        self.actor.getChild(0).setH(180)
        self.destination = self.get_new_destination()
        self.collider.node().setFromCollideMask(Masks.OTHER)
        self.collider.node().setIntoCollideMask(Masks.OTHER)

    def get_new_destination(self):
        return [randint(-8, 8), randint(-8, 8), randint(-8, 8)]

    def update(self, time_delta, *args, keys=None, **kwargs):
        super().update(time_delta, *args, **kwargs)

        self.run_logic(time_delta)

        # This can be improved. If the character is walking go through the two possibilites (was standing/ was walking)
        # Else set them to loop stand.
        # Should just be.... self.update_current_animation()
        if self.walking:
            stand_control = self.actor.getAnimControl("stand")
            if stand_control.isPlaying():
                stand_control.stop()
            walk_control = self.actor.getAnimControl("walk")
            if not walk_control.isPlaying():
                self.actor.loop("walk")
        else:
            stand_control = self.actor.getAnimControl("stand")
            if not stand_control.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")

        # Check if damage_taken_model can be refreshed
        if self.damage_taken_model and self.damage_taken_model_timer > 0:
            self.damage_taken_model_timer -= time_delta
            self.damage_taken_model.setScale(2.0 - self.damage_taken_model_timer / self.damage_taken_model_duration)
            if self.damage_taken_model_timer <= 0:
                self.damage_taken_model.hide()

    def run_logic(self, time_delta):
        vectorToPlayer = LPoint3f(self.destination[0], self.destination[1], self.destination[2]) - self.actor.getPos()
        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()
        vectorToPlayer2D.normalize()
        heading = self.y_vector.signedAngleDeg(vectorToPlayer2D)
        self.walking = True
        vectorToPlayer.setZ(0)
        vectorToPlayer.normalize()
        self.velocity += vectorToPlayer * self.movement_speed * time_delta
        self.actor.setH(heading)
        if distanceToPlayer < 1:
            self.destination = self.get_new_destination()

    def remove_object_from_world(self):
        GameObject.remove_object_from_world(self)

    def __str__(self):
        return self.__class__.__name__

