import random

symbols = {
    "origin": "☺",
    "flag": "▹",
    "snake": "S",
    "hidden": "∘",
    "numbers": ["∙", "➀", "➁", "➂", "➃", "➄", "➅", "➆", "➇"]
}

adjacencies = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

def spacer(current_number, max_number):
    """
    Creates a string with an appropriate length of spaces based on the length of key numbers.
    Used for keeping spacing consistent when rending the board.
    """
    spacer = " "*(1 + len(str(max_number))-len(str(current_number)))
    return spacer

def tile_spacer(max_number):
    """Simpler spacer for spacing tiles. Uses a fixed amount"""
    spacer = " "*len(str(max_number))
    return spacer

def error_message(first):
    if first == True:
        print("Coords not found. Check your formatting?! Example: '1,2'")
    else:
        print("Coords not found. Check your formatting?! Example: 'p 1,2'")

class Board():
    """Represents the board containing the tiles"""
    def __init__(self, rows, columns, snakes):
        self.rows = rows
        self.columns = columns
        self.snakes = snakes
        self.lose = False

    def build_tiles(self):
        """Initializes a dictionary of all the tiles on the board with default values"""
        self.tiles_dict = {}
        for row in range(1, self.rows+1):
            for col in range(1, self.columns+1):
                self.tiles_dict[(row, col)] = {
                    "coords": f"{row},{col}",
                    "flag": False,
                    "exposed": False,
                    "snake": False,
                    "number": 0,
                    }
        self.tiles_list = list(self.tiles_dict.keys())
        self.unexposed = self.tiles_list[:]
                
    def set_snakes(self, starting_tile):
        """
        Sets a selection of the tiles to be snakes.
        Retries until the starting tile is not a snake.
        """
        temp_tiles_list = self.tiles_list[:]
        temp_tiles_list.remove(starting_tile)
        self.unexposed.remove(starting_tile)
        for adjacent in adjacencies:
            tile = ((starting_tile[0]+adjacent[0]), (starting_tile[1]+adjacent[1]))
            if tile in self.tiles_list:
                temp_tiles_list.remove(tile)
                self.unexposed.remove(tile)
        snake_tiles = random.sample(temp_tiles_list, k=self.snakes)
        for tile in snake_tiles:
            self.tiles_dict[tile]["snake"] = True
            self.unexposed.remove(tile)
        self.snake_tiles = snake_tiles

    def set_numbers(self):
        """
        Only use after snakes have been set.
        Adds 1 to the number of every tile surrounding every snake.
        """
        for snake_tile in self.snake_tiles:
            for adjacent in adjacencies:
                tile = ((snake_tile[0]+adjacent[0]), (snake_tile[1]+adjacent[1]))
                if tile in self.tiles_list:
                    self.tiles_dict[tile]["number"] += 1

    def reveal_tile(self, coords):
        """
        Only use if coords is not a snake.
        Reveals selected tile, and reveals surroundings.
        Chains the revealing of 0-tiles to save time.
        """
        to_reveal_surroundings = [coords]
        self.tiles_dict[coords]["exposed"] = True
        try:
            self.unexposed.remove(coords)
        except ValueError:
            pass
        while to_reveal_surroundings:
            center_tile = to_reveal_surroundings.pop()
            if self.tiles_dict[coords]["number"] == 0:
                for adjacent in adjacencies:
                    tile = ((center_tile[0]+adjacent[0]), (center_tile[1]+adjacent[1]))
                    if tile in self.tiles_list:
                        if self.tiles_dict[tile]["exposed"] is False:
                            if self.tiles_dict[tile]["snake"] is False:
                                self.tiles_dict[tile]["exposed"] = True
                                try:
                                    self.unexposed.remove(tile)
                                except ValueError:
                                    pass
                                if self.tiles_dict[tile]["number"] == 0:
                                    to_reveal_surroundings.append(tile)

    def reveal_board(self):
        """Reveals the entire board upon the game ending."""
        for tile in self.tiles_list:
            self.tiles_dict[tile]["exposed"] = True
            self.tiles_dict[tile]["flag"] = False

    def draw_board(self):
        """Creates a string to render the board"""
        board_render = f"{symbols['origin']}{spacer(0, self.rows)}"
        
        #labels the columns at the top
        for i in range(1, self.columns+1):
            board_render += f"{i}{spacer(i, self.columns)}"
            if i == self.columns:
                board_render += f"\n"
        
        #renders each tile
        for coords, data in self.tiles_dict.items():
            #labels the row at the left side
            if coords[1] == 1:
                board_render += f"{coords[0]}{spacer(coords[0], self.rows)}"

            tile_render = ""
            if data["flag"] == True:
                tile_render = symbols["flag"]
            elif data["exposed"] == True:
                if data["snake"] == True:
                    tile_render = symbols["snake"]
                else:
                    tile_render = symbols["numbers"][(data["number"])]
            else:
                tile_render = symbols["hidden"]
            board_render += f"{tile_render}{tile_spacer(self.columns)}"
            if coords[1] == self.columns:
                board_render += "\n"
        print()
        print(board_render)

    def user_action(self, message, first=False):
        """Performs an action based on user input."""
        while True:
            if first == True:
                coord = input(message)
            else:
                user_input = input(message)
                inputs = user_input.split(" ")
                try:
                    action = inputs[0]
                    coord = inputs[1]
                except IndexError:
                    error_message(first)
                    continue
            coord_list = coord.split(",")
            try:
                coord_tuple = (int(coord_list[0]), int(coord_list[1]))
            except ValueError:
                error_message(first)
                continue

            if coord_tuple in self.tiles_list:
                if first == True:
                    self.set_snakes(coord_tuple)
                    self.set_numbers()
                    self.reveal_tile(coord_tuple)
                    break
            else:
                error_message(first)
                continue

            if action in ["f", "p"]:
                if action == "f":
                    if self.tiles_dict[coord_tuple]["exposed"] == True:
                        print("Can't flag an exposed tile!!!")
                        continue
                    elif self.tiles_dict[coord_tuple]["exposed"] == False:
                        self.flag_tile(coord_tuple)
                        break
                if action == "p":
                    if self.tiles_dict[coord_tuple]["exposed"] == True:
                        print("Can't pounce on an exposed tile!!!")
                        continue
                    if self.tiles_dict[coord_tuple]["snake"] == True:
                        self.lose = True
                        self.reveal_board()
                    elif self.tiles_dict[coord_tuple]["snake"] == False:
                        self.reveal_tile(coord_tuple)
                    break
            else:
                print("Action not recognized. Check your formatting?!")
                continue

    def flag_tile(self, coords):
        self.tiles_dict[coords]["flag"] = True
        
def get_positive_int(message, amount_type):
    """Ensures that an input is an integer. Takes 'idk' as a randomizer."""
    if amount_type == "rows" or "columns":
        greater_than = 3
    if amount_type == "snakes":
        greater_than = 0
        max_value = (area-10)
    while True:
        value = input(message)
        if value == 'idk':
            if amount_type == "rows" or amount_type == "columns":
                value = random.randint(5, 40)
            elif amount_type == "snakes":
                value = random.randint((int((area-10)*0.1)+1), (int((area-10)*0.4)))
            print(f"There are obviously {value}.")
            break
        try:
            value = int(value)
        except ValueError:
            print("Must be an integer!!")
        else:
            if value <= greater_than:
                print(f"Must be greater than {greater_than}!!!!")
            elif amount_type == "snakes":
                if value > max_value:
                    print(f"Must leave at least 10 open spaces! At most, {max_value}!!!")
                else:
                    break
            else:
                break
    return value


# Gameplay loop (not a loop yet)
print("Hello, welcome to snake avoider!")
rows = get_positive_int(f"\nHow many rows are in your lawn? (Type 'idk' if you don't know)\n", "rows")
columns = get_positive_int(f"\nHow many columns are in your lawn?\n", "columns")
area = rows*columns
snakes = get_positive_int(f"\nHow many snakes are in your lawn? (Type 'idk' if you don't know)\n", "snakes")
game = Board(rows, columns, snakes)
game.build_tiles()
game.draw_board()
game.user_action(f"\nChoose first tile to pounce on. Format: 'row,col'\n", first=True)
game.draw_board()
while game.unexposed:
    tile_message = f"\nInput an action and tile. 'p' to pounce, 'f' to flag, row and col as integers.\nFormat: 'action row,col'\n"
    game.user_action(tile_message)
    game.draw_board()
    if game.lose == True:
        break
if game.lose == True:
    print("You lose! Idiot!")
else:
    print("You are winner!")
    game.reveal_board()
    game.draw_board()
