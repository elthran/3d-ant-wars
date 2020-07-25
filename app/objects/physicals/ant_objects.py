from random import randint

from panda3d.core import LPoint3f

from app.game.constants import CharacterTypes
from app.objects.physicals.game_objects import GameObject
from app.objects.physicals.creature_objects import CreatureObject


class Ant(CreatureObject):
    def __init__(self, *args, tool_belt=None, **kwargs):
        super().__init__(*args,
                         model_name="panda-model",
                         model_animation={"stand": "panda-walk4",
                                          "walk": "panda-walk4"},
                         damage_taken_model="Misc/playerHit",
                         **kwargs)

        self.character_type = CharacterTypes.ANT
        self.actor.getChild(0).setH(180)
        self.destination = self.get_new_destination()

    def get_new_destination(self):
        return [randint(-8, 8), randint(-8, 8), randint(-8, 8)]

    def update(self, time_delta, *args, keys=None, **kwargs):
        super().update(time_delta, *args, **kwargs)

        self.run_logic(time_delta)

        # self.actor.setScale(0.0009, 0.0009, 0.0009)
        self.actor.setScale(0.001, 0.001, 0.001)

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

