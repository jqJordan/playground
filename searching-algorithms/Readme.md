## search.py
#### Implemetation of Breadth First Search, AStar, Recursive Breadth First Search.

#### Search with Heuristics
H(n) = (M(0, 0) + M(180, 180) + M(90, 0) + M(90, 90) + M(90, 180)) / 4

`python search.py <ALG> <File>`

Where ALG is one of: "BFS", "AStar", "RBFS". And FILE is the puzzle file name.

#### Coordinates of the Globe 
- Longitude 0/180: (0◦, 0◦), (30◦, 0◦), (60◦, 0◦), (90◦, 0◦), (120◦, 0◦), (150◦, 0◦), (180◦, 180◦), (150◦, 180◦), (120◦, 180◦), (90◦, 180◦), (60◦, 180◦), (30◦, 180◦)
- Longitude 90/270: (0◦, 0◦), (30◦, 90◦), (60◦, 90◦), (90◦, 90◦), (120◦, 90◦), (150◦, 90◦), (180◦, 180◦), (150◦, 270◦), (120◦, 270◦), (90◦, 270◦), (60◦, 270◦), (30◦, 270◦)
- Equator: (90◦, 0◦), (90◦, 30◦), (90◦, 60◦), (90◦, 90◦), (90◦, 120◦), (90◦, 150◦), (90◦, 180◦), (90◦, 210◦), (90◦, 240◦), (90◦, 270◦), (90◦, 300◦), (90◦, 330◦)

#### puzzle file
Tile(30-180, (90,270), Exact(30,180))

This specifies a single tile. In this case we have a tile with ID "30-180" that is currently at latitude and longitude (90,270) and which has an exact target coordinates of latitude and longitude (30,180) to match. A puzzle is complete when all of its tiles are at their target locations.

## NQueens.py

The N-queens problem is a classical constraint problem where the goal is to determine where queens can be placed on an n ∗ n chessboard such that no two queens threaten the other.

`NQueens.py ALG N CFile RFile`

where: ALG is one of FOR or MAC representing Backtracking search with forward checking or Maintaining
Arc Consistency respectively. N represents the number of rows and columns in the chessboard as well as the
number of queens to be assigned. CFile is an output filename for your constraint problem. And RFile is an
output file for your results.
