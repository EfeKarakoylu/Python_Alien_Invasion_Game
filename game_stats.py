class GameStats():
    "Track statistics for Alien Invasion."

    def __init__(self, ai_settings):
        "Initialize statistics"
        self.ai_settings = ai_settings
        self.reset_stats()
        #Start Alien Invasion in an inactive state
        self.game_active = False
        with open('best_score') as fo:

            num = fo.read()
            if num:
                print(num)
                self.high_score = int(num)
            else:
                print('vov')

    def reset_stats(self):
        "Initialize statistics that cabn change during the game"
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1