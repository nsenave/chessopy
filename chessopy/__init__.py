# This file is part of the chessopy library.
# Copyright (C) 2020 Nicolas Sénave <email>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
A simple graphical interface written only in Python using tkinter.
A very simple oriented object was written to modelize the chess game.
The rules of chess are not implemented in these objects, that means 
that the user can make whatever he wants on the board.
"""

__author__ = "Nicolas Sénave"

# __email__ = "email" 
# NB: I will create an email for this project if some are interested by it.

__version__ = "0.0.1-SNAPSHOT"

from enum import Enum
from abc import ABC, abstractmethod
from typing import List
import re
import json
from random import randrange
from tkinter import Tk, Canvas, PhotoImage, Button, Label, \
    N, E, S, W, NE, NW, SE, SW, X, Y, BOTH

# TODO: work with relative path instead...
FOLDER_PATH = "C:/Users/Nico/Documents/chessopy/"

# TODO: improve the file gestion (NB: comment already written in MovLines)
LINES_TO_BE_LOADED = "french"
# write a name of a saved database in the folder (<name>_database.json)
# write "new" to start with an empty dictionnary

############ Chess objects ############

class PieceColor(Enum) :
    BLACK = 0
    WHITE = 1

class Piece(ABC) :
    """
    Abstract buisness class for chess pieces.
    A piece is initialized with a PieceColor.
    A piece has a square number which can be used to find 
    the square that the piece has been put on.
    """
    
    def __init__(self, piece_color: PieceColor) :
        self.color = piece_color
        self.san_name = None
        self.value = None
        self.square_number = None
    
    def get_color(self) -> PieceColor :
        return self.color
    
    def get_san_name(self) -> str :
        return self.san_name
    
    def set_square_number(self, square_number: int) :
        self.square_number = square_number
    
    def get_value(self) -> int :
        return self.value
    
    def get_square_number(self) -> int :
        return self.square_number

class Pawn(Piece) :
    
    def __init__(self, piece_color: PieceColor) :
        Piece.__init__(self, piece_color)
        self.value = 1
        self.san_name = 'P'

class Knight(Piece) :
    
    def __init__(self, piece_color: PieceColor) :
        Piece.__init__(self, piece_color)
        self.value = 3
        self.san_name = 'N'

class Bishop(Piece) :
    
    def __init__(self, piece_color: PieceColor) :
        Piece.__init__(self, piece_color)
        self.value = 3
        self.san_name = 'B'

class Rook(Piece) :
    
    def __init__(self, piece_color: PieceColor) :
        Piece.__init__(self, piece_color)
        self.value = 5
        self.san_name = 'R'

class Queen(Piece) :
    
    def __init__(self, piece_color: PieceColor) :
        Piece.__init__(self, piece_color)
        self.value = 9
        self.san_name = 'Q'

class King(Piece) :
    
    def __init__(self, piece_color: PieceColor) :
        Piece.__init__(self, piece_color)
        self.san_name = 'K'

class SquareColor(Enum) :
    DARK = 0
    LIGHT = 1

class Square() :
    """
    Business class for the board squares.
    A square is defined with his rank and file, 
    which are integers between 0 and 7 included.
    These are called the square 'coordinates'.
    """

    RANK_NAMES = ['1','2','3','4','5','6','7','8']
    FILE_NAMES = ['a','b','c','d','e','f','g','h']

    @staticmethod
    def calculate_square_color(file_number: int, rank_number: int) -> SquareColor :
        """Return the SquareColor corresponding to the square coordinates."""
        return (file_number%2 + rank_number%2)%2

    def __init__(self, rank_number, file_number) :
        self.rank = rank_number
        self.file = file_number
        self.color = Square.calculate_square_color(rank_number, file_number)
        self.piece = None
    
    def __repr__(self) :
        return f"Square({self.rank},{self.file})"
    
    def __str__(self) :
        return f"{self.get_name()} square."
    
    def get_rank(self) -> int :
        """Return the rank nulber of the square."""
        return self.rank

    def get_file(self) -> int :
        """Return the file number of the square."""
        return self.file
    
    def get_file_name(self) -> str :
        """
        Return the file name of the square.
        For instance : 'e'.
        Notice that the name is calculated and is not an attribute of the class.
        """
        return Square.FILE_NAMES[self.file]

    def get_name(self) -> str :
        """
        Return the name of the square.
        For instance : 'e4'.
        Notice that the name is calculated and is not an attribute of the class.
        """
        rank_name = Square.RANK_NAMES[self.rank]
        file_name = Square.FILE_NAMES[self.file]
        return f"{file_name}{rank_name}"
    
    def get_number(self) -> int :
        """Return the number that the square has on the board."""
        return self.rank*8 + self.file
    
    def get_color(self) :
        return self.color
    
    def put_piece(self, piece: Piece) :
        """Put the given piece on the square."""
        self.piece = piece
    
    def remove_piece(self) :
        """Remove the piece (if exists) from the square.
        Nothing happens if the square was already empty."""
        self.piece = None
    
    def get_piece(self) -> Piece :
        """Return the piece which is on the square.
        Return None if there is no piece on the square."""
        return self.piece

    def has_piece(self) -> bool :
        return self.piece is not None
    
    def is_empty(self) -> bool :
        return self.piece is None

class Move() :
    """
    Chess class to manage moves.
    A move is defined by the start_square and the destination_square.
    An exception is raised if the start square has no piece.
    """

    def __init__(self, start_square: Square, destination_square: Square) :
        if start_square.is_empty() :
            raise NoPieceOnStartSquareException()
        self.start_square = start_square
        self.destination_square = destination_square
        self.piece_taken = destination_square.piece
    
    def __str__(self) :
        return f"({self.start_square.get_number()},{self.destination_square.get_number()})"
    
    def get_san_notation(self) -> str :
        """
        Return the san notation of the move.
        NB: disambiguation of ambiguous knight moves is not implemented.
        """
        res = ""
        moving_piece = self.start_square.piece
        res = res + self.destination_square.get_name()
        if self.destination_square.has_piece() :
            res = 'x' + res
            if type(moving_piece) is Pawn :
                res = self.start_square.get_file_name() + res
        if type(moving_piece) is not Pawn :
            res = moving_piece.get_san_name() + res
        return res
    
    def get_piece_taken(self) :
        return self.piece_taken

class MoveLines(dict) :
    """
    Subclass from dict which is designed to contain moves (class Move).
    The class has methods to save and load lines in/from json files.
    """
    # TODO: some work with the file gestion ... ...
    def __init__(self, lines_name=LINES_TO_BE_LOADED) :
        #
        dict.__init__(self)
        self.lines_name = lines_name
        #
        self["move_lines"] = {} # root node
        #
        if lines_name == "new" : # TODO: cf. last comment. This doesn't make any sense
            pass # do nothing
        else :
            self.load_from_database(lines_name)
        #
        self.current_node = self["move_lines"]
        self.current_line = []
    
    def load_from_database(self, lines_name: str) :
        """
        The lines_name argument is the name of the lines in the database.
        "all" will load the entire database
        Otherwise: 
        For instance: "french" will select the moves which have been recorded under that name.
        """
        with open(FOLDER_PATH + "databases/" + lines_name + "_database.json") as json_database :
            loaded_dict = json.load(json_database)
            print("loaded_dict : ", loaded_dict)
        self["move_lines"] = loaded_dict["move_lines"]
    
    def save_new_database(self, database_name="new_database.json") :
        # TODO: relative path...
        with open(FOLDER_PATH + "databases/" + database_name, 'w') as json_database :
            json.dump(self, json_database) #indent=2
    
    def add_curent_lines_to_database(self) :
        # TODO
        pass

    def go_to_root(self) :
        """
        Set the current_node attribute to the root of the dict (which is self itself).
        The current_line is reseted.
        """
        self.current_node = self["move_lines"]
        self.current_line = []
    
    def go_to_child(self, key) -> dict :
        """
        Set the current_node attribute to the child using the key given.
        If the key does not exist, create a new branch with the key given and 
        {} (empty dict) as value.
        The key is added to the current_line attribute.
        """
        if key not in self.current_node :
            self.current_node[key] = {}
            print("MoveRecord: Adding a new node.")
        self.current_line.append(key)
        self.current_node = self.current_node[key]
    
    def go_to_parent(self) -> dict :
        """
        Set the current_node attribute to its parent.
        The current node is unchanched if current_node is already at the top.
        """
        if self.current_line != [] :
            self.current_line.pop()
            # We go to root then remake the line
            self.current_node = self["move_lines"]
            for key in self.current_line :
                self.current_node = self.current_node[key]
        else :
            print("MoveRecord: Warning: already at the top node.")

    def add_move(self, move: Move) :
        """
        Add the move given to the dictionnary.
        """
        key = f"{move.start_square.get_number()},{move.destination_square.get_number()}"
        self.go_to_child(key)
    
    def get_coords_of_current_node(self) -> tuple :
        """
        Get the key of the curent node, for instance "52,44", 
        convert it to a tuple like (52,44) and return it.
        """
        key = next(iter(self.current_node))
        coords = tuple(int(number) for number in key.split(','))
        print(f"Coords of current move in the dict : {coords}")
        return coords
    
    def get_coords_of_childs_of_current_node(self) -> List[tuple] :
        """
        Return the list of the coords of the children of the current node.
        Coords are tuple like (52,44).
        """
        res = []
        for key in self.current_node :
            res.append(tuple(int(number) for number in key.split(',')))
        return res

class NotValidSanMoveException(Exception) :
    pass

class Board() :
    """
    Business class for the chess board.

    The board contains a list of 64 squares named squares.
    The pieces are stored in black_pieces and white_pieces lists 
    when created (allows to iterate on the piece of a side without 
    testing a color condition).

    >>> board = Board()
    """

    @staticmethod
    def create_squares() -> List[Square] :
        """Return a list of all the board squares."""
        res = []
        for rank_number in range(8):
            for file_number in range(8):
                res.append(Square(rank_number, file_number))
        return res
    
    @staticmethod
    def create_pieces_set(color: PieceColor) : # NB: not used for the moment
        """Return a list of 8 pawns, 2 rooks, 2 bishops, 2 knights, 1 queen, 1 knight,
        of the given color."""
        res = [Pawn(color) for k in range(8)]
        res += [Rook(color) for k in range(2)]
        res += [Bishop(color) for k in range(2)]
        res += [Knight(color) for k in range(2)]
        res += [Queen(color), King(color)]
        return res

    def __init__(self) :
        self.squares = Board.create_squares()
        self.white_pieces = []
        self.black_pieces = []
        # move_played is a list of moves (class Move)
        self.move_played = []
        # move_lines is a MoveLines object.
        # Its current_line attribute is a list of coords of moves :
        # (start_square_number, destination_square_number)
        self.move_lines = MoveLines()
        #
        self.set_new_game()
    
    def __str__(self) :
        pass
    
    def get_square_from_number(self, square_number: int) -> Square :
        """
        Return the square at index square_number from the squares list.
        Thus, square_number must be between 0 and 63.
        """
        return self.squares[square_number]
    
    def get_square_from_coords(self, rank_number:int, file_number:int) -> Square :
        """
        Return square of given coordinates
        rank and file must be between 0 and 7.
        """
        return self.squares[rank_number*8 + file_number]
    
    def get_square_from_name(self, square_name: str) -> Square :
        """
        Return the square that correspond to the square_name.
        The square_name is for instance 'e4'.
        """
        rank_number = Square.RANK_NAMES.index(square_name[1])
        file_number = Square.FILE_NAMES.index(square_name[0])
        return self.get_square_from_coords(rank_number, file_number)
    
    def put_piece_on_square(self, piece: Piece, square: Square) :
        square.put_piece(piece)
        piece.set_square_number(square.get_number())

    def get_all_pieces(self) -> List[Piece] :
        """Return a list containing all the pieces on board.
        Note that this method does not allow to modify the piece lists 
        of the board."""
        return self.white_pieces + self.black_pieces

    def delete_all_pieces(self) :
        """Renew white_pieces and black_pieces as new lists.
        NB: This method doesn't really delete the piece since they still exist 
        on the squares !"""
        # TODO: improve the gestion of pieces
        # (these two lists seem pointless...)
        self.white_pieces = []
        self.black_pieces = []
    
    def set_new_game(self) :
        """
        Set the white and black pieces on the board.
        """
        #
        self.move_played = []
        self.move_lines.go_to_root()
        # Clean the board
        self.delete_all_pieces()
        for square in self.squares :
            square.piece = None
        # Create and put the 8 pawns on each side
        for file_number in range(8) :
            white_pawn = Pawn(PieceColor.WHITE)
            self.white_pieces.append(white_pawn)
            self.put_piece_on_square(white_pawn, self.get_square_from_coords(1, file_number))
            black_pawn = Pawn(PieceColor.BLACK)
            self.black_pieces.append(black_pawn)
            self.put_piece_on_square(black_pawn, self.get_square_from_coords(6, file_number))
        # Create and put pieces which come by two
        for k in range(2) :
            white_bishop = Bishop(PieceColor.WHITE)
            white_knight = Knight(PieceColor.WHITE)
            white_rook = Rook(PieceColor.WHITE)
            self.white_pieces.extend([white_bishop, white_knight, white_rook])
            self.put_piece_on_square(white_bishop, self.get_square_from_coords(0, 2+k*3))
            self.put_piece_on_square(white_knight, self.get_square_from_coords(0, 1+k*5))
            self.put_piece_on_square(white_rook, self.get_square_from_coords(0, 0+k*7))
            black_bishop = Bishop(PieceColor.BLACK)
            black_knight = Knight(PieceColor.BLACK)
            black_rook = Rook(PieceColor.BLACK)
            self.black_pieces.extend([black_bishop, black_knight, black_rook])
            self.put_piece_on_square(black_bishop, self.get_square_from_coords(7, 2+k*3))
            self.put_piece_on_square(black_knight, self.get_square_from_coords(7, 1+k*5))
            self.put_piece_on_square(black_rook, self.get_square_from_coords(7, 0+k*7))
        # King and Queen
        white_queen = Queen(PieceColor.WHITE)
        self.white_pieces.append(white_queen)
        self.put_piece_on_square(white_queen, self.get_square_from_coords(0, 3))
        black_queen = Queen(PieceColor.BLACK)
        self.black_pieces.append(black_queen)
        self.put_piece_on_square(black_queen, self.get_square_from_coords(7, 3))
        white_king = King(PieceColor.WHITE)
        self.white_pieces.append(white_king)
        self.put_piece_on_square(white_king, self.get_square_from_coords(0, 4))
        black_king = King(PieceColor.BLACK)
        self.black_pieces.append(black_king)
        self.put_piece_on_square(black_king, self.get_square_from_coords(7, 4))

    def move_piece(self, piece: Piece, destination_square: Square, undo=False) :
        """Moves the given piece on the given square."""
        # Get the values needed
        start_square_number = piece.get_square_number()
        start_square = self.get_square_from_number(start_square_number)
        # Record move
        if not undo :
            move = Move(start_square, destination_square)
            # In move_played
            self.move_played.append(move)
            # In move_lines
            self.move_lines.add_move(move)
            #
            print(move.get_san_notation())
        # Move piece
        piece.set_square_number(destination_square.get_number())
        start_square.remove_piece()
        destination_square.put_piece(piece)
    
    def pop_last_move(self) -> Move :
        """Undo the last move and return it."""
        # Pop move from move_played
        last_move = self.move_played.pop()
        # Go in the parent in move_lines
        self.move_lines.go_to_parent()
        # Change what to be changed on the board
        self.move_piece(last_move.destination_square.piece, last_move.start_square, undo=True)
        if last_move.piece_taken is not None :
            self.put_piece_on_square(last_move.piece_taken, last_move.destination_square)
        return last_move
    
    def castle_king_side(self) :
        """Warning : function does not check if catling is possible."""
        pass

    def castle_queen_side(self) :
        """Warning : function does not check if catling is possible."""
        pass

    def move_en_passant(self) :
        pass
    
    def move_from_san(self, san_string: str) :
        """Make the move from the san move given.
        An exception is raised if the given san move is not valid.
        Note: the 'e.p.' mention for en passant moves makes the expression not valid."""
        # Check if the expression is correct
        san_pattern = re.compile(r"/^([NBRQK])?([a-h])?([1-8])?(x)?([a-h][1-8])(=[NBRQK])?(\+|#)?$|^O-O(-O)?$/")
        if not san_pattern.match(san_string) :
            raise NotValidSanMoveException()
        # Remove the non 'move-meaningfull' characters # NB: maybe not usefull to do that finally
        san_string.replace('#', '')
        san_string.replace('+', '')
        # Castle
        if 'O-O-O' in san_string :
            self.castle_queen_side()
        elif 'O-O' in san_string :
            self.castle_king_side()
        # Other moves
        else :
            destination_san_square = re.findall(r"[a-h][1-8]", san_string)
            san_string.replace(destination_san_square, '')
            moving_piece_name = re.findall(r"K|Q|R|B|N", san_string).pop()
            # to be continued... ####################################################################################
    
    def set_training_lines(self, lines_name: str) :
        """
        Load a set of lines using MoveLines.load_from_database
        The lines_name argument is the name of the lines in the database.
        "all" will load the entire database
        Otherwise: 
        For instance: "french" will select the moves which have been recorded under that name.
        """
        self.move_lines.load_from_database(lines_name)
    
    def check_move(self, move: Move) -> bool :
        """
        Check if the move given is in the lines chosen.
        """
        start_square_number = move.start_square.get_number()
        destination_square_number = move.start_square.get_number()
        coords = (start_square_number, destination_square_number)
        return coords in self.move_lines.current_node

class NoPieceOnStartSquareException(Exception) :
    pass

############ Graphical objects ############

SQUARE_SIZE = 86
BOARD_SIZE = SQUARE_SIZE * 8

class PieceGui(PhotoImage) :
    
    def __init__(self, piece: Piece, image_path: str) :
        PhotoImage.__init__(self, file=image_path)
        self.piece = piece

class SquareGui(Canvas) :

    DARK_BG = 'lightgrey'
    LIGHT_BG = 'lightblue'

    SELECTED_COLOR = 'yellow'

    HIGHLIGHTED_COLOR = 'blue'

    def __init__(self, parent, square: Square) :
        # Init
        Canvas.__init__(self, parent, width=SQUARE_SIZE, height=SQUARE_SIZE)
        self.parent = parent
        # Square attribute
        self.square = square
        self.selected = False
        self.highlighted = False
        # Graphical piece
        self.piece_gui = None
        # Position on the board canvas
        x_position = 1/8 * self.square.get_file()
        y_position = 1 - (1/8 * (self.square.get_rank() + 1))
        self.place(relx=x_position, rely=y_position)
        # Configure square background
        if self.square.get_color() == SquareColor.DARK.value :
            self.base_color = SquareGui.DARK_BG
        else :
            self.base_color = SquareGui.LIGHT_BG
        self.configure(bg=self.base_color)
        # Button bindings
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
    
    def set_piece_gui(self, piece_gui: PieceGui) :
        """Set the piece_gui attribute."""
        self.piece_gui = piece_gui

    def display_piece(self) :
        self.create_image(0, 0, image=self.piece_gui, anchor=NW)
    
    def clear_square(self) :
        self.delete("all")
    
    def select(self) :
        self.selected = True
        self.point()
        self.parent.square_gui_selected = self

    def unselect(self) :
        self.selected = False
        self.unpoint()
        self.parent.square_gui_selected = None
    
    def point(self) :
        self.configure(bg=SquareGui.SELECTED_COLOR)
    
    def unpoint(self) :
        if self.highlighted :
            self.configure(bg=SquareGui.HIGHLIGHTED_COLOR)
        else :
            self.configure(bg=self.base_color)
    
    def on_left_click(self, event) :
        if self.selected :
            self.unselect()
        else :
            if self.parent.square_gui_selected is None :
                if self.square.has_piece() :
                    self.select()
                else :
                    pass # do nothing
            else :
                if self.parent.is_training_session :
                    self.parent.check_then_make_move(self)
                else :
                    self.parent.make_move(self)
                self.parent.square_gui_selected.unselect()
    
    def highlight(self) :
        self.configure(bg=SquareGui.HIGHLIGHTED_COLOR)
        self.highlighted = not self.highlighted
    
    def unhighlight(self) :
        if not self.selected :
            self.configure(bg=self.base_color)
        else :
            self.configure(bg=SquareGui.HIGHLIGHTED_COLOR)
        self.highlighted = not self.highlighted

    def on_right_click(self, event) :
        if not self.highlighted :
            self.highlight()
        else :
            self.unhighlight()
        

class BoardGui(Canvas) :
    
    def __init__(self, parent) :
        Canvas.__init__(self, parent, width=BOARD_SIZE, height=BOARD_SIZE)
        self.parent = parent
        self.board = Board()
        self.squares_gui = []
        for square in self.board.squares :
            self.squares_gui.append(SquareGui(self, square))
        #
        self.square_gui_selected = None
        #
        self.off_board_pieces_gui = []
        #
        self.is_training_session = False
        # self.training_list = [ #this list will be replaced by board.move_lines
        #     (12,28),
        #     (52,44),
        #     (11,27),
        #     (51,35),
        #     (28,36),
        #     (50,34)
        #     ]
        # self.move_number = 0
    
    def display_all_pieces(self) :
        for piece in self.board.get_all_pieces() :
            image_path = FOLDER_PATH + "images/piece_sets/cburnett/86x86/" # TODO: relative path...
            if piece.get_color() == PieceColor.BLACK :
                image_file = "black"
            else :
                image_file = "white"
            if type(piece) is Pawn :
                image_file += "_pawn.png"
            elif type(piece) is Knight :
                image_file += "_knight.png"
            elif type(piece) is Bishop :
                image_file += "_bishop.png"
            elif type(piece) is Rook :
                image_file += "_rook.png"
            elif type(piece) is Queen :
                image_file += "_queen.png"
            else :
                image_file += "_king.png"
            piece_gui = PieceGui(piece, image_path+image_file)
            square_number = piece.get_square_number()
            square_gui = self.squares_gui[square_number]
            square_gui.set_piece_gui(piece_gui)
            square_gui.display_piece()

    def clear_board(self) :
        for square_gui in self.squares_gui :
            square_gui.piece_gui = None
            square_gui.clear_square()
    
    def reset_position(self) :
        self.board.set_new_game()
        self.clear_board()
        self.display_all_pieces()

    def check_then_make_move(self, square_gui: SquareGui) :
        start_square_number = self.square_gui_selected.square.get_number()
        destination_square_number = square_gui.square.get_number()
        next_moves_coords = self.board.move_lines.get_coords_of_childs_of_current_node()
        if (start_square_number, destination_square_number) not in next_moves_coords :
            print("T'es pas dans le coup.")
        else :
            self.make_move(square_gui)

    def make_move(self, square_gui: SquareGui) :
        #
        self.parent.undo_button.configure(state="normal")
        #
        if square_gui.square.has_piece() :
            self.off_board_pieces_gui.append(square_gui.piece_gui)
            square_gui.clear_square()
        self.board.move_piece(self.square_gui_selected.square.piece, square_gui.square)
        square_gui.set_piece_gui(self.square_gui_selected.piece_gui)
        square_gui.display_piece()
        self.square_gui_selected.clear_square()
        #
        if self.is_training_session :
            self.square_gui_selected.unpoint()
            # square_gui.point()
            self.update()
            # square_gui.unpoint()
            self.play_random_move()
    
    def make_computer_move(self, start_square_number: int, destination_square_number: int) :
        """Make a move without using the square_gui_selected attribute."""
        # Get the squares
        start_square_gui = self.squares_gui[start_square_number]
        destination_square_gui = self.squares_gui[destination_square_number]
        # 
        if destination_square_gui.square.has_piece() :
            self.off_board_pieces_gui.append(destination_square_gui.piece_gui)
            destination_square_gui.clear_square()
        self.board.move_piece(start_square_gui.square.piece, destination_square_gui.square)
        destination_square_gui.set_piece_gui(start_square_gui.piece_gui)
        destination_square_gui.display_piece()
        start_square_gui.clear_square()
    
    def undo_last_move(self, event) :
        if not self.board.move_played == [] :
            # In case of a square was selected while the user clicked 'Undo'
            if self.square_gui_selected is not None :
                self.square_gui_selected.unselect()
            #
            last_move = self.board.pop_last_move()
            piece_gui_unmoved = self.squares_gui[last_move.destination_square.get_number()].piece_gui
            self.squares_gui[last_move.start_square.get_number()].set_piece_gui(piece_gui_unmoved)
            self.squares_gui[last_move.start_square.get_number()].display_piece()
            self.squares_gui[last_move.destination_square.get_number()].clear_square()
            if last_move.piece_taken is not None :
                self.squares_gui[last_move.destination_square.get_number()].set_piece_gui(self.off_board_pieces_gui.pop())
                self.squares_gui[last_move.destination_square.get_number()].display_piece()
        if self.board.move_played == [] :
            self.parent.undo_button.configure(state="disabled")
    
    def start_training(self, event) :
        #
        if not self.is_training_session :
            self.reset_position()
            self.is_training_session = True
            self.parent.start_button.configure(text="Stop training")
        else :
            self.is_training_session = False
            self.parent.start_button.configure(text="Start training")
    
    def play_random_move(self, event=None) :
        print("event is None : ", event is None)
        if event is None :
            self.after(200) #TODO? number of millisec is hardcoded
            # NB: maybe put 300 if we add sounds
            pass
        #
        if self.board.move_lines.current_node == {} :
            print("No more move on the current line.")
        else :
            key_list = list(self.board.move_lines.current_node.keys())
            random_key = key_list[randrange(len(key_list))]
            coords = tuple(int(number) for number in random_key.split(','))
            self.make_computer_move(coords[0], coords[1])
    
    def print_some_stuff(self, event) :
        print("Moves in move_played : ")
        for move in self.board.move_played :
            print(move)
        print("Move lines : ")
        print(self.board.move_lines)
        
    def save_current_move_lines(self, event) : 
        #TODO: add a database_name argument to let the user control it from the gui
        """Save the move lines using MoveRecord.save_new_database."""
        self.board.move_lines.save_new_database()

############ Main ############

class ChessGuiApp(Tk) :
    
    def __init__(self) :
        # Define the window
        Tk.__init__(self)
        self.title("ChessOpy")
        # 
        self.board_gui = BoardGui(self)
        self.board_gui.display_all_pieces()
        self.board_gui.grid(row=0, column=0)
        #
        self.side_canvas = Canvas(self, width=BOARD_SIZE//4, height=BOARD_SIZE, bg='ivory')
        self.side_canvas.grid(row=0, column=1, sticky='ns')
        #
        # self.buttons_canvas = Canvas(self.side_canvas, bg='ivory')
        # self.buttons_canvas.pack(fill=X)
        #
        self.create_buttons()
        #
        # self.display_canvas = Canvas(self.side_canvas, bg='lightgreen')
        # self.display_canvas.pack(expand=True)
        #
        self.display_label= Label(self.side_canvas, text="Bienvenue !", bg='lightgreen')
        self.display_label.pack(expand=True)
    
    def create_buttons(self) :
        #
        self.undo_button = Button(self.side_canvas, text="Undo", state="disabled")
        self.undo_button.bind("<Button-1>", self.board_gui.undo_last_move)
        self.undo_button.pack(fill=X)
        #
        self.start_button = Button(self.side_canvas, text="Start training")
        self.start_button.bind("<Button-1>", self.board_gui.start_training)
        self.start_button.pack(fill=X)
        #
        self.save_button = Button(self.side_canvas, text="Save move lines")
        self.save_button.bind("<Button-1>", self.board_gui.save_current_move_lines)
        self.save_button.pack(fill=X)
        #
        self.play_button = Button(self.side_canvas, text="Play random move")
        self.play_button.bind("<Button-1>", self.board_gui.play_random_move)
        self.play_button.pack(fill=X)

if __name__ == "__main__" :
    root = ChessGuiApp()
    # root.geometry(f'{int(BOARD_SIZE*1.25)}x{BOARD_SIZE}+40+20')
    root.mainloop()
