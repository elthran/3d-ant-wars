from app.game.constants import WorldPhysics, CharacterTypes
from app.objects.game_models.base import GameObject
from app.objects.game_models.base_physical import PhysicalObject


class CreatureObject(PhysicalObject):
    """A character object. Generally capable of walking, attacking, interacting, responding, etc.

    Attributes:
        attributes (Attributes): All attributes accessible by the character.
        proficiencies (Proficiencies): All proficiencies accessible by the character.
        abilities (Abilities): All abilities accessible by the character.
        walking (bool): If the character is currently walking (mainly used for display).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character_type = CharacterTypes.GENERIC

        self.movement_speed = 3

        # Possible animations to play
        self.walking = False
        # The starting animation (stand plays if no action is set)
        self.actor.loop("stand")
        # If the model is in the process of dying
        self.dying = False
        self.dead = False

    def update(self, time_delta, *args, **kwargs):
        """What gets done after every frame of the game.

        Args:
            time_delta (float): Time since the last frame?
        """
        super().update(time_delta, *args, **kwargs)

        speed = self.velocity.length()
        if speed > self.movement_speed:
            self.velocity.normalize()
            self.velocity *= self.movement_speed
            speed = self.movement_speed

        if not self.walking:
            friction_value = WorldPhysics.FRICTION * time_delta
            if friction_value > speed:
                self.velocity.set(0, 0, 0)
            else:
                friction_vector = -self.velocity
                friction_vector.normalize()
                friction_vector *= friction_value
                self.velocity += friction_vector

        if self.actor is not None:
            self.actor.setFluidPos(self.velocity * time_delta + self.actor.getPos())

    def remove_object_from_world(self):
        GameObject.remove_object_from_world(self)

    def __str__(self):
        return self.__class__.__name__
