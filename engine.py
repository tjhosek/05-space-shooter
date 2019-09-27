import arcade, random, os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Space Shooter"

MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    '''Main Application Class'''

    def __init__(self, width, height, title):
        '''Initializer'''

        super().__init__(width, height, title)

        filePath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(filePath)

        self.playerList = None
        self.enemyList = None
        self.projectileList = None

        self.score = 0
        self.player = None

    def setup(self):
        self.playerList = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.projectileList = arcade.SpriteList()

        self.score = 0
        self.player = arcade.Sprite()

        characterScale = 1
        flameScale = 1
        self.player.hoverTextures = []
        self.player.hoverTextures.append(arcade.load_texture("images/character_sprites/hover.png", scale = characterScale))

        self.player.flyRightTextures = []
        self.player.flyRightTextures.append(arcade.load_texture("images/character_sprites/tilt.png", scale=characterScale))

        self.player.flyLeftTextures = []
        self.player.flyLeftTextures.append(arcade.load_texture("images/character_sprites/tilt.png", scale=characterScale, mirrored=True))

        self.player.flameTextures = []
        self.player.flameTextures.append(arcade.load_texture("images/character_sprites/flame0.png", scale=flameScale))
        self.player.flameTextures.append(arcade.load_texture("images/character_sprites/flame1.png", scale=flameScale))

        self.player.texture_change_distance = 20

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_x = SCREEN_HEIGHT - 10
        self.player.scale = 1

        self.playerList.append(self.player)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        '''renders the screen'''

        arcade.start_render()

        self.enemyList.draw()
        self.playerList.draw()
        self.projectileList.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        '''Called whenever a key is pressed'''

        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        '''Called when the user releases a key'''
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 90

    def update(self, delta_time):
        '''Movement and Game Logic'''

        self.playerList.update()
        self.playerList.update_animation()
        self.enemyList.update()
        self.enemyList.update_animation()
        self.projectileList.update()
        self.projectileList.update_animation()

        hitList = arcade.check_for_collision_with_list(self.player, self.enemyList)


def main():
    '''main method'''
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()