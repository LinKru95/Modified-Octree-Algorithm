class OctreeNode:
    def __init__(self, min_corner, size):
        self.min_corner = min_corner
        self.size = size
        self.children = []
        self.center = self.calculate_center_coordinates()

    def calculate_center_coordinates(self):
        center_x = self.min_corner[0] + self.size[0] / 2
        center_y = self.min_corner[1] + self.size[1] / 2
        center_z = self.min_corner[2] + self.size[2] / 2
        
        return (center_x, center_y, center_z)

def create_initial_octree_root(bounding_box):
    min_corner, max_corner = bounding_box
    root_min_corner = min_corner
    root_size = (max_corner[0] - min_corner[0], max_corner[1] - min_corner[1], max_corner[2] - min_corner[2])
    root_node = OctreeNode(root_min_corner, root_size)

    return root_node