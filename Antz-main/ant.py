from tile import *
import random

class Ant:
    # Ant constructor, creates an at at the given coordinates
    # (We'll use the nest coordinates), and they spawn with no food
    def __init__(self, tile):
        self.has_food = False
        self.direction = random.choice(range(0,8))
        self.activated = False
        self.current_tile = tile

    # Ant picks up food and sets has_food to True
    def pick_up_food (self):
        self.has_food = True

    # Ant drops up food and sets has_food to False
    def drop_food (self): 
        self.has_food = False
    
    # Ant leaves the appropriate pheromones depending on whether the ant is looking for food or the colony
    def leave_pheromone(self):
        if self.has_food:
            self.current_tile.set_home_pheromone(self.current_tile.get_home_pheromone() + 4)
        else:
            self.current_tile.set_food_pheromone(self.current_tile.get_food_pheromone() + 4)
    
    # Helper function for ant to move into the given tile and sets its previous tile as unoccupied
    def march(self, tile):

        if not self.current_tile.get_is_colony() and not self.current_tile.get_has_food():
            self.leave_pheromone()
        if not tile.get_is_colony():
            tile.set_is_occupied(True)

        self.current_tile.set_is_occupied(False)
        self.current_tile = tile

    # Change direction of the ant to reflect its current or future movement
    def turn (self, turning_decision):
        # Implement movment but it shoud not move when it is facing an obsticale
        # behavior when in colony
        # 0 i left
        # 1 is forward
        # 2 is right
        # -1 is turn around

        if (turning_decision == 0):
            self.direction -= 1

        elif (turning_decision == 2):
            self.direction += 1
        
        elif (turning_decision == -1):
            self.direction += 4

        elif (turning_decision == -2):
            self.direction += random.choice([-1,1])

        self.direction = self.direction % 8

    # Ant decides which tile it will turn into using the visible tiles' pheromone ranks
    def decide_turning(self, list):
    
        if random.random() <= 0.95:
            max_val = max(list)
            max_indices = [i for i, weight in enumerate(list) if weight == max_val]
            return random.choice(max_indices)
        else:
            return random.choice([i for i, weight in enumerate(list) if weight > 0])
        # return random.choices([0,1,2], weights = list)[0] Alternative method for choosing which tile to move into

    # Ant checks if there's anyting in front of it among the neighboring tiles and moves to a new tile
    def move(self, code, neighboring_tiles):
        # Ant turns around if all tile are occupied or inaccessible
        if (neighboring_tiles == [None, None, None]):
            self.turn(-2)
            return
        else:

            pheromone_list = [0, 0, 0]
            
            # Move into tile the ant is facing if the tile is of the objective the ant is searching for
            for i in [1,0,2]:
                if (neighboring_tiles[i] != None):
                    if (neighboring_tiles[i].get_check_method(code)):
                        self.turn(i)
                        self.march(neighboring_tiles[i])
                        return
                    
                    else:
                        pheromone_list[i] = neighboring_tiles[i].get_pheromone_method(code)
            
            # Semi-randomly move into one of the available tiles based on pheromone level
            turning_direction = self.decide_turning(pheromone_list)
            self.turn(turning_direction)
            self.march(neighboring_tiles[turning_direction])

    
    # Updates the board with new positions of every ant and each tile's pheromone rank each timestep
    def update(self, neighboring_tiles):
        if self.activated:
            if not self.has_food:
                if self.current_tile.get_has_food():
                    self.pick_up_food()
                    self.turn(-1) # turning around
                    return 0
                else:
                    self.move(1, neighboring_tiles)
            else:
                if self.current_tile.get_is_colony():
                    self.drop_food()
                    self.turn(-1) # turning round
                    return 1
                else:
                    self.move(0, neighboring_tiles)
        
        return -1