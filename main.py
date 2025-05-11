from game import Game
from scanner import Grid
from entities import Player
import math

game = Game()

### game settings ###

game.Slides.update_slides_collection() # check all slides in the presentation
game.Slides.set_level_slide(3) # sets the slide where the level design is placed
game.Slides.set_render_slide(2) #sets the slide where the level design will be rendered

level = Grid(game.Slides.level_slide) # generates a new matrix for the level
level.update_matrix()


player = Player("player-name")
player_x, player_y = 2, 2
fov = math.radians(90)
direction = math.radians(90) # facing down

level.matrix[player_x][player_y] = "p"
level.log_matrix()

hits = game.Render.cast_all_rays(level.matrix, player_x, player_y, direction, fov=fov, num_rays=60)
print(hits)

game.loop = False
while(game.loop):
    #print(game.Slides.get_slides_collection())
    #level.log_matrix()
    """
        # renders the level in the specified render_slide
        game.Render(level.matrix)

        game.PlayerActions(<PlayerClass>) # player keyboard input, PlayerClass is passed so the Player can be moved

        # if something in-game changes the level design:
            level.update_matrix()
    """