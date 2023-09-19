import math
from octree import OctreeNode

def calculate_bounding_box(points):
    # Initialize minimum and maximum coordinates
    min_x = min_y = min_z = float('inf')  # Initialize to positive infinity
    max_x = max_y = max_z = float('-inf')  # Initialize to negative infinity

    # Iterate through the points to find the minimum and maximum coordinates
    for point in points:
        x, y, z = point[0], point[1], point[2]
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

    edge_length = max(max_x - min_x, max_y - min_y, max_z - min_z)
    center_x = (max_x + min_x) / 2
    center_y = (max_y + min_y) / 2
    center_z = (max_z + min_z) / 2
    min_corner_x = center_x - edge_length / 2
    min_corner_y = center_y - edge_length / 2
    min_corner_z = center_z - edge_length / 2
    bounding_cube = ((min_corner_x, min_corner_y, min_corner_z), (min_corner_x + edge_length, min_corner_y + edge_length, min_corner_z + edge_length))
    return bounding_cube

def add_child_nodes(node, split_cube):
    # Split the current cube into child cubes
    child_cubes = split_cube(node)

    # Create child nodes for each cube
    for child_cube in child_cubes:
        child_node = OctreeNode(child_cube.min_corner, child_cube.size)
        node.children.append(child_node)

def split_cube(parent_cube):
    # Extract parent cube information
    parent_min_corner = parent_cube.min_corner
    parent_size = parent_cube.size

    # Calculate the half size of the parent cube
    half_size = (parent_size[0] / 2, parent_size[1] / 2, parent_size[2] / 2)

    # Define the eight child cube positions relative to the parent cube
    child_positions = [
        parent_min_corner,
        (parent_min_corner[0] + half_size[0], parent_min_corner[1], parent_min_corner[2]),
        (parent_min_corner[0], parent_min_corner[1] + half_size[1], parent_min_corner[2]),
        (parent_min_corner[0] + half_size[0], parent_min_corner[1] + half_size[1], parent_min_corner[2]),
        (parent_min_corner[0], parent_min_corner[1], parent_min_corner[2] + half_size[2]),
        (parent_min_corner[0] + half_size[0], parent_min_corner[1], parent_min_corner[2] + half_size[2]),
        (parent_min_corner[0], parent_min_corner[1] + half_size[1], parent_min_corner[2] + half_size[2]),
        (parent_min_corner[0] + half_size[0], parent_min_corner[1] + half_size[1], parent_min_corner[2] + half_size[2]),
    ]

    # Create and return child cubes
    child_cubes = []
    for position in child_positions:
        child_cube = OctreeNode(position, half_size)
        child_cubes.append(child_cube)

    return child_cubes

def is_point_inside_node(point, node):
    x, y, z = point
    min_x, min_y, min_z = node.min_corner
    max_x, max_y, max_z = (node.min_corner[0] + node.size[0], node.min_corner[1] + node.size[1], node.min_corner[2] + node.size[2])

    return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z

def calculate_distance(point1, point2):
    # Calculate the differences in x, y, and z coordinates
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]
    delta_z = point1[2] - point2[2]

    # Calculate the square of the Euclidean distance
    squared_distance = delta_x**2 + delta_y**2 + delta_z**2

    # Take the square root to get the actual distance
    distance = math.sqrt(squared_distance)
    
    return distance

def filter_points_for_node(node, points):
    half_edge_length = min(node.size) / 2
    result = []

    # Create a set to store the indices of points to exclude
    exclude_indices = set()

    # Exclude points that are farther from the node's center than half_edge_length
    for i, point in enumerate(points):
        if calculate_distance(point, node.center) > half_edge_length:
            exclude_indices.add(i)

    # Exclude points that are closer to any child node's center than half_edge_length
    for child_node in node.children:
        for i, point in enumerate(points):
            if calculate_distance(point, child_node.center) > (half_edge_length / 2) and is_point_inside_node(point, child_node):
                exclude_indices.add(i)

    # Append points to result list that are not in the exclude_indices set
    result.extend(point for i, point in enumerate(points) if i not in exclude_indices)

    return result