from typing import List

class Block:
    def __init__(self, position, color,):
        self.position = position
        self.color = color
    
    def __str__(self) -> str:
        return f"color: {self.color} \n position: {self.position}"
        
class Piece:
    def __init__(self, position: tuple[int, int], is_solid: bool):
        assert all(isinstance(coord, int) for coord in position), "Both position coordinates must be integers"
        assert isinstance(position, tuple) and len(position) == 2, "Position must be a tuple of two integers"
        
        self.position = position
        self.is_solid = is_solid

class Shape:
    def __init__(self, piece_list: List[Piece], color: str):
        self.piece_list = piece_list
        self.color = color
        self.blocks = self.create_blocks()

    def create_blocks(self):
        blocks = []
        for piece in self.piece_list:
            if piece.is_solid:
                block = Block(piece.position, self.color)
                blocks.append(block)
        return blocks
    
    def move(self):
        
        
class Car(Shape):
    def __init__(self, color):
        pieces_car = [Piece((0, 1), True), Piece((0, 3), True), Piece((1, 0), True),
                      Piece((1, 1), True), Piece((1, 2), True), Piece((1, 3), False),
                      Piece((2, 1), True), Piece((2, 3), True)]
        super().__init__(pieces_car, color)
        
class Kerbs(Shape):
    def __init__(self, color):
        pieces_kerbs = [Piece((0, 1), False), Piece((0, 2), True), Piece((0, 3), True),
                       Piece((0, 4), True), Piece((0, 5), False)]
        super().__init__(pieces_kerbs, color)

# shape = Shape([Piece((1,0), True), Piece((1,1), True), Piece((1,2), True), Piece((0,0), False)], "orange")
# ref = "0"
# for i in range(3):
#     for j in range(3):
#         for block in shape.blocks:
#             if(block.position[0] == i and block.position[1] == j):
#                 ref = "x"
#         print(ref, end="")
#         ref = "0"
#     print('\n')
            
# print("------------")

# for i in range(3):
#     for j in range(3):
#         for piece in shape.piece_list:
#             if(piece.position[0] == i and piece.position[1] == j):
#                 ref = "x"
#         print(ref, end="")
#         ref = "0"
#     print('\n')