import random

from battleship.board import Board
from battleship.convert import CellConverter

class Player:
    """ Class representing the player
    """
    count = 0  # for keeping track of number of players
    
    def __init__(self, board=None, name=None):
        """ Initialises a new player with its board.

        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
        Player.count += 1
        if name is None:
            self.name = f"Player {self.count}"
        else:
            self.name = name
    
    def __str__(self):
        return self.name
    
    def select_target(self):
        """ Select target coordinates to attack.
        
        Abstract method that should be implemented by any subclasses of Player.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        raise NotImplementedError
    
    def receive_result(self, is_ship_hit, has_ship_sunk):
        """ Receive results of latest attack.
        
        Player receives notification on the outcome of the latest attack by the 
        player, on whether the opponent's ship is hit, and whether it has been 
        sunk. 
        
        This method does not do anything by default, but can be overridden by a 
        subclass to do something useful, for example to record a successful or 
        failed attack.
        
        Returns:
            None
        """
        return None
    
    def has_lost(self):
        """ Check whether player has lost the game.
        
        Returns:
            bool: True if and only if all the ships of the player have sunk.
        """
        return self.board.have_all_ships_sunk()


class ManualPlayer(Player):
    """ A player playing manually via the terminal
    """
    def __init__(self, board, name=None):
        """ Initialise the player with a board and other attributes.
        
        Args:
            board (Board): The player's board. If not provided, then a board
                will be generated automatically
            name (str): Player's name
        """
        super().__init__(board=board, name=name)
        self.converter = CellConverter((board.width, board.height))
        
    def select_target(self):
        """ Read coordinates from user prompt.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        print(f"It is now {self}'s turn.")

        while True:
            try:
                coord_str = input('coordinates target = ')
                x, y = self.converter.from_str(coord_str)
                return x, y
            except ValueError as error:
                print(error)


class RandomPlayer(Player):
    """ A Player that plays at random positions.

    However, it does not play at the positions:
    - that it has previously attacked
    """
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        self.tracker = set()

    def select_target(self):
        """ Generate a random cell that has previously not been attacked.
        
        Also adds cell to the player's tracker.
        
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        target_cell = self.generate_random_target()
        self.tracker.add(target_cell)
        return target_cell

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        
        while has_been_attacked:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.tracker

        return random_cell

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)


class AutomaticPlayer(Player):
    """ Player playing automatically using a strategy."""
    def __init__(self, name=None):
        """ Initialise the player with an automatic board and other attributes.
        
        Args:
            name (str): Player's name
        """
        # Initialise with a board with ships automatically arranged.
        super().__init__(board=Board(), name=name)
        # TODO: Add any other attributes necessary for your strategic player
        self.target_hit_list = [] # List of bools corresponding to hits and misses of previous turns.
        self.target_list = [] # List of previous target cells.
        self.last_hit_sunk = None # Check whether last hit sunk the ship.
        self.search_direction = 0 # Direction the player is searching in.
        self.first_hit = None # Coordinates of first cell hit.
        self.hit_cells = set()

    def is_near_hit_cell(self, cell):
        """ Check whether cell is near a hit cell.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any hit cell. Returns False otherwise.
        """
        is_near = False
        # Loop through hit cells.
        for hit_cell in self.hit_cells:
            is_near = (hit_cell[0]-1 <= cell[0] <= hit_cell[0]+1 
                and hit_cell[1]-1 <= cell[1] <= hit_cell[1]+1)
            if(is_near):
                break
        return is_near

    def get_random_coordinates(self):
        """ Generate random coordinates.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        x = random.randint(1, self.board.width)
        y = random.randint(1, self.board.height)
        return (x, y)

    def generate_random_target(self):
        """ Generate a random cell that has previously not been attacked and isn't near a hit cell.
               
        Returns:
            tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        has_been_attacked = True
        random_cell = None
        is_near_hit = True
        # Keep generating cells until not been attacked or is not near a hit cell.
        while has_been_attacked or is_near_hit:
            random_cell = self.get_random_coordinates()
            has_been_attacked = random_cell in self.target_list
            is_near_hit = self.is_near_hit_cell(random_cell)

        return random_cell

    def receive_result(self, is_ship_hit, has_ship_sunk):
        """
        Update player attributes according to last turn.
        Args:
            - is_ship_hit (bool): Boolean determining whether turn hit.
            - has_ship_sunk (bool): Boolean determining whether turn sunk a ship.
        Returns:
            None
        """
        # Record whether a ship was hit.
        self.target_hit_list.append(is_ship_hit)
        if(is_ship_hit):
            self.hit_cells.add(self.target_list[-1])
        self.last_hit_sunk = has_ship_sunk
        # Save the coordinate if it was the first hit seen.
        if(self.first_hit == None and is_ship_hit):
            self.first_hit = self.target_list[-1]
        # If sunk reset search direction and first hit parameters.
        if(has_ship_sunk):
            self.search_direction = 0
            self.first_hit = None
        
        return None

    def next_target_in_search(self, from_cell):
        """
        Gets the next cell in the search direction.
        Args:
            - from_cell (tuple): coordinates of the cell being seached from.
        Returns:
            - next_target (tuple): next cell in search direction.
        """
        #If next cell isn't valid next_target will stay as None
        next_target = None
        last_target_x = from_cell[0]
        last_target_y = from_cell[1]
        # Move in the search direction and get the cell in that direction, check that new cell is in bounds.
        if(self.search_direction == 0):
            if(last_target_x-1 > 0):
                next_target = (last_target_x-1,last_target_y)
        elif(self.search_direction == 1):
            if(last_target_y+1 < self.board.height+1):
                next_target = (last_target_x,last_target_y+1)
        elif(self.search_direction == 2):
            if(last_target_x+1 < self.board.width+1):
                next_target = (last_target_x+1,last_target_y)
        elif(self.search_direction == 3):
            if(last_target_y-1 > 0):
                next_target = (last_target_x,last_target_y-1)
        # If already tried then set next_target to None,
        if(next_target in self.target_list):
            next_target = None
        return next_target

    def switch_direction(self):
        """
        Flips the search direction.
        Returns: None
        """
        if(self.search_direction == 0):
            self.search_direction = 2
        elif(self.search_direction == 1):
            self.search_direction = 3
        elif(self.search_direction == 2):
            self.search_direction = 0
        elif(self.search_direction == 3):
            self.search_direction = 1
        return None

    def rotate_direction(self):
        """
        Rotates the search direction 90 degrees clockwise
        Returns: None
        """
        if(self.search_direction == 0):
            self.search_direction = 1
        elif(self.search_direction == 1):
            self.search_direction = 2
        elif(self.search_direction == 2):
            self.search_direction = 3
        elif(self.search_direction == 3):
            self.search_direction = 4
        return None

    def next_neighbour(self):
        """
        Finds the next cell to try when searching a hit sequence.
        Returns:
            - next_target (tuple): next cell to try in hit sequence.
        """
        next_target = None
        # If the last turn was a hit then continue in same line.
        if(self.target_hit_list[-1]):
            next_target = self.next_target_in_search(self.target_list[-1])
        # Otherwise try the other end of the hit sequence horizontally.
        if(next_target is None):
            self.switch_direction()
            next_target = self.next_target_in_search(self.first_hit)
            # Otherwise try searching vertically above the first hit cell.
            if(next_target is None):
                self.switch_direction()
                self.rotate_direction()
                next_target = self.next_target_in_search(self.first_hit)
                # Otherwise try searching below the first hit cell.
                if(next_target is None):
                    self.switch_direction()
                    next_target = self.next_target_in_search(self.first_hit)
        return next_target


    def select_target(self):
        """ Select target coordinates to attack.
        
        Returns:
            next_target tuple[int, int] : (x, y) cell coordinates at which to launch the 
                next attack
        """
        # Initialise next_target
        next_target = None
        # Randomly generate if a target hasn't been hit or the last hit sunk the ship.
        # Otherwise search the current hit sequence in the way defined in next_neighbour() function.
        if(self.first_hit is None or self.last_hit_sunk):
            next_target = self.generate_random_target()
        else:
            next_target = self.next_neighbour()
        self.target_list.append(next_target) # Record the next target in list of cells tried.
        return next_target
