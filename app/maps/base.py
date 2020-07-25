from random import choice

from panda3d.core import Vec3, DirectionalLight, AmbientLight, Vec4, CollisionCapsule, CollisionNode

from app.objects.game_models.ant_creature import Ant
from app.objects.game_models.food_base import Food


class World:
    def __init__(self, game):
        self.game = game

        background_music = loader.loadMusic("resources/music/background_theme.ogg")
        background_music.setLoop(True)
        # I find this piece to be pretty loud, so I've turned the volume down a lot.
        background_music.setVolume(0.5)
        background_music.play()

        main_light = DirectionalLight("main light")
        self.main_light_node_path = render.attachNewNode(main_light)
        self.main_light_node_path.setHpr(45, -45, 0)
        render.setLight(self.main_light_node_path)

        ambient_light = AmbientLight("ambient light")
        ambient_light.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambient_light_node_path = render.attachNewNode(ambient_light)
        render.setLight(self.ambient_light_node_path)

        render.setShaderAuto()

        # Load the environment model.
        self.scene = loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.15, 0.15, 0.15)
        self.scene.setPos(10, 60, 0)

        # self.environment = loader.loadModel("Misc/environment")
        # self.environment.reparentTo(render)

        self.walking_enemies = []
        self.deadEnemies = []
        self.foods = []

        # Set up some monster spawn points
        self.spawn_time = 1
        self.spawn_timer = 1
        self.maximum_walking_enemies = 2
        self.spawn_points = []
        number_points_per_wall = 5
        for i in range(number_points_per_wall):
            coord = 7.0 / number_points_per_wall + 0.5
            self.spawn_points.append(Vec3(-7.0, coord, 0))
            self.spawn_points.append(Vec3(7.0, coord, 0))
            self.spawn_points.append(Vec3(coord, -7.0, 0))
            self.spawn_points.append(Vec3(coord, 7.0, 0))

        self.generate_walls()

        self.spawn_food(Vec3(2.0, -7.0, 2.0))
        self.spawn_food(Vec3(3.0, -3.0, 3.0))
        self.spawn_food(Vec3(-5.0, -4.0, 7.0))

    def generate_walls(self):
        wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setY(8.0)

        wallSolid = CollisionCapsule(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setY(-8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setX(8.0)

        wallSolid = CollisionCapsule(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("Wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.show()
        wall.setX(-8.0)

    def spawn_enemy(self):
        spawn_point = choice(self.spawn_points)
        new_enemy = Ant(starting_position=spawn_point)
        self.walking_enemies.append(new_enemy)

    def spawn_food(self, coordinates):
        new_food = Food(starting_position=coordinates)
        self.foods.append(new_food)

    def update(self, time_delta):
        self.spawn_timer -= time_delta
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = self.spawn_time

        [walking_enemy.update(time_delta, hero=self.game.hero) for walking_enemy in self.walking_enemies]

        self.walking_enemies = [enemy for enemy in self.walking_enemies if not enemy.dead]
        self.foods = [food for food in self.foods if not food.eaten]

    def cleanup(self):
        for walking_enemy in self.walking_enemies:
            walking_enemy.remove_object_from_world()
