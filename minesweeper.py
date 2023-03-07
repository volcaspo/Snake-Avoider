# class Tile():
#     """Represents a tile on the board"""
#     def __init__(self, coords):
#         self.coords = coords
#         self.flag = False
#         self.snake = False
#         self.number = 0

#     def add_flag(self, add=True):
#         """Adds or removes a flag to or from the tile"""
#         if add is True:
#             self.flag = True
#         if add is False:
#             self.flag = False
    
#     def set_snake(self):
#         """Sets a mine on a tile"""
#         self.snake = True

#     def set_number(self, number):
#         """Sets a number for the tile"""
#         self.number = number

import random

symbols = {
    "origin": "☺",
    "flag": "▷",
    "snake": "🐍",
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

class Board():
    """Represents the board containing the tiles"""
    def __init__(self, rows, columns, snakes):
        self.rows = rows
        self.columns = columns
        self.snakes = snakes

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
                
    def set_snakes(self, starting_tile):
        """
        Sets a selection of the tiles to be snakes.
        Retries until the starting tile is not a snake.
        """
        temp_tiles_list = self.tiles_list[:]
        temp_tiles_list.remove(starting_tile)
        snake_tiles = random.sample(temp_tiles_list, k=self.snakes)
        for tile in snake_tiles:
            self.tiles_dict[tile]["snake"] = True
        self.snake_tiles = snake_tiles

    def reveal_tile(self, coords):
        surrounding_tiles = []
        self.tile_dict[coords]["exposed"] = True
        for adjacent in adjacencies:
            tile = ((coords+adjacent[0]), (coords+adjacent[1]))
            surrounding_tiles.append(tile)
        for tile in surrounding_tiles:
            if tile in self.tiles_list:
                if self.tiles_dict[tile]["snake"] == False:
                    self.tiles_dict[tile]["exposed"] = True


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
        print(board_render)



    def flag_tile(self, coords):
        pass
    
                



game = Board(9, 9, 80)
game.build_tiles()
game.set_snakes((5, 5))
print(game.snake_tiles)
print(game.tiles_dict)
print((5, 5) in game.snake_tiles)

#game.tiles_dict[(2, 5)]["flag"] = True
#game.draw_board()

# active = True
# while active:
#     print("Hello, welcome to snake avoider!")
#     rows = input(f"How many rows are in your lawn? (Type 'idk' if you don't know)\n")
#     columns = input(f"How many columns are in your lawn?\n")
#     snakes = 0
#     while snakes == 0:
#         snakes_temp = input(f"How many snakes are in your lawn? (You know how many, right?)\n")
#         if 