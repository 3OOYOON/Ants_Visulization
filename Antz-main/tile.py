import math

class Tile:
    
    def __init__(self, x_coord, y_coord, a_f = math.e, b_f = 5, c_f = -5, a_h = math.e, b_h = 5, c_h = -5,):
        
        self.inital_pheromone = 5
        self.x = x_coord
        self.y = y_coord

        self.home_pheromone = self.inital_pheromone 
        self.food_pheromone = self.inital_pheromone 
        self.has_food = False
        self.is_colony = False
        self.is_occupied = False

        #Decay function variables
        self.a_f = a_f
        self.b_f = b_f
        self.c_f = c_f

        self.a_h = a_h
        self.b_h = b_h
        self.c_h = c_h

    #Set home_pheromone level to a user specified value
    def set_home_pheromone(self, new_pheromone):
        self.home_pheromone = new_pheromone

    #Set food_pheromone level to a user specified value
    def set_food_pheromone(self, new_pheromone):
        self.food_pheromone = new_pheromone

    #Set has_food to a user specified value
    def set_has_food(self, new_state):
        self.has_food = new_state
    
    #Set is_colony to a user specified value
    def set_is_colony(self, new_state):
        self.is_colony = new_state
    
    # Set is_occupied to a user specified value
    def set_is_occupied(self, new_state):
        self.is_occupied = new_state
    
    # Returns home_pheromone level
    def get_home_pheromone(self):
        return self.home_pheromone
    
    # Returns food_pheromone level
    def get_food_pheromone(self):
        return self.food_pheromone

    # Returns has_food
    def get_has_food(self):
        return self.has_food
    
    # Returns is_colony
    def get_is_colony(self):
        return self.is_colony

    # Returns is_occupied
    def get_is_occupied(self):
        return self.is_occupied
    
    # Perform pheromone decay for food pheromone
    def cur_food_pheromone_decay_pace(self):
        if self.food_pheromone == self.inital_pheromone :
            return 0 
        else:
            return ((self.a_f)**(self.food_pheromone-self.c_f))/self.b_f
    
    # Perform pheromone decay for home pheromone
    def cur_home_pheromone_decay_pace(self):
        if self.home_pheromone == self.inital_pheromone :
            return 0 
        else:
            return ((self.a_h)**(self.home_pheromone-self.c_h))/self.b_h

    # Perform tile behavior for a single time instance
    def update(self):
        # self.food_pheromone = max(self.inital_pheromone , self.food_pheromone - self.cur_food_pheromone_dacay_pace())
        # self.home_pheromone = max(self.inital_pheromone , self.home_pheromone - self.cur_home_pheromone_dacay_pace())
        self.food_pheromone = max(self.food_pheromone*0.99, 0.1)
        self.home_pheromone = max(self.home_pheromone*0.99, 0.1)

    # Return tile as a string
    def __str__(self):
        if self.get_has_food():
            return "F"
        elif self.get_is_colony():
            return "C"
        elif self.get_is_occupied():
            return "A"
        else:
            return str(round(self.food_pheromone))

    # Return has_food or is_colony depending on code
    def get_check_method(self, code):
        if code == 1:
            return self.get_has_food()
        return self.get_is_colony()
    
    # Return food_pheremone level or home_pheremone level depending on code
    def get_pheromone_method(self, code):
        if code == 1:
            return self.get_home_pheromone()
        return self.get_food_pheromone()
