class Route:

    def __init__(self, RS):
        self._distance: int = 0
        self._completed: bool = False
        self._arrived: bool = False
        self._last_visited_node = None

        self._is_division: bool = False
        self._current_node_to_set = None

        self._path = []
        self.RS = RS
        self.id = RS.get_route_id()

        self.remove_reason = ""

    def increase_distance(self, distance):
        self._distance += distance

    def set_completed(self):
        self._completed = True

    def set_arrived(self):
        self.set_completed()
        self._arrived = True

    def set_distance(self, distance):
        self._distance = distance

    def set_last_visited_node(self, node):
        self._last_visited_node = node

    def set_division_status(self, division: bool):
        self._is_division = division

    def set_current_node_to_set(self, node):
        self._current_node_to_set = node

    def is_completed(self) -> bool:
        return self._completed

    def is_arrived(self) -> bool:
        return self._arrived

    def is_division(self) -> bool:
        return self._is_division

    def is_node_exist(self, node):
        return node in self._path

    def get_last_visited_node(self):
        return self._last_visited_node

    def get_path(self):
        return self._path

    def get_distance(self) -> int:
        return self._distance

    def get_current_node_to_set(self):
        return self._current_node_to_set

    def copy_path_of_route(self, route):
        for i in route.get_path():
            self._path.append(i)

    def add_node_to_path(self, node):
        self._path.append(node)

    def loop_check(self, node):
        if node in self._path:
            return True

    def move(self, to_node, distance):
        self._path.append(to_node)
        self.set_last_visited_node(to_node)
        self._distance += distance

