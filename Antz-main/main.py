from ant import *
from tile import *
import numpy as np
import math, random, argparse
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
import matplotlib.colors as mcolors

def tuple_add(tup_1, tup_2):
    """Helper functions that adds together two tuples of size 2."""
    return (tup_1[0] + tup_2[0], tup_1[1] + tup_2[1])

class Board:
    """
    The board represents the 2D grid which the ants, colony, and food operate on. Has methods
    which control the general simulation flow, from visualization to the update function.
    """
    def __init__(self, width = 15, height = 20, spawn_radius = 1, num_ants = 2, num_food = 1, colony_x = None, colony_y = None):
        self.width = width
        self.height = height
        self.spawn_radius = spawn_radius
        self.num_ants = num_ants
        self.num_food = num_food
        self.grid = np.ndarray((self.height, self.width), dtype=Tile)
        self.ants = np.ndarray((num_ants), dtype=Ant)
        self.colony = (colony_y, colony_x)
        self.t = 0

        self.num_activated = 0
        self.activated_per_timestep = 2

        self.directions = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)] #[(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

        self.ant_food_collection_data = []
        self.ant_food_deposit_data = []

        self.initialize_board()

    def initialize_board(self):
        """
        Initializes a board with a colony, food, and ants.
        """
        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x] = Tile(x,y)
        self.add_colony()
        self.add_food()
        self.add_ants()

    def add_colony(self):
        """Adds a colony to the board"""
        if self.colony == (None, None):
            self.colony = self.get_center_location(self.width, self.height)
        elif self.colony[0] == None or self.colony[1] == None:
            raise Exception("You must specify both an x and a y (or neither).")
        self.grid[self.colony].is_colony = True

    def add_food(self):
        """Adds food to the board, if possible"""
        all_locations = self.get_valid_food_locations()
        if self.spawn_radius > max(self.width, self.height):
            raise Exception("The exclusion radius is too large for food to be placed.")
        elif len(all_locations) < self.num_food:
            raise Exception("There are not enough locations to place food.")
        food_locations = random.sample(list(all_locations), self.num_food)
        for loc in food_locations:
            x = loc % self.width
            y = loc // self.width
            # set tile to be a food source
            self.grid[y][x].set_has_food(True)

    def add_ants(self):
        """Adds ants to the board."""
        self.ants = [Ant(self.grid[self.colony]) for i in range(self.num_ants)]

    def get_valid_food_locations(self):
        """
        Helper function for add_food.

        Food can only be placed within the grid and cannot be placed within a certain X by X
        square surrounding the colony. Thus, this function returns a set of all possible
        locations food could spawn in. 
        """
        all_locations = set(range(self.width * self.height))
        for y in range(max(self.colony[0] - self.spawn_radius, 0), min(self.colony[0] + self.spawn_radius + 1, self.height - 1)):
            for x in range(max(self.colony[1] - self.spawn_radius, 0), min(self.colony[1] + self.spawn_radius + 1, self.width - 1)):
                location = x + y * self.width
                all_locations.remove(location)
        return all_locations

    def get_center_location(self, width, height):
        """
        Helper function for add_colony, in case a colony X and Y is not specified.

        Gets the center location on the grid
        """
        return (math.floor(height / 2), math.floor(width / 2))

    def get_food_locs(self):
        """Returns a list of tuples representing the location of each food"""
        food = []
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[j][i].get_has_food():
                    food.append((j,i))
        return food
    
     # Return an array of the unoccupied neighboring tiles at the current direction
    def get_neighboring_tiles(self, loc, direction):
        """
        Returns a list of the 3 tiles an ant faces when at location 'loc' with direction 'direction'.
        If a location is invalid, None is passed instead of a Tile object.

        Written by Yang
        """
        neighboring_tiles = [None, None, None]
        if self.is_location_empty(tuple_add(loc, self.directions[direction - 1])):
            neighboring_tiles[0] = self.grid[tuple_add(loc, self.directions[direction - 1])]
        if self.is_location_empty(tuple_add(loc, self.directions[direction])):
             neighboring_tiles[1] = self.grid[tuple_add(loc, self.directions[direction])]
        if self.is_location_empty(tuple_add(loc, self.directions[(direction + 1) % 8])):
            neighboring_tiles[2] = self.grid[tuple_add(loc, self.directions[(direction + 1) % 8])]
         
        return neighboring_tiles
    
    def is_location_empty(self, loc):
        """
        Confirms a tile at a specific location exists and is not occupied by an ant
        """
        return (0 <= loc[0] < self.height) and (0 <= loc[1] < self.width) and (not self.grid[loc].get_is_occupied())

    def get_home_pheromone_grid(self):
        """Computes a 2D grid of home pheromone levels."""
        home_pheromone = np.vectorize(lambda x: x.get_home_pheromone())(self.grid)
        return home_pheromone
                
    def get_food_pheromone_grid(self):
        """Computes a 2D grid of food pheromone levels."""
        food_pheromone = np.vectorize(lambda x: x.get_food_pheromone())(self.grid)
        return food_pheromone

    def __str__(self):
        """The board represented as a string. Useful alternative to matplotlib"""
        representation = " _" * self.width + "\n"
        for y in range(self.height):
            representation += "|"
            for x in range(self.width):
                representation += str(self.grid[y][x]) + " "
            representation = representation[:-1]
            representation += "|\n"
        representation += (" _" * self.width)
        return representation

    def activate_ants(self):
        """
        Helper function to the update function.
        Activates activated_per_timestep ants each timestep so they can start moving.
        """
        for i in range(self.activated_per_timestep): 
            if self.num_activated < self.num_ants:
                self.ants[self.num_activated].activated = True
                self.num_activated += 1
                
    def set_activated_per_timestep(self, new_activated_per_timestep):
        """Setter function for _activated_per_timestep"""
        self.activated_per_timestep = new_activated_per_timestep

    def update(self):
        """
        Update function.

        For each timestep:
        1. activates ants which have not started moving
        2. calls the update function of each ant (rotating, moving)
        3. calls the update function of each tile (pheromone decay)
        """
        # 1. Activation
        if self.num_activated < self.num_ants:
            self.activate_ants()
        # 2. Ant Update
        for ant in self.ants:
            ant_location = (ant.current_tile.y, ant.current_tile.x)
            neighboring_tiles = self.get_neighboring_tiles(ant_location, ant.direction)
            food_code = ant.update(neighboring_tiles)
            # aside (data collection)
            if (food_code == 0):
                self.ant_food_collection_data.append([self.t, ant_location])
            elif (food_code == 1):
                self.ant_food_deposit_data.append([self.t, ant_location])
        # 3. Tile Update
        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x].update()

    def simulate(self, time = 100, animate = False):
        """
        Runs the update function for a certain amount of timesteps. If animate,
        then at each update a matplotlib plot will display to the screen with a status.
        """
        for t in range(time):
            self.t += 1
            self.update()
            if animate:
                self.visualization(animate)

    def visualization(self, animate = False):
        """
        Using matplotlib, plots the ants, food, pheromone levels on the screen.

        If animate=True, will continuously create new matplotlib plots to show ant movement. This is
        bare-bones animation and is primarily for testing to investigate ant behavior.

        Based on Tom Finzell's code
        """

        # images
        ants = [f"./images/ant{i}.png" for i in range(8)]
        bread = "./images/bread.png" #https://www.dreamstime.com/stock-illustration-flat-design-single-bread-slice-icon-vector-illustration-image79060025
        anthill = "./images/anthill.png" #https://www.dreamstime.com/stock-illustration-flat-design-single-bread-slice-icon-vector-illustration-image79060025

        ant_list = self.ants
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

        ant_imgs = [plt.imread(ant) for ant in ants]
        bread_img = plt.imread(bread)
        anthill_img = plt.imread(anthill)
        
        zoom_val = 0.12  # Zoom dictates how big the images should appear on the screen
                         # All images are 200 x 200 so 

        cmap1 = mcolors.LinearSegmentedColormap.from_list("red_map", ["white", "red"])
        cmap2 = mcolors.LinearSegmentedColormap.from_list("blue_map", ["white", "blue"])

        # pheromone heatmaps
        sns.heatmap(self.get_food_pheromone_grid(), ax=ax1, cmap=cmap1, cbar=True)
        ax1.set_title('Food Pheromone')
        sns.heatmap(self.get_home_pheromone_grid(), ax=ax2, cmap=cmap2, cbar=True)
        ax2.set_title('Home Pheromone')

        # plotting the ants at the correct with possible food in hand
        bread_imagebox = OffsetImage(bread_img, zoom=zoom_val / 2) 
        for ant in ant_list:
            x_ant_image_coord = ant.current_tile.x + 0.5
            y_ant_image_coord = ant.current_tile.y + 0.5
            imagebox = OffsetImage(ant_imgs[ant.direction], zoom=zoom_val)
            ab = AnnotationBbox(imagebox, (x_ant_image_coord, y_ant_image_coord), frameon=False)
            ax1.add_artist(ab)
            ab = AnnotationBbox(imagebox, (x_ant_image_coord, y_ant_image_coord), frameon=False)
            ax2.add_artist(ab)
            if ant.has_food:
                food_in_hand = AnnotationBbox(bread_imagebox, (x_ant_image_coord + 0.2, y_ant_image_coord - 0.2), frameon=False)
                ax1.add_artist(food_in_hand)
                food_in_hand = AnnotationBbox(bread_imagebox, (x_ant_image_coord + 0.2, y_ant_image_coord - 0.2), frameon=False)
                ax2.add_artist(food_in_hand)

        # plotting the food
        food_locs = board.get_food_locs()
        for food in food_locs:
            bread_imagebox = OffsetImage(bread_img, zoom=zoom_val) 
            ab = AnnotationBbox(bread_imagebox, (food[1] + 0.5, food[0] + 0.5), frameon=False)
            ax1.add_artist(ab)
            ab = AnnotationBbox(bread_imagebox, (food[1] + 0.5, food[0] + 0.5), frameon=False)
            ax2.add_artist(ab)

        # plotting the anthill
        anthill_imagebox = OffsetImage(anthill_img, zoom=zoom_val) 
        ab = AnnotationBbox(anthill_imagebox, (board.colony[1] + 0.5, board.colony[0] + 0.5), frameon=False)
        ax1.add_artist(ab)
        ab = AnnotationBbox(anthill_imagebox, (board.colony[1] + 0.5, board.colony[0] + 0.5), frameon=False)
        ax2.add_artist(ab)

        # if animating, the display only shows for 0.15 seconds
        if animate:
            plt.show(block=False)
            plt.pause(0.15)
            plt.close()
        else:
            plt.show()

    def plot_food_collection_data(self):
        """At each timestep, plots the number of food collected"""
        food_time_data = np.zeros(self.t)

        for time in self.ant_food_collection_data:
            food_time_data[time[0]] += 1
        
        plt.plot(food_time_data, marker='o',linestyle='')
        plt.xlabel("Time instance")
        plt.ylabel("Amount of food collected")
        plt.title("Amount of food collected over time")
        plt.show()

    def plot_food_deposit_data(self):
        """At each timestep, plots the number of food deposited at the colony"""
        food_time_data = np.zeros(self.t)
        
        for time in self.ant_food_deposit_data:
            food_time_data[time[0]] += 1
        
        plt.plot(food_time_data, marker='o',linestyle='')
        plt.xlabel("Time instance")
        plt.ylabel("Amount of food deposited")
        plt.title("Amount of food deposited over time")
        plt.show()

    def hist_food_deposit_data(self):
        """Cleaner histogram for displaying food deposit information"""
        food_timestamps = [food[0] for food in self.ant_food_deposit_data]
        plt.hist(food_timestamps, bins=20)
        plt.xlabel("Time instance")
        plt.ylabel("Amount of food deposited")
        plt.title("Amount of food deposited over time")        
        plt.show()

    def hist_food_collection_data(self):
        """Cleaner histogram for displaying food collection information"""
        food_timestamps = [food[0] for food in self.ant_food_collection_data]
        plt.hist(food_timestamps, bins=20)
        plt.xlabel("Time instance")
        plt.ylabel("Amount of food collected")
        plt.title("Amount of food collected over time")        
        plt.show()


if __name__ == "__main__":
    """
    Uses argparse to allow the user to input information about the grid.
    """
    # parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--ants", type=int, help="number of ants", default = 6)
    parser.add_argument("-f", "--food", type=int, help="number of food", default = 3)
    parser.add_argument("-d", "--dimensions", type=int, help="first argument width of grid, second argument height of grid", nargs = 2, default=[15, 15])
    parser.add_argument("-t", "--timesteps", type=int, help="timesteps to run simulation for", default = 100000)
    parser.add_argument("-v", "--visualize", help="shows animation of ants moving around the grid", action="store_true")
    args = parser.parse_args()

    # simulate
    board = Board(num_ants = args.ants, num_food = args.food, spawn_radius = 4, width = args.dimensions[0], height = args.dimensions[1])
    board.simulate(args.timesteps, args.visualize)

    # post-simulation visualizations
    board.visualization()
    board.hist_food_deposit_data()
    board.hist_food_collection_data()
