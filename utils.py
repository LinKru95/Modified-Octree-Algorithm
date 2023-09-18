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

    # Return the bounding box as a tuple of two points: (min_corner, max_corner)
    bounding_box = ((min_x, min_y, min_z), (max_x, max_y, max_z))
    return bounding_box

def add_child_nodes_to_depth(node, max_depth, current_depth, split_cube):
    if current_depth >= max_depth:
        return

    # Split the current cube into child cubes
    child_cubes = split_cube(node)

    # Create child nodes for each cube
    for child_cube in child_cubes:
        child_node = OctreeNode(child_cube.min_corner, child_cube.size)
        node.children.append(child_node)

        # Recursively add child nodes for the next level
        add_child_nodes_to_depth(child_node, max_depth, current_depth + 1, split_cube)

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