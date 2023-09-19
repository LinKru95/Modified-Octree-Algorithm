import laspy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from utils import calculate_bounding_box, add_child_nodes, split_cube, filter_points_for_node
from octree import create_initial_octree_root

max_depth = 1

with laspy.open("2743_1234.las", mode="r") as las_file:
    las = las_file.read()
    x_values = las.x
    y_values = las.y
    z_values = las.z

points = list(zip(x_values, y_values, z_values))
points = points[::10000]
print("Number of points:", len(points))
bounding_box = calculate_bounding_box(points)
root_octree_node = create_initial_octree_root(bounding_box)
# points = [point for point in points if is_point_inside_node(point, root_octree_node)]
add_child_nodes(root_octree_node, split_cube)
points = filter_points_for_node(root_octree_node, points)
# print("Number of points:", len(points))
# points = points[::10000]
print("Number of points:", len(points))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x_filtered = [point[0] for point in points]
y_filtered = [point[1] for point in points]
z_filtered = [point[2] for point in points]

ax.scatter(x_filtered, y_filtered, z_filtered, c='b', marker='.')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Filtered 3D Point Cloud')

plt.show()

# print("Bounding Box:")
# print("Min Corner:", bounding_box[0])
# print("Max Corner:", bounding_box[1])
# print("Root Node Position:", root_octree_node.min_corner)
# print("Root Node Size:", root_octree_node.size)

# def print_octree(node, depth=0):
#     print("Node Depth:", depth)
#     print("Node Min Corner:", node.min_corner)
#     print("Node Size:", node.size)
#     print("Node Center:", node.center)
#     print("Node Children Count:", len(node.children))
    
#     for child in node.children:
#         print_octree(child, depth + 1)

# print_octree(root_octree_node)










