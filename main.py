import sys

from PathFinder.path_finder import PathFinder

file_path = sys.argv[1]
first_node_id = int(sys.argv[2])
target_node_id = int(sys.argv[3])

rs = PathFinder(file_path, first_node_id, target_node_id)
rs.debug = False
minimum_distance = rs.run()
print(minimum_distance)
