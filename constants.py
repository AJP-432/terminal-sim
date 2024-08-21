import math
from enum import Enum

class MapEdges(Enum):
    TOP_RIGHT = 0
    TOP_LEFT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class UnitType(Enum):
    WALL = 0
    SUPPORT = 1
    TURRET = 2
    SCOUT = 3
    # DEMOLISHER = 4
    # INTERCEPTOR = 5
    # REMOVE = 6
    # UPGRADE = 7   

ARENA_SIZE = 28
HALF_ARENA = 14

def is_in_bounds(loc: tuple[int, int]) -> bool:
    """Checks if the given location is inside the diamond shaped game board.

    Args:
        location: A map location

    Returns:
        True if the location is on the board, False otherwise
    
    """
    x, y = loc
    half_board = HALF_ARENA                                                     

    row_size = y + 1
    startx = half_board - row_size
    endx = startx + (2 * row_size) - 1
    top_half_check = (y < HALF_ARENA and x >= startx and x <= endx)

    row_size = (ARENA_SIZE - 1 - y) + 1
    startx = half_board - row_size
    endx = startx + (2 * row_size) - 1
    bottom_half_check = (y >= HALF_ARENA and x >= startx and x <= endx)

    return bottom_half_check or top_half_check

def get_quadrant(loc: tuple[int, int]) -> MapEdges:
    """"
    Gets the quadrant of the map that a location is in
    """
    x, y = loc
    if x < ARENA_SIZE // 2 and y < ARENA_SIZE // 2:
        return MapEdges.BOTTOM_LEFT
    if x >= ARENA_SIZE // 2 and y < ARENA_SIZE // 2:
        return MapEdges.BOTTOM_RIGHT
    if x >= ARENA_SIZE // 2 and y >= ARENA_SIZE // 2:
        return MapEdges.TOP_RIGHT
    if x < ARENA_SIZE // 2 and y >= ARENA_SIZE // 2:
        return MapEdges.TOP_LEFT

def get_edge_locations(quadrant: MapEdges) -> list[tuple[int, int]]:
    return get_edges()[quadrant.value]

def end_edge_locations(quadrant: MapEdges) -> list[tuple[int, int]]:
    if quadrant == MapEdges.TOP_RIGHT:
        return get_edges()[MapEdges.BOTTOM_LEFT.value]
    if quadrant == MapEdges.TOP_LEFT:
        return get_edges()[MapEdges.BOTTOM_RIGHT.value]
    if quadrant == MapEdges.BOTTOM_LEFT:
        return get_edges()[MapEdges.TOP_RIGHT.value]
    if quadrant == MapEdges.BOTTOM_RIGHT:
        return get_edges()[MapEdges.TOP_LEFT.value]

def get_edges() -> list[list[tuple[int, int]]]:
    """Gets all of the edges and their edge locations

    Returns:
        A list with four lists inside of it of locations corresponding to the four edges.
        [0] = top_right, [1] = top_left, [2] = bottom_left, [3] = bottom_right.
    """
    # assume 0,0 is bottom left
    top_right = []
    for num in range(0, HALF_ARENA):
        x = HALF_ARENA + num
        y = ARENA_SIZE - 1 - num
        top_right.append([int(x), int(y)])
    top_left = []
    for num in range(0, HALF_ARENA):
        x = HALF_ARENA - 1 - num
        y = ARENA_SIZE - 1 - num
        top_left.append([int(x), int(y)])
    bottom_left = []
    for num in range(0, HALF_ARENA):
        x = HALF_ARENA - 1 - num
        y = num
        bottom_left.append([int(x), int(y)])
    bottom_right = []
    for num in range(0, HALF_ARENA):
        x = HALF_ARENA + num
        y = num
        bottom_right.append([int(x), int(y)])
    return [top_right, top_left, bottom_left, bottom_right]

def distance_between_locations(loc_1: tuple[int, int], loc_2: tuple[int, int]) -> float:
    """Euclidean distance

    Args:
        location_1: An arbitrary location, [x, y]
        location_2: An arbitrary location, [x, y]

    Returns:
        The euclidean distance between the two locations

    """
    x1, y1 = loc_1
    x2, y2 = loc_2

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distance_to_closest_edge(x: int, y: int) -> float:
    """Calculates the distance from a location to the closest edge"""
    quadrant = get_quadrant(x, y)
    edge_locations = get_edge_locations(quadrant)
    min_distance = float("inf")
    for edge_location in edge_locations:
        distance = distance_between_locations((x, y), edge_location)
        min_distance = min(min_distance, distance)
    return min_distance

def get_locations_in_range(location: tuple[int, int], radius: float) -> list[tuple[int, int]]:
    """Gets locations in a circular area around a location

    Args:
        location: The center of our search area
        radius: The radius of our search area

    Returns:
        The locations that are within our search area

    """
    if not is_in_bounds((location[0], location[1])):
        raise IndexError("Location out of bounds")

    x, y = location
    locations = []
    search_radius = math.ceil(radius)
    getHitRadius = 0.01 #from the configs
    for i in range(int(x - search_radius), int(x + search_radius + 1)):
        for j in range(int(y - search_radius), int(y + search_radius + 1)):
            new_location = (i, j)
            # A unit with a given range affects all locations whose centers are within that range + get hit radius
            if is_in_bounds((new_location[0], new_location[1])) and distance_between_locations(location, new_location) < radius + getHitRadius:
                locations.append(new_location)
    return locations