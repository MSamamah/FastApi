from typing import Dict, List, Callable
from fastapi import Request

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
        
        # Find the most specific route match
        matched_route = None
        for route_path in self.route_middleware.keys():
            if path == route_path or path.startswith(route_path + "/"):
                # This is a more specific match than what we have
                if matched_route is None or len(route_path) > len(matched_route):
                    matched_route = route_path
        
        if matched_route is not None:
            for group_name in self.route_middleware[matched_route]:
                if group_name in self.middleware_groups:
                    middlewares.extend(self.middleware_groups[group_name])
        
        return middlewares

# Create a global registry instance
registry = MiddlewareRegistry()