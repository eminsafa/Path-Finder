class Node:

    def __init__(self, node_id, route_solver):
        self.id = node_id
        self.RS = route_solver

        # edges = { <node> : <int: distance> }
        self.edges = {}
        self.routes = {}

        self.minimum_route = None
        self.prev_distance = 0
        self._minimum_distance = 999_999_999
        self.divided = False

    def add_edge(self, node, distance):
        if node not in self.edges.keys():
            self.edges[node] = distance
        else:
            assert f"EDGE #{node} ALREADY IN THE LIST"

    def remove_edge(self, node):
        if node in self.edges.keys():
            self.edges.pop(node)

    def get_edges(self):
        return self.edges

    def set_minimum_distance(self, distance):
        self._minimum_distance = distance

    def get_minimum_distance(self):
        return self._minimum_distance

    def remove_route_from_node(self, route):
        if route in self.routes:
            self.routes.pop(route)

    def get_distance_to_node(self, node):
        if node in self.edges:
            return self.edges[node]
        else:
            print("CRUTUAL ERROR not in node list")
            return False

    def route_arrived(self, route):

        route_to_remove = []
        if route not in self.routes:
            self.routes[route] = route.get_distance()

        for r in self.routes:
            distance = self.routes[r]
            if self.get_minimum_distance() >= distance:
                self.prev_distance = self.get_minimum_distance()
                self.set_minimum_distance(distance)
                self.minimum_route = r

        for r in self.routes:
            distance = self.routes[r]
            if self.get_minimum_distance() < distance:
                route_to_remove.append(r)

        if len(self.edges) == 1:
            for r in route_to_remove:
                a = 0
                self.RS.remove_route(r, f'Node {self.id} Called')
