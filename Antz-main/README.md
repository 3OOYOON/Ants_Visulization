# Antz Project Documentation
### Group members:

```
Kai Weiner
Yang Tan
Dylan Smith
Hanane Akeel
Simon Noble
```

## What Is This?

The ANTZ project is a computational model of ant behavior for CS 364. Ants in this model seek out food to bring back to a colony, while leaving pheromones for future ants to follow. Over time, the pheromone levels at each spot in the grid decay. This model assumes the world is a grid and that there is an infinite supply of food.

## Usage
To use the ANTZ program run the following after downloading the code:

```
$ python main.py
```
Additional command line arguments may be added:

* -a Followed by a number will set the number of ants in the simulation. The default is 6 ants.

* -f Followed by a number will set the number of food in the simulation. The default is 3 pieces.

* -d Followed by 2 numbers will set the width and height of the board respectively. The default is 15x15.

* -t Followed by a number will set the number of timesteps the simulation runs for. The default is 100000 timesteps.

* -v Sets the animation option to *True* meaning that the simulation will be animated rather than merely producing the final maps and graphs of food collection.

NOTE: The visulization may not work on all devices due to differences in the speed at which tabs open and close. This is mainly for testing purposes! Be prepared to ctrl + c between frames.

For example, this simulation that will use 3 ants, 1 piece of food, a 10x10 board, and run for 500000 steps:

```
$ python main.py -a 3 -f 1 -d 10 10 -t 500000
```

## Main.py
This file takes in ant.py and tile.py to help initialize the board the ants move in.
 - there is a tuple helper called **tuple_add** function
 - the **Board** is initialized as a class which:
    * places the colony onto the board
    * the width and height of the board
    * the number of ants and food
    * and the directions the ant can turn _**(not move)**_
 - the functions **add_colony** and **add_food** add the colony and food to the board
 - the functions **get_food_locs** and **get_valid_food_locations** help add food to the board
    * **get_valid_food_locations** helps to make sure food spawns in the board but not in the radius of the ant colony
 - the function **get_center_location** gets the location of the center of the board
 - **get_neighboring_tiles** helps the ant know what valid neighboring tiles it could turn towards
 - there is a helper function called **is_facing_empty** for **get_neighboring_tiles** helps make sure the potential tiles that the ant can turn to are not occupied
 - the string function **__str__** helps represent the board through underscores ( __ )
 - **initialize_board** initializes the board
 - **add_ants** helps to add ants to the board through **initialize_board**
 - **simulate** handles the timesteps
 - **update** helps update the location and rotation of the ants
 - **activate_ants** helps release the ants so they aren't all unable to move due to the tile in front of them being occupied by other ants
 - **set_activated_per_timestep** helps activate the ants bit by bit
 - **visualization** handles the visualization of the board by:
    * using a heat map for food and home pheromones
    * putting ant png's on the board based on where the ants are supposed to be on
    * placing the colony on the board visually


## Tile.py
This file handles the information of each tile on the board.
Tiles remember:
- food and home pheromone
- the rate of decay for those pheromones
- whether a tile is occupied
- whether a tile is part of a colony or where the food is
- updating that information through time steps
- and representing the board through strings with:
    * A = ants
    * C = colony
    * F = food


## Ant.py
This file takes in tile.py to help with the ants' movement.
Ant.py works by:
- initializing the class **Ant** where most of the functions for ant resides
- there is the list **list_of_directions** which lists out the directions the ant can turn
- **\_\_init\_\_** initializes the ant with:
    * not having any food at the start
    * its direction facing forward
    * the ant not being launched out of the colony into the board
    * the current tile the ant is on
    * the direction options the ant can rotate
- **pick_up_food** makes it so that ants having food is true
- **drop_food** makes it so that ants having food is false
- **leave_pheromone** lets an ant leave a home or food pheromone on the tile depending on whether or not the ant has food
- **march** lets an ant leave a pheromone if the ant is occupying a tile
- **turn** uses math to help the ant to turn based on its current rotation
- **decide_turning** makes the ant turn randomly in cases where the ant is on the edge of the board
- **move** lets the ant move on the board using functions turn and march
- **update** updates whether the ant has food or not and drops the food into the colony

## Results

The ants learn paths to food and back and are able to (at times) become efficient in their food grabbing process. Unfortunately, the ants unlearn these strategies as quickly as they learn them, often getting distracted by another's ants random wandering around the grid. We use matplotlib to plot the results of our model, and it shows this: there are ebbs and flows in the ants' success over time.

## Next Steps

There's a lot more that can be done here. While we did a lot of manual tuning of parameters to maximize ant success, it could be worthwhile using techniques from ML or Statistics to optimize our hyperparameters (pheromones left per timstep, pheromone decay rate, ant turning strategy, etc.).

Additionally, we could add new features to the model to add realism. For instance, there could be obstacles which find themselves between ants and their food source, or multiple anthills.

Lastly, several parts of our code have been written with multiple techniques in mind so that we could play around with these hyperparameters. We have kept in some alternate methods as a means of documentation. Later, one technique shold be picked.