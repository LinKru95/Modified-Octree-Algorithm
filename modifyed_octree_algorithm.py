import laspy
from utils import calculate_bounding_box, add_child_nodes_to_depth, split_cube
from octree import OctreeNode, create_initial_octree_root

max_depth = 2

with laspy.open("2743_1234.las", mode="r") as las_file:
    las = las_file.read()
    x_values = las.x
    y_values = las.y
    z_values = las.z

points = list(zip(x_values, y_values, z_values))
bounding_box = calculate_bounding_box(points)
root_octree_node = create_initial_octree_root(bounding_box)
add_child_nodes_to_depth(root_octree_node, max_depth, 0, split_cube)

# print("Bounding Box:")
# print("Min Corner:", bounding_box[0])
# print("Max Corner:", bounding_box[1])
# print("Root Node Position:", root_octree_node.min_corner)
# print("Root Node Size:", root_octree_node.size)

# def print_octree(node, depth=0):
#     # Print information about the current node
#     print("Node Depth:", depth)
#     print("Node Min Corner:", node.min_corner)
#     print("Node Size:", node.size)
#     print("Node Children Count:", len(node.children))
    
#     # Recursively print information for child nodes
#     for child in node.children:
#         print_octree(child, depth + 1)

# # Call the print_octree function with the root node
# print_octree(root_octree_node)










