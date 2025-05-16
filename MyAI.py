# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Serena Nguyen
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import itertools

class MyAI(AI):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        # Initialize the AI with board dimensions and starting position
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.board = [[None for _ in range(colDimension)] for _ in range(rowDimension)]
        
        self.uncovered_count = 0
        self.current_x = startX
        self.current_y = startY
        self.safe_tiles_to_uncover = (rowDimension * colDimension) - totalMines


    def getAction(self, number: int) -> Action:
        # Update the number of adjacent mines for the last uncovered tile
        self.board[self.current_y][self.current_x] = number
        self.uncovered_count += 1

        # If uncovered 24 tiles (in a 5x5 board with 1 mine), all safe tiles found, we are done
        if self.uncovered_count >= self.safe_tiles_to_uncover:
            print(f"[AI DEBUG] Turn: {self.uncovered_count}, Current pos: ({self.current_x}, {self.current_y}), Number: {number}")
            print(f"[AI DEBUG] Action: LEAVE, Coords: ({self.current_x}, {self.current_y})")
            return Action(AI.Action.LEAVE)

        # Step 1: try to find a guaranteed safe move (adjacent to a '0' tile)
        safe_move = self.find_safe_move()
        if safe_move:
            self.current_x, self.current_y = safe_move
            print(f"[AI DEBUG] Action: UNCOVER, Coords: ({self.current_x}, {self.current_y})")
            return Action(AI.Action.UNCOVER, self.current_x, self.current_y)

        # Step 2: If no guaranteed safe move, use model checking on the frontier
        frontier = self.get_frontier()
        if frontier:
            safe_tiles = self.model_checking(frontier)
            if safe_tiles:
                self.current_x, self.current_y = safe_tiles[0]
                print(f"[AI DEBUG] Action: UNCOVER, Coords: ({self.current_x}, {self.current_y})")
                return Action(AI.Action.UNCOVER, self.current_x, self.current_y)

        # Step 3: If no safe move found after model checking, choose the center-most covered tile
        self.current_x, self.current_y = self.get_center_most_covered()
        print(f"[AI DEBUG] Action: UNCOVER, Coords: ({self.current_x}, {self.current_y})")
        return Action(AI.Action.UNCOVER, self.current_x, self.current_y)

    def find_safe_move(self):
        # Scan the board for uncovered '0' tiles
		# And return an adjacent covered tile if found
        for y in range(self.rowDimension):
            for x in range(self.colDimension):
                if self.board[y][x] == 0: # Found a '0' tile
				    # Check 8 adjacent tiles
                    for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                        nx, ny = x + dx, y + dy
						 # Ensure the adjacent tile is within the board boundaries
                        if 0 <= nx < self.colDimension and 0 <= ny < self.rowDimension:
                            if self.board[ny][nx] is None:
                                return nx, ny
        return None # No safe moves found

    def get_frontier(self):
        # Identify the frontier which is the covered tiles adjacent to uncovered numbered tiles
        frontier = set()
        for y in range(self.rowDimension):
            for x in range(self.colDimension):
                if self.board[y][x] is not None and self.board[y][x] > 0:
					# Check 8 adjacent tiles
                    for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.colDimension and 0 <= ny < self.rowDimension:
                            if self.board[ny][nx] is None:  # Adjacent tile is covered
                                frontier.add((nx, ny))
        return list(frontier)

    def model_checking(self, frontier):
        # Use model checking to identify guaranteed safe or mine tiles
        constraints = self.get_constraints(frontier)
        safe_tiles = []
        mine_tiles = []

        for tile in frontier:
            is_safe = True
            is_mine = True
			# Generate all possible mine configurations for the frontier
            for assignment in itertools.product([0, 1], repeat=len(frontier)):
                if self.satisfies_constraints(assignment, constraints):
					# If this tile is a mine in this valid configuration
                    if assignment[frontier.index(tile)] == 1: 
                        is_safe = False
					#Else this tile is safe in this valid configuration
                    else:
                        is_mine = False
				# Cannot determine if this tile is safe or a mine, break
                if not is_safe and not is_mine: 
                    break
            if is_safe:
                safe_tiles.append(tile)
            elif is_mine:
                mine_tiles.append(tile)

        return safe_tiles

    def get_constraints(self, frontier):
        # Generate constraints based on the numbers on uncovered tiles adjacent to the frontier
        constraints = []
        for y in range(self.rowDimension):
            for x in range(self.colDimension):
                if self.board[y][x] is not None and self.board[y][x] > 0: # Uncovered numbered tile
                    constraint = []
                    count = 0
					# Check 8 adjacent tiles
                    for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.colDimension and 0 <= ny < self.rowDimension:
                            if (nx, ny) in frontier:
                                constraint.append(frontier.index((nx, ny)))
                            elif self.board[ny][nx] is None:
                                count += 1
                    if constraint:
						# sum of mines in these frontier tiles = number on tile - count of definite mines
                        constraints.append((constraint, self.board[y][x] - count))
        return constraints

    def satisfies_constraints(self, assignment, constraints):
        # Check if a given assignment of mines to frontier tiles satisfies all constraints
        for constraint, value in constraints:
            if sum(assignment[i] for i in constraint) != value:
                return False # constraint is violated!
        return True # All constraints are satisfied

    def get_center_most_covered(self):
        # Find the covered tile closest to the center of the board
        center_x, center_y = self.colDimension // 2, self.rowDimension // 2
        min_distance = float('inf')
        best_tile = None
        for y in range(self.rowDimension):
            for x in range(self.colDimension):
                if self.board[y][x] is None: # Tile is covered already
				    # Manhattan distance to center
                    distance = abs(x - center_x) + abs(y - center_y)
                    if distance < min_distance:
                        min_distance = distance
                        best_tile = (x, y)
        return best_tile