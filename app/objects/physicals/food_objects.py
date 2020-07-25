from app.game.constants import CharacterTypes
from app.objects.physicals.game_objects import GameObject
from app.objects.physicals.physical_objects import PhysicalObject


class Food(PhysicalObject):
    def __init__(self, *args, tool_belt=None, **kwargs):
        super().__init__(*args,
                         model_name="Misc/trap",
                         model_animation={
                             "stand": "Misc/trap-stand",
                             "walk": "Misc/trap-walk"},
                         damage_taken_model="Misc/playerHit",
                         **kwargs)

        self.character_type = CharacterTypes.FOOD
        self.eaten = False

    def update(self, time_delta, *args, keys=None, **kwargs):
        super().update(time_delta, *args, **kwargs)

        self.actor.setScale(0.001, 0.001, 0.001)

    def remove_object_from_world(self):
        GameObject.remove_object_from_world(self)

    def __str__(self):
        return self.__class__.__name__
