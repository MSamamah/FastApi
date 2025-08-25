from typing import Dict, List, Callable

class MiddlewareRegistry:
    def __init__(self):
        self.middleware_groups: Dict[str, List[Callable]] = {}
        self.route_middleware: Dict[str, List[str]] = {}
    
    def register_group(self, name: str, middlewares: List[Callable]):
        self.middleware_groups[name] = middlewares
    
    def assign_to_route(self, route_path: str, groups: List[str]):
        self.route_middleware[route_path] = groups
    
    def get_middlewares_for_route(self, path: str) -> List[Callable]:
        middlewares = []
        
        for route_path, groups in self.route_middleware.items():
            if path.startswith(route_path):
                for group_name in groups:
                    if group_name in self.middleware_groups:
                        middlewares.extend(self.middleware_groups[group_name])
        
        return middlewares

# Create a global registry instance
registry = MiddlewareRegistry()