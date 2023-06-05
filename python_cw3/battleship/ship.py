import random

from battleship.convert import CellConverter

class Ship:
    """ Represent a ship that is placed on the board.
    """
    def __init__(self, start, end, should_validate=True):
        """ Creates a ship given its start and end coordinates on the board. 
        
        The order of the cells do not matter.

        Args:
            start (tuple[int, int]): tuple of 2 positive integers representing
                the starting cell coordinates of the Ship on the board
            end (tuple[int, int]): tuple of 2 positive integers representing
                the ending cell coordinates of the Ship on the board
            should_validate (bool): should the constructor check whether the 
                given coordinates result in a horizontal or vertical ship? 
                Defaults to True.

        Raises:
            ValueError: if should_validate==True and 
                if the ship is neither horizontal nor vertical
        """
        # Start and end (x, y) cell coordinates of the ship
        self.x_start, self.y_start = start
        self.x_end, self.y_end = end

        # make x_start on left and x_end on right
        self.x_start, self.x_end = min(self.x_start, self.x_end), max(self.x_start, self.x_end) 

        # make y_start on top and y_end on bottom 
        self.y_start, self.y_end = min(self.y_start, self.y_end), max(self.y_start, self.y_end)

        if should_validate:
            if not self.is_horizontal() and not self.is_vertical():
                raise ValueError("The given coordinates are invalid. "
                    "The ship needs to be either horizontal or vertical.")

        # Set of all (x,y) cell coordinates that the ship occupies
        self.cells = self.get_cells()
        
        # Set of (x,y) cell coordinates of the ship that have been damaged
        self.damaged_cells = set()
    
    def __len__(self):
        return self.length()
        
    def __repr__(self):
        return (f"Ship(start=({self.x_start},{self.y_start}), "
            f"end=({self.x_end},{self.y_end}))")
        
    def is_vertical(self):
        """ Check whether the ship is vertical.
        
        Returns:
            bool : True if the ship is vertical. False otherwise.
        """
        # Check start and end coordinates have same x value.
        vertical = (self.x_start == self.x_end)

        return vertical
   
    def is_horizontal(self):
        """ Check whether the ship is horizontal.
        
        Returns:
            bool : True if the ship is horizontal. False otherwise.
        """
        # Check start and end coordinates have same y value.
        horizontal = (self.y_start == self.y_end)

        return horizontal
    
    def get_cells(self):
        """ Get the set of all cell coordinates that the ship occupies.
        
        For example, if the start cell is (3, 3) and end cell is (5, 3),
        then the method should return {(3, 3), (4, 3), (5, 3)}.
        
        This method is used in __init__() to initialise self.cells
        
        Returns:
            set[tuple] : Set of (x ,y) coordinates of all cells a ship occupies
        """
        # Loop from start to end coordinate along relevant axis.
        cells = set()
        if(self.is_vertical()):
            for i in range(self.y_start, self.y_end+1):
                cells.add((self.x_start, i))
        else:
            for i in range(self.x_start, self.x_end+1):
                cells.add((i, self.y_start))
        return cells

    def length(self):
        """ Get length of ship (the number of cells the ship occupies).
        
        Returns:
            int : The number of cells the ship occupies
        """
        # Get length of the ship cells.
        return len(self.cells)

    def is_occupying_cell(self, cell):
        """ Check whether the ship is occupying a given cell

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to check

        Returns:
            bool : return True if the given cell is one of the cells occupied 
                by the ship. Otherwise, return False
        """
        occupies = (cell in self.cells)
        return occupies
    
    def receive_damage(self, cell):
        """ Receive attack at given cell. 
        
        If ship occupies the cell, add the cell coordinates to the set of 
        damaged cells. Then return True. 
        
        Otherwise return False.

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the cell coordinates that is damaged

        Returns:
            bool : return True if the ship is occupying cell (ship is hit). 
                Return False otherwise.
        """
        received_damage = False
        if(self.is_occupying_cell(cell)):
            self.damaged_cells.add(cell)
            received_damage = True

        return received_damage
    
    def count_damaged_cells(self):
        """ Count the number of cells that have been damaged.
        
        Returns:
            int : the number of cells that are damaged.
        """
        
        return len(self.damaged_cells)
        
    def has_sunk(self):
        """ Check whether the ship has sunk.
        
        Returns:
            bool : return True if the ship is damaged at all its positions. 
                Otherwise, return False
        """
        sunk = (len(self.damaged_cells) == len(self.cells))
        return sunk
    
    def is_near_ship(self, other_ship):
        """ Check whether a ship is near another ship instance.
        
        Hint: Use the method is_near_cell(...) to complete this method.

        Args:
            other_ship (Ship): another Ship instance against which to compare

        Returns:
            bool : returns True if and only if the coordinate of other_ship is 
                near to this ship. Returns False otherwise.
        """
        # Loop through other ship cells and use is_near_cell method.
        near_ship = False
        for other_ship_cell in other_ship.cells:
            if(not near_ship):
                near_ship = self.is_near_cell(other_ship_cell)
        return near_ship

    def is_near_cell(self, cell):
        """ Check whether the ship is near an (x,y) cell coordinate.

        In the example below:
        - There is a ship of length 3 represented by the letter S.
        - The positions 1, 2, 3 and 4 are near the ship
        - The positions 5 and 6 are NOT near the ship

        --------------------------
        |   |   |   |   | 3 |   |
        -------------------------
        |   | S | S | S | 4 | 5 |
        -------------------------
        | 1 |   | 2 |   |   |   |
        -------------------------
        |   |   | 6 |   |   |   |
        -------------------------

        Args:
            cell (tuple[int, int]): tuple of 2 positive integers representing
                the (x, y) cell coordinates to compare

        Returns:
            bool : returns True if and only if the (x, y) coordinate is at most
                one cell from any part of the ship OR is at the corner of the 
                ship. Returns False otherwise.
        """
        return (self.x_start-1 <= cell[0] <= self.x_end+1 
                and self.y_start-1 <= cell[1] <= self.y_end+1)


class ShipFactory:
    """ Class to create new ships in specific configurations."""
    def __init__(self, board_size=(10,10), ships_per_length=None):
        """ Initialises the ShipFactory class with necessary information.
        
        Args: 
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)
            ships_per_length (dict): A dict with the length of ship as keys and
                the count as values. Defaults to 1 ship each for lengths 1-5.
        """
        self.board_size = board_size
        
        if ships_per_length is None:
            # Default: lengths 1 to 5, one ship each
            self.ships_per_length = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        else:
            self.ships_per_length = ships_per_length

    @classmethod
    def create_ship_from_str(cls, start, end, board_size=(10,10)):
        """ A class method for creating a ship from string based coordinates.
        
        Example usage: ship = ShipFactory.create_ship_from_str("A3", "C3")
        
        Args:
            start (str): starting coordinate of the ship (example: 'A3')
            end (str): ending coordinate of the ship (example: 'C3')
            board_size (tuple[int,int]): the (width, height) of the board in 
                terms of number of cells. Defaults to (10, 10)

        Returns:
            Ship : a Ship instance created from start to end string coordinates
        """
        converter = CellConverter(board_size)
        return Ship(start=converter.from_str(start),
                    end=converter.from_str(end))

    def generate_ships(self):
        """ Generate a list of ships in the appropriate configuration.
        
        The number and length of ships generated must obey the specifications 
        given in self.ships_per_length.
        
        The ships must also not overlap with each other, and must also not be 
        too close to one another (as defined earlier in Ship::is_near_ship())
        
        The coordinates should also be valid given self.board_size
        
        Returns:
            list[Ships] : A list of Ship instances, adhering to the rules above
        """
        ships = []
        # Loop through ship lengths.
        for ship_length in self.ships_per_length.keys():
            # Loop through number of ships per length.
            for ship_num in range(0, self.ships_per_length[ship_length]):
                # Loop until a ship which isn't near other ships is found.
                ship_near = True
                while(ship_near):
                    # Make the ship horizontal or vertical at random.
                    horizontal = random.randint(0,1)
                    # Initialise start and end coordinates.
                    x_start = 0
                    y_start = 0
                    x_end = 0
                    y_end = 0
                    # Set coordinates depending on horizontal or vertical.
                    if(horizontal == 1):
                        x_start = random.randint(1, self.board_size[0])
                        y_start = random.randint(1, self.board_size[1] - ship_length + 1)
                        x_end = x_start
                        y_end = y_start + ship_length - 1
                    else:
                        x_start = random.randint(1, self.board_size[0] - ship_length + 1)
                        y_start = random.randint(1, self.board_size[1])
                        y_end = y_start
                        x_end = x_start + ship_length - 1
                    # Generate ship
                    new_ship = Ship((x_start,y_start),(x_end,y_end))
                    ship_near = False
                    # Check if the ship is near any of the others
                    for other_ship in ships:
                        if(not ship_near):
                            ship_near = new_ship.is_near_ship(other_ship)
                ships.append(new_ship)
        return ships
        
        
if __name__ == '__main__':
    # SANDBOX for you to play and test your methods

    ship = Ship(start=(3, 3), end=(5, 3))
    print(ship.get_cells())
    print(ship.length())
    print(ship.is_horizontal())
    print(ship.is_vertical())
    print(ship.is_near_cell((5, 3)))
    
    print(ship.receive_damage((4, 3)))
    print(ship.receive_damage((10, 3)))
    print(ship.damaged_cells)
    
    ship2 = Ship(start=(4, 1), end=(4, 5))
    print(ship.is_near_ship(ship2))

    # For Task 3
    ships = ShipFactory().generate_ships()
    print(ships)
        
    