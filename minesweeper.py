import random

import block_numbers as bn

class ANSI():
    """Adds colors to strings"""
    green = '\x1B[32m'
    red = '\x1B[31m'
    lred = '\x1B[38;2;255;100;100m'
    lorange = '\x1B[38;2;255;128;0m'
    yellow = '\x1B[38;2;255;255;0m'
    lavender = '\x1B[38;2;180;160;255m'
    lcyan = '\x1B[38;2;0;255;255m'
    lblue = '\x1B[38;2;51;153;255m'
    lpurple = '\x1B[38;2;178;102;255m'
    lmagenta = '\x1B[38;2;255;102;255m'
    lgreen = '\x1B[38;2;128;255;0m'
    cyan = '\x1B[36m'
    gray = '\x1B[38;2;120;120;120m'
    white = '\x1B[37m'
    end = '\x1B[0m'
    bred = '\x1B[41m'

symbols = {
    "origin": ANSI.cyan+"☺"+ANSI.end,
    "flag": ANSI.red+"▹"+ANSI.end,
    "snake": ANSI.green+"S"+ANSI.end,
    "hidden": ANSI.white+"◇"+ANSI.end,
    "numbers": [
        ANSI.gray+"∙"+ANSI.end,
        ANSI.yellow+"1"+ANSI.end,
        ANSI.lorange+"2"+ANSI.end,
        ANSI.lred+"3"+ANSI.end,
        ANSI.lpurple+"4"+ANSI.end,
        ANSI.lblue+"5"+ANSI.end,
        ANSI.lmagenta+"6"+ANSI.end,
        ANSI.lcyan+"7"+ANSI.end,
        ANSI.lgreen+"8"+ANSI.end,
        ],
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

def spacer(max_number, current_number=1):
    """
    Creates a string with an appropriate length of spaces based on the length of key numbers.
    Used for keeping spacing consistent when rending the board.
    """
    return " "*(1 + len(str(max_number))-len(str(current_number)))

def error_message():
    print("Coords don't exist, or formatting is unclear. Type 'f' for formatting info.")

sizes = {
    "small": 4,
    "medium": 13,
    "large": 22,
}

class Board():
    """Represents the board containing the tiles"""
    def __init__(self, rows, columns, snakes):
        self.rows = rows
        self.columns = columns
        self.snakes = snakes
        self.lose = False

        #builds a list of block-number styles that are fit for the number of rows
        styles = []
        for size, measure in sizes.items():
            if self.rows >= measure:
                self.size = size
        for style in bn.styles:
            if style[0][1] == self.size and style[0][0] <= self.rows+2:
                styles.append(style)
        self.style = random.choice(styles)

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
        3 by 3 area around starting tile cannot be snakes.
        """
        temp_tiles_list = self.tiles_list[:]
        temp_tiles_list.remove(starting_tile)
        self.unexposed.remove(starting_tile)
        adjacent_tiles = self.build_adjacencies(starting_tile)
        for tile in adjacent_tiles:
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
        Or, if there are more snakes than number tiles,
        adds 1 to every number tile for each surrounding snake.
        """
        if self.snakes <= len(self.unexposed):
            for snake_tile in self.snake_tiles:
                adjacent_tiles = self.build_adjacencies(snake_tile)
                for tile in adjacent_tiles:
                    self.tiles_dict[tile]["number"] += 1
        else:
            for number_tile in self.unexposed:
                adjacent_tiles = self.build_adjacencies(number_tile)
                for tile in adjacent_tiles:
                    if self.tiles_dict[tile]["snake"] == True:
                        self.tiles_dict[number_tile]["number"] += 1

    def build_adjacencies(self, center_tile):
        adjacent_tiles = []
        for adjacent in adjacencies:
            tile = ((center_tile[0]+adjacent[0]), (center_tile[1]+adjacent[1]))
            if tile in self.tiles_list:
                adjacent_tiles.append(tile)
        return adjacent_tiles


    def reveal_tile(self, coords, satisfied=False):
        """
        Reveals selected tile, and reveals surroundings if the tile is a 0.
        Chains the revealing of 0-tiles.
        Only use if coords is not a snake tile.
        """
        to_reveal_surroundings = [coords]
        self.tiles_dict[coords]["exposed"] = True
        try:
            self.unexposed.remove(coords)
        except ValueError:
            pass
        while to_reveal_surroundings:
            center_tile = to_reveal_surroundings.pop()
            if self.tiles_dict[coords]["number"] == 0 or satisfied == True:
                adjacent_tiles = self.build_adjacencies(center_tile)
                for tile in adjacent_tiles:
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
            if self.tiles_dict[tile]["flag"] == False and self.tiles_dict[tile]["snake"] == True and self.lose != False:
                self.tiles_dict[tile]["snake"] = "missed"
            self.tiles_dict[tile]["flag"] = False

    def check_satisfaction(self, check_tile):
        """Checks whether a tile has enough flags around it to equal its number."""
        number = 0
        snake = False
        adjacent_tiles = self.build_adjacencies(check_tile)
        for tile in adjacent_tiles:
            if self.tiles_dict[tile]["flag"] == True:
                number += 1
            else:
                if self.tiles_dict[tile]["snake"] == True:
                    snake = True
        if number == self.tiles_dict[check_tile]["number"]:
            if snake == True:
                return "snake"
            else:
                return "satisfied"
        else:
            return "unsatisfied"
        

    def draw_board(self, first=False):
        """
        Creates a string to render the board.
        Renders the number of unexposed tiles to the right.
        """
        board_render = f"{symbols['origin']}{spacer(self.rows)}"
        if first == True:
            first_offset = self.snakes
        else:
            first_offset = 0
        num_lines = bn.build_number_lines(len(self.unexposed)-first_offset, self.style)

        #labels the columns at the top
        for i in range(1, self.columns+1):
            board_render += ANSI.cyan+f"{i}{spacer(self.columns, i)}"+ANSI.end
            if i == self.columns:
                board_render += f"{symbols['origin']}{spacer(self.rows)}"
                board_render += " "+num_lines[0]
                board_render += f"\n"
        
        #renders each tile
        for coords, data in self.tiles_dict.items():
            #labels the row at the start of each row
            if coords[1] == 1:
                board_render += ANSI.cyan+f"{coords[0]}{spacer(self.rows, coords[0])}"+ANSI.end

            tile_render = ""
            if data["flag"] == True:
                tile_render = symbols["flag"]
            elif data["exposed"] == True:
                if data["snake"] == True:
                    tile_render = symbols["snake"]
                elif data["snake"] == "missed":
                    tile_render = ANSI.bred+symbols["snake"]
                else:
                    tile_render = symbols["numbers"][(data["number"])]
            else:
                tile_render = symbols["hidden"]
            board_render += f"{tile_render}{spacer(self.columns)}"
            #makes new line at the end of each row
            if coords[1] == self.columns:
                board_render += ANSI.cyan+f"{coords[0]}{spacer(self.rows, coords[0])}"+ANSI.end
                if coords[0] < len(num_lines):
                    board_render += " "+num_lines[coords[0]]
                board_render += "\n"

        #labels the columns at the bottom
        board_render += f"{symbols['origin']}{spacer(self.rows)}"
        for i in range(1, self.columns+1):
            board_render += ANSI.cyan+f"{i}{spacer(self.columns, i)}"+ANSI.end
            if i == self.columns:
                board_render += f"{symbols['origin']}{spacer(self.rows)}"
        if self.rows == len(num_lines)-2:
            board_render += " "+num_lines[self.rows]

        print()
        print(board_render)

    def user_action(self, message, first=False):
        """Performs an action based on user input."""
        while True:
            user_input = input(message)
            other = universal_action(user_input, active=True)
            if other == "continue":
                continue
            elif other == "r":
                if first == False:
                    self.lose = "forfeit"
                    self.reveal_board()
                    self.draw_board()
                elif first == True:
                    self.lose = "restart"
                break
            elif other == "q":
                self.lose = "quit"
                break
            if first == True:
                coord = user_input
                action = ''
            else:
                try:
                    int_check = int(user_input[0])
                except:
                    action = user_input[0]
                    try:
                        coord = user_input[1:]
                    except IndexError:
                        error_message()
                else:
                    coord = user_input
                    action = "d"
            if " " in coord:
                coord = coord.strip(" ")
                if " " in coord:
                    coord_list = coord.split(" ")
                if "," in coord:
                    coord_list = coord.split(",")
            elif "," in coord:
                coord_list = coord.strip(",").split(",")
            else:
                error_message()
                continue

            try:
                coord_tuple = (int(coord_list[0]), int(coord_list[1]))
            except:
                error_message()
                continue

            if coord_tuple in self.tiles_list:
                if first == True:
                    self.set_snakes(coord_tuple)
                    self.set_numbers()
                    self.reveal_tile(coord_tuple)
                    break

            else:
                error_message()
                continue

            if action in ["f", "p", "o", "d"] or type(user_input[0]) is int:
                if action == "f" or action == "p":
                    act = "flag" if action == "f" else "pamper"
                    if self.tiles_dict[coord_tuple]["exposed"] == True:
                        if self.flag_surroundings(coord_tuple):
                            print(f"This tile has no surroundings to {act}!")
                            continue
                        else:
                            break
                    elif self.tiles_dict[coord_tuple]["exposed"] == False:
                        self.flag_tile(coord_tuple)
                        break
                if action == "o" or action == "d" or type(user_input[0]) is int:
                    act = "occupy" if action == "o" else "diddle"
                    if self.tiles_dict[coord_tuple]["exposed"] == True:
                        satisfied = self.check_satisfaction(coord_tuple)
                        if satisfied == "satisfied":
                            self.reveal_tile(coord_tuple, satisfied=True)
                        elif satisfied == "unsatisfied":
                            print(f"Can't expose all the surroundings of an unsatisfied tile!")
                            continue
                        elif satisfied == "snake":
                            self.lose = "lose"
                            self.reveal_board()
                            self.draw_board()
                    elif self.tiles_dict[coord_tuple]["flag"] == True:
                        print(f"Can't {act} on a flagged/pampered tile!")
                        continue
                    if self.tiles_dict[coord_tuple]["snake"] == True:
                        self.lose = "lose"
                        self.reveal_board()
                        self.draw_board()
                    elif self.tiles_dict[coord_tuple]["snake"] == False:
                        self.reveal_tile(coord_tuple)
                    break
            else:
                error_message()
                continue

    def flag_tile(self, coords):
        """Toggles 'flag' for a tile."""
        if self.tiles_dict[coords]["flag"] == False:
            self.tiles_dict[coords]["flag"] = True 
        else:
            self.tiles_dict[coords]["flag"] = False

    def flag_surroundings(self, coords):
        """
        Toggles 'flag' for all the surroundings of a tile.
        Only unflags if all the surroundings are flagged.
        Returns a value only if it fails.
        """
        unexposed = 0
        flagged = 0
        adjacent_tiles = self.build_adjacencies(coords)
        for tile in adjacent_tiles:
            if self.tiles_dict[tile]["exposed"] == False:
                unexposed += 1
                if self.tiles_dict[tile]["flag"] == True:
                    flagged += 1
        if unexposed == 0:
            return "fail"
        elif flagged == unexposed:
            for tile in adjacent_tiles:
                if self.tiles_dict[tile]["exposed"] == False:
                    self.tiles_dict[tile]["flag"] = False
        else:
            for tile in adjacent_tiles:
                if self.tiles_dict[tile]["exposed"] == False:
                    self.tiles_dict[tile]["flag"] = True
            


def get_positive_int(message, amount_type, active=False):
    """Ensures that an input is an integer within a set range. Takes 'idk' as a randomizer."""
    if amount_type == "rows" or "columns":
        min_value = 3
    if amount_type == "snakes":
        min_value = 0
        max_value = (area-10)
    while True:
        value = input(message)
        other = universal_action(value, active)
        if other == 'continue':
            continue
        if other == 'q' or other == 'r':
            break
        if value == 'idk':
            if amount_type == "rows" or amount_type == "columns":
                value = random.randint(5, 40)
            elif amount_type == "snakes":
                value = random.randint((int((area-10)*0.13)+1), (int((area-10)*0.28)))
            print(f"There are obviously {value}.")
            break
        try:
            value = int(value)
        except ValueError:
            print("Must be an integer!")
        else:
            if value <= min_value:
                print(f"Must be greater than {min_value}!")
            elif amount_type == "snakes":
                if value > max_value:
                    print(f"Must leave at least 10 open spaces! At most, {max_value}!!!")
                else:
                    break
            else:
                break
    return value

def get_text_input(question, options):
    """Prompts user for inputs until an available option is chosen."""
    while True:
        user_input = input(question)
        if user_input in options:
            break
        else:
            other = universal_action(user_input)
            if other == "continue":
                continue
            elif other == "q":
                break
            else:
                print("Action not recognized. Try again.")
    return user_input


def universal_action(input, active=False):
    """Processes inputs to check for actions that can be entered at any time."""
    if input == 'i':
        print("""
        You are looking to diddle on your grid-shaped lawn, but there are snakes.
        If you diddle on the home of a snake, you will be eaten alive in one big gulp.
        Luckily, your lawn has numbers to indicate the presence of adjacent snakes.
        You will not be satisfied until you have diddled or occupied every snake-free tile.
        """)
        return "continue"
    if input == 'f':
        print("""
        For your action, you can either occupy/diddle a tile or you can flag/pamper a tile.
        These each have a corresponding letters: 'o', 'd', 'f', 'p'.
        If you are on your first turn, you don't need an action.
        If you don't type in an action, your action will by default be diddle.

        For your coordinates, you must input a row and then a column as integers.
        The action and the coordinates can either be separated by a space or a comma.
        Pro tip: the action does not need to be separated from the coordinates.

        Examples of acceptable formatting:
        'p 1,2'   'f5 9'   'o,3,4'   'd 15 3'   'f,6 14'   '4 11'
        """)
        return "continue"
    if input == "b":
        print("""
        You win if you expose every non-snake tile.
        You lose if you expose a snake tile.
        You can expose tiles by diddling on/occupying them.
        You can flag/pamper tiles that you think are snakes.
        You can unflag tiles that are flagged.
        You can't expose a tile that is flagged/pampered.

        Each tile has a number representing the quantity of adjacent snakes.
        Tiles are adjacent if they are in adjacent rows or columns, including diagonals.

        ADVANCED RULES FOR SPEEDY GAMEPLAY:
        By diddling/occupying an exposed and satisfied tile, you can expose all its adjacent unflagged tiles.
        A tile is satisfied if the number on the tile equals the number of surrounding flags.
        By flagging/pampering an exposed tile, you can flag or unflag all of its surroundings.
        """)
        return "continue"
    if input == "r":
        if active == False:
            print("There is no game to forfeit!")
            return "continue"
        elif active == True:
            return input
    if input == 'q' or input == 'r':
        return input

modes = {
    "custom": None,
    "easy": [9, 9, 10],
    "medium": [16, 16, 40],
    "hard": [30, 16, 99],
    "extreme": [35, 25, 210],
    "impossible": [100, 100, 9990],
    "snake": [9, 9, 1],
}


# Gameplay loop
print(f"""
Hello, welcome to {ANSI.green}Snake{ANSI.end} {ANSI.red}Avoider{ANSI.end}!

At any time, input 'i' for instructions, 'b' for rulebook,
'f' for formatting info, 'r' to restart/forfeit, or 'q' to quit""")

same = False
while True:
    if same == False:
        mode = get_text_input(f"\n{ANSI.end}How difficult is your lawn to traverse? Options:\n"
            f"'easy'   'medium'   'hard'   'extreme'   'impossible'   'snake'   'custom'\n{ANSI.lavender}",
            list(modes.keys()))
        if mode == 'custom':
            rows = get_positive_int(f"{ANSI.end}\nHow many rows are in your lawn? (Type 'idk' if you don't know)\n{ANSI.lavender}", "rows", active=True)
            if rows == 'q':
                break
            elif rows == 'r':
                continue
            columns = get_positive_int(f"{ANSI.end}\nHow many columns are in your lawn? (Type 'idk' if you don't know)\n{ANSI.lavender}", "columns", active=True)
            area = rows*columns
            if columns == 'q':
                break
            elif columns == 'r':
                continue
            snakes = get_positive_int(f"{ANSI.end}\nHow many snakes are in your lawn? (Type 'idk' if you don't know)\n{ANSI.lavender}", "snakes", active=True)
            if snakes == 'q':
                break
            elif snakes == 'r':
                continue
        elif mode == 'q':
            break
        else:
            rows = modes[mode][0]
            columns = modes[mode][1]
            snakes = modes[mode][2]

    game = Board(rows, columns, snakes)
    game.build_tiles()
    game.draw_board(first=True)
    game.user_action(f"{ANSI.end}\nChoose first tile to diddle on. Input coordinates:\n{ANSI.lavender}", first=True)

    if game.lose == False and game.unexposed:
        game.draw_board()

        # Action loop
        while game.unexposed:
            tile_message = f"{ANSI.end}\nInput action and coordinates:\n{ANSI.lavender}"
            game.user_action(tile_message)
            if game.lose != False or not game.unexposed:
                break
            game.draw_board()

    # Game endings
    if game.lose == "quit":
        break
    elif game.lose == "restart":
        continue
    elif game.lose == "lose":
        print(f"\n{ANSI.end}You lose! {ANSI.red}FAIL!!{ANSI.end}")
    elif game.lose == "forfeit":
        print(f"\n{ANSI.end}You gave up! {ANSI.red}Nooooo!{ANSI.end}")
    else:
        game.reveal_board()
        game.draw_board()
        print(f"\n{ANSI.end}You are winner! {ANSI.green}Champion!!!{ANSI.end}")
    again = get_text_input(f"{ANSI.end}Type 's' to play again with the same settings,\n"
        f"or type 'd' to play with different settings.\n{ANSI.lavender}", ['s','d'])
    if again == 'q':
        break
    if again == 's':
        same = True
    if again == 'd':
        same = False
print(f"{ANSI.end}")