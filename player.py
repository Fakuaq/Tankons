from shot import Shot
from particle import Particle
from sound_controller import SoundController
import pygame as pg
import math

class Player(pg.sprite.Sprite):
    """
    A class representing a player-controlled tank in the game.

    Attributes:
        - speed (int): The movement speed of the player.
        - rotation_speed (int): The rotation speed of the player.
        - shot_bounces (int): The maximum number of bounces for shots fired by the player.
        - shot_radius (float): The radius of the shots fired by the player.
        - shot_speed (int): The speed of the shots fired by the player.
        - shot_cd (int): The cooldown time between consecutive shots.
        - curr_shot_cd (int): The current remaining cooldown time for shooting.
        - angle (float): The rotation angle of the player's tank.
        - stats_powerups (list): A list of active powerups affecting the player's stats.
        - weapon_powerup (Powerup): The active powerup affecting the player's weapon, if any.

    Methods:
        - __init__(self, identity, score, controls, pos, shots, walls, players, *groups):
            Initializes the Player object with the specified parameters.

        - update(self):
            Updates the position and behavior of the player based on user input and game interactions.

        - kill_player(self):
            Handles the player's death by creating particles, playing sound, and removing the player from the game.

        - get_sprite_color(self):
            Retrieves the color of the player's tank sprite at the center.

        - get_turret_position(self):
            Calculates and returns the position of the player's turret based on the tank's rotation.

        - shoot(self):
            Fires a shot from the player's tank, creating a new Shot object.

        - add_stats_powerup(self, powerup):
            Adds a stat-affecting powerup to the player's active powerups.

        - remove_stats_powerup(self, powerup):
            Removes a stat-affecting powerup from the player's active powerups.
    """
    
    speed = 3
    rotation_speed = 3
    shot_bounces = 3
    shot_radius = 5.5
    shot_speed = 5
    shot_cd = 20
    curr_shot_cd = shot_cd
    angle = 0
    stats_powerups = []
    weapon_powerup = None

    def __init__(self, identity, score, controls, pos, shots, walls, players, *groups):
        """
        Initializes a Player object with the specified parameters.

        Parameters:
            - identity (str): A unique identifier for the player.
            - score (int): The initial score of the player.
            - controls (dict): A dictionary mapping control actions to keycodes for the player.
            - pos (tuple): The initial position of the player's tank (x, y).
            - shots (Group): The group containing all shots in the game.
            - walls (Group): The group containing all walls in the game.
            - players (Group): The group containing all players in the game.
            - *groups: Additional sprite groups to which the player should belong.

        Attributes:
            - score (int): The current score of the player.
            - identity (str): The unique identifier for the player.
            - image (Surface): The image of the player's tank loaded from a file.
            - image_copy (Surface): A copy of the player's tank image.
            - controls (dict): The dictionary mapping control actions to keycodes for the player.
            - rect (Rect): The rectangular area occupied by the player's tank.
            - position (Vector2): The 2D vector representing the position of the player's tank.
            - shots (Group): The group containing all shots in the game.
            - walls (Group): The group containing all walls in the game.
            - player_color (Color): The color of the player's tank sprite at the center.
            - players (Group): The group containing all players in the game.
            - groups (tuple): A tuple containing additional sprite groups to which the player belongs.
        """
        self.score = score
        self.identity = identity
        self.image = pg.image.load(f'assets/tank_{identity}.png').convert_alpha()
        self.image_copy = self.image
        self.controls = controls
        self.rect = self.image.get_rect(center=pos)
        self.position = pg.math.Vector2((self.rect.centerx, self.rect.centery))
        self.shots = shots
        self.walls = walls
        self.player_color = self.get_sprite_color()
        self.players = players
        self.groups = groups

        pg.sprite.Sprite.__init__(self, self.players, *self.groups)

    def update(self):
        keys = pg.key.get_pressed()

        # movement update
        direction = int(keys[self.controls['down']] - keys[self.controls['up']])
        direction_vector = pg.math.Vector2(0, 1).rotate(-self.angle) * direction * self.speed
        self.position += direction_vector
        self.rect.center = int(self.position.x), int(self.position.y)

        # rotate sprite
        rotation = int(keys[self.controls['rotate_left']] - keys[self.controls['rotate_right']])
        rotation = rotation if direction != 1 else rotation * -1 # flip rotation if moving backwards
        if rotation:
            self.angle = self.angle % 360 + rotation * self.rotation_speed
            self.image = pg.transform.rotate(self.image_copy, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        # shoot update
        self.curr_shot_cd -= 1
        if keys[self.controls['shoot']]:
            if self.weapon_powerup:
                self.weapon_powerup.shoot()
            else:
                self.shoot()

        # shot collision        
        if pg.sprite.spritecollideany(self, self.shots):
            shot = pg.sprite.spritecollideany(self, self.shots)
            
            if shot.shot_by is not self or (shot.bounces != 0 and shot.shot_by is self):
                shot.kill()
                self.kill_player()

        # wall collision
        for collided_wall in pg.sprite.spritecollide(self, self.walls, False):
            overlap_top = abs(self.rect.bottom - collided_wall.rect.top)
            overlap_bottom = abs(self.rect.top - collided_wall.rect.bottom)
            overlap_left = abs(self.rect.right - collided_wall.rect.left)
            overlap_right = abs(self.rect.left - collided_wall.rect.right)
        
            smallest_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)
            
            if smallest_overlap == overlap_top:
                self.rect.bottom = collided_wall.rect.top
            elif smallest_overlap == overlap_bottom:
                self.rect.top = collided_wall.rect.bottom
            elif smallest_overlap == overlap_left:
                self.rect.right = collided_wall.rect.left
            elif smallest_overlap == overlap_right:
                self.rect.left = collided_wall.rect.right
            
            self.position.update(self.rect.centerx, self.rect.centery)

        # player collision
        if pg.sprite.spritecollide(self, self.players, False):
            players = pg.sprite.spritecollide(self, self.players, False)
            for player in players:
                if player is not self:
                    self.position -= 1.1 * direction_vector
                    self.rect.center = int(self.position.x), int(self.position.y)
                
        # powerup update
        for powerup in self.stats_powerups.copy():
            powerup.update()
        if self.weapon_powerup:
            self.weapon_powerup.update()

    def kill_player(self):
        """
        Initiates the player's death sequence, creating particles and playing a death sound.

        Parameters:
            None

        Returns:
            None
        """
        particle_count = 50
        particle_speed = 5
        particle_color = self.player_color
        SoundController.death_sound()

        for _ in range(particle_count):
            Particle(self.rect.centerx, self.rect.centery, particle_color, particle_speed, *self.groups)
            
        self.kill()
        
    def get_sprite_color(self):
        """
        Gets the color of the player's tank sprite at the center.

        Parameters:
            None

        Returns:
            Color: The color at the center of the player's tank sprite.
        """
        return self.image.get_at((int(self.rect.width / 2 + 5), int(self.rect.height / 2)))
    
    def get_turret_position(self):
        """
        Calculates the position of the turret relative to the player's tank.

        Parameters:
            None

        Returns:
            tuple: The (x, y) coordinates of the turret position.
        """
        x_turret = self.rect.centerx - (self.rect.height / 2) * math.sin(math.radians(self.angle))
        y_turret = self.rect.centery - (self.rect.height / 2) * math.cos(math.radians(self.angle))

        return int(x_turret), int(y_turret)
    
    def shoot(self):
        """
        Initiates the shooting mechanism of the player, creating a shot and playing a shooting sound.

        Parameters:
            None

        Returns:
            None
        """
        if self.curr_shot_cd > 0: return

        self.curr_shot_cd = self.shot_cd
        turret_position = self.get_turret_position()
       
        direction = pg.math.Vector2(0, 1).rotate(-self.angle + 180)
        Shot(self, turret_position, direction, self.shot_bounces, self.shot_radius, self.shot_speed, self.walls, self.shots, *self.groups)
        SoundController.shoot_sound()

    def add_stats_powerup(self, powerup):
        self.stats_powerups.append(powerup)
        
    def remove_stats_powerup(self, powerup):
        self.stats_powerups.remove(powerup)