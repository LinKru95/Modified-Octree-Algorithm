import glob
import laspy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from utils import calculate_bounding_box, add_child_nodes, split_cube, filter_points_for_node
from octree import create_initial_octree_root

las_files = glob.glob("*.las")

if len(las_files) == 0:
    print("No .las files found in the current directory.")
else:
    las_file_path = las_files[0]

with laspy.open(las_file_path, mode="r") as las_file:
    las = las_file.read()
    x_values = las.x
    y_values = las.y
    z_values = las.z

points = list(zip(x_values, y_values, z_values))
points = points[::1000]
bounding_box = calculate_bounding_box(points)
root_octree_node = create_initial_octree_root(bounding_box)
add_child_nodes(root_octree_node, split_cube)
points = filter_points_for_node(root_octree_node, points)
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