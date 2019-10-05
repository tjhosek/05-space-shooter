import sys, logging, os, random, math, arcade, open_color

# Checking Version
version = (3,7)
assert sys.version_info >= version, f"This script requires at least Python {version[0]}.{version[1]}"

# Logging
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Game Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 32
SCREEN_TITLE = "Space Shooter"
GAME_STATE = 0                  # If game state is 0, the game is running, if game state is 1, the player won, if game state is -1, the player lost

# Player Variables
STARTING_LOCATION = (400,100)
CHARACTER_SPEED = 5
HIT_SCORE = 10
KILL_SCORE = 100
CHARACTER_SCALE = 2

# Projectile variables
BULLET_DAMAGE = 10
BULLET_SCALE = 1
BULLET_SPEED = (0,10)

# Enemy variables
ENEMY_SCALE = 2
ENEMY_HP = 100
ENEMY_MOVE_DELAY = 0
NUM_ENEMIES = 20
ENEMY_COL_MAX = 10
ENEMY_SPEED = 1

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        '''
        Initializes the Bullet
        '''
        super().__init__("images/character_sprites/flame0.png",BULLET_SCALE)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the Bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Reticle(arcade.Sprite):
    def __init__(self):
        super().__init__("images/reticle.png")
        (self.center_x, self.center_y) = int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("images/character_sprites/hover.png",CHARACTER_SCALE)
        (self.center_x,self.center_y) =  STARTING_LOCATION
        self.dx = CHARACTER_SPEED
        self.dy = CHARACTER_SPEED
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

    def update(self):
        '''
        updates the position of the player
        '''
        if self.center_x > MARGIN and self.center_x < SCREEN_WIDTH - MARGIN:
            if self.move_left:
                self.center_x -= self.dx
            elif self.move_right:
                self.center_x += self.dx
        else:                                                                   # Making sure that the player does not go past the edge of the screen
            if self.center_x <= MARGIN:
                self.center_x = MARGIN + 1
            elif self.center_x >= SCREEN_WIDTH - MARGIN:
                self.center_x = SCREEN_WIDTH - MARGIN - 1

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("images/enemy.png",ENEMY_SCALE)
        self.hp = ENEMY_HP
        (self.center_x,self.center_y) = position
        (self.dx, self.dy) = 20,-32
        self.fire_delay = random.randint(30,120)

    def update(self):
        '''
        Moves the enemy
        '''
        self.center_x += self.dx
        if self.center_x +MARGIN >= SCREEN_WIDTH or self.center_x < MARGIN:
            self.center_y += self.dy
            self.dx = -self.dx
        

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.sprite_list()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.reticle = Reticle()
        self.score = 0

    def setup(self):
        '''
        Set up enemies
        '''
        row = 1
        column = 1
        # Enemies will be spawned in a space invaders style grid,
        for i in range(NUM_ENEMIES):
            if column > ENEMY_COL_MAX:
                row += 1
                column = 1
            x = column*32*ENEMY_SCALE
            y = SCREEN_HEIGHT - (row*32*ENEMY_SCALE)
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)
            column += 1
        
    def update(self, delta_time):
        global ENEMY_MOVE_DELAY
        self.player.update()
        self.bullet_list.update()
        if ENEMY_MOVE_DELAY <= 0:
            ENEMY_MOVE_DELAY = 30
            self.enemy_list.update()
        else:
            ENEMY_MOVE_DELAY -= 1
        # arcade.draw_text(str(enemy_move_delay),100,200,open_color.white,16)

        for e in self.enemy_list:
            collision = e.collides_with_list(self.bullet_list)
            for i in collision:
                e.hp -= i.damage
                i.kill()
                self.score += HIT_SCORE
            if e.hp <= 0:
                e.kill()
                self.score += KILL_SCORE
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score),20,40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.reticle.draw()
        

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        Moves the aiming reticle with the mouse
        '''
        self.Reticle.center_x = x
        self.Reticle.center_y = y

    def on_mouse_press(self,x,y,button,modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y
            bullet = Bullet((x,y),BULLET_SPEED,BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    def on_key_press(self,key,modifiers):
        if key == arcade.key.A:
            self.player.move_left = not self.player.move_left
        if key == arcade.key.D:
            self.player.move_right = not self.player.move_right
    
    def on_key_release(self,key,modifiers):
        if key == arcade.key.A:
            self.player.move_left = not self.player.move_left
        if key == arcade.key.D:
            self.player.move_right = not self.player.move_right

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
