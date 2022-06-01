from PathFinder.container import Container
from PathFinder.route import Route


class PathFinder:

    def __init__(self, file_path, first_node_id, target_node_id):
        self.file_path = file_path
        self.container = Container(self)
        self.container.importer(self.file_path)

        self.first_node = self.container.get_node_by_id(first_node_id)
        self.target_node = self.container.get_node_by_id(target_node_id)

        self.routes = []
        self.visited_nodes = []

        self.completed_routes = []
        self.completed_routes_len = 0
        self.arrived_routes = []

        self.last_route_id = 1
        self.current_node = self.first_node
        self.current_route = self.new_route()

        self.removed_node = 0
        self.debug = False
        self.debug_node_id = 0

    def p(self, text):
        if self.debug:
            print(text)

    def print_route_path(self, route, prefix="---------------  ->", disabled=True):
        result = prefix
        if not disabled:
            for node in route.get_path():
                result += " " + str(node.id)
            self.p(result)

    def get_route_id(self):
        temp = self.last_route_id
        self.last_route_id += 1
        return temp

    def new_route(self, copy: Route = None):
        route = Route(self)
        if copy is not None:
            route.set_distance(copy.get_distance())
            route.copy_path_of_route(copy)
        else:
            route.add_node_to_path(self.first_node)
            route.set_last_visited_node(self.first_node)
        self.routes.append(route)
        return route

    def set_current_route(self, route):
        self.current_route = route

    def add_new_node(self, node):
        if node in self.visited_nodes:
            self.visited_nodes.append(node)

    def set_route_completed(self, route):
        route.set_completed()
        if route in self.routes:
            self.routes.remove(route)
        if route not in self.completed_routes:
            self.completed_routes.append(route)

    def set_route_arrived(self, route):
        route.set_arrived()
        if route in self.routes:
            self.routes.remove(route)
        if route not in self.arrived_routes:
            self.arrived_routes.append(route)

    def get_first_node(self, edges):
        for e in edges:
            return e, edges[e]

    def division(self, route):
        return self.new_route(route)

    def remove_route(self, route, reason):
        route.remove_reason = reason
        self.set_route_completed(route)

    def move(self, from_node, to_node, route):
        if route.is_node_exist(from_node):
            if not route.loop_check(to_node):
                distance = from_node.get_distance_to_node(to_node)
                route.move(to_node, distance)
                to_node.route_arrived(route)
                if to_node == self.target_node:
                    self.set_route_arrived(route)
                return to_node
            else:
                self.p(f"\u001b[31;1m    << ROUTE SET COMPLETED {from_node.id} to {to_node.id}  R= {route.id} >> \u001b[0m")
                self.set_route_completed(route)
        else:
            print("CRUTUAL ERROR! FROM NODE DOES NOT EXIST!")

    def run(self):
        iteration = 1
        while len(self.routes) > 0:
            self.p(f"\n\n<<<<< ITERATION {iteration} >>>>>")

            self.set_current_route(self.routes[-1])
            self.current_node = self.current_route.get_last_visited_node()
            edges = self.current_node.get_edges()
            edge_len = len(edges)

            if self.debug_node_id == self.current_node.id:
                a = 14
                b = a

            if edge_len == 0:
                # Completed
                self.set_route_completed(self.current_route)
            elif edge_len == 1:
                to_node, distance = self.get_first_node(edges)
                self.p(f"\u001b[34;1m << DIRECT MOVE {self.current_node.id} to {to_node.id} R= {self.current_route.id} >> \u001b[0m")
                self.move(self.current_node, to_node, self.current_route)
            else:
                i = 1
                for to_node in edges:
                    if i == edge_len:
                        self.p(f"\u001b[34;1m << THEN MOVE {self.current_node.id} to {to_node.id}  R= {self.current_route.id} >> \u001b[0m")
                        self.move(self.current_node, to_node, self.current_route)
                    else:
                        route = self.division(self.current_route)
                        self.p(f"\u001b[31m << DIVISION and MOVE of {self.current_node.id} to {to_node.id}  R= {route.id} >> \u001b[0m")
                        self.move(self.current_node, to_node, route)
                    i += 1
            if iteration % 20000 == 0:
                self.completed_routes_len += len(self.completed_routes)
                for i in self.completed_routes:
                    del i
                self.completed_routes = []
                self.p(f"     IT: {iteration} Route: {len(self.routes)} Removed: {self.completed_routes_len} Visited Node: {len(self.visited_nodes)} Last Node: {self.current_node.id}")

            iteration += 1

        self.p(f"\u001b[35;1m << ALL ROUTES: {len(self.routes)} ENDED: {len(self.completed_routes)} ARRIVED: {len(self.arrived_routes)} >> \u001b[0m")

        minimum = 999_999_999
        for i in self.arrived_routes:
            if i.get_distance() < minimum:
                minimum = i.get_distance()
        for i in self.arrived_routes:
            if i.get_distance() == minimum:
                self.print_route_path(i, '----->', False)
                self.p(i.get_distance())
        return minimum
