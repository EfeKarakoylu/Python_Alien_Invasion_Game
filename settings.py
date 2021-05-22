
class Settings():
    "A class to store all settings for alien invasion"

    def __init__(self):
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        #Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 50
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # Scoring
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        "Initialize settings that change throughout the game."
        self.ship_speed_factor = 1.5
        self.bullet_speed = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1


    def increase_speed(self):
        "Increase speed settings"
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

