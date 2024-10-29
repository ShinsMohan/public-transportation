# bus_route_management.py

class Bus:
    def __init__(self, bus_id, route_name, driver_name):
        self.bus_id = bus_id
        self.route_name = route_name
        self.driver_name = driver_name
        self.stops = []

    def add_stop(self, stop_name, arrival_time):
        """Add a stop to the bus route with an expected arrival time."""
        self.stops.append({"stop": stop_name, "arrival_time": arrival_time})

    def show_schedule(self):
        """Display the full schedule for the bus route."""
        print(f"Route: {self.route_name} (Bus ID: {self.bus_id})")
        print(f"Driver: {self.driver_name}")
        print("Stops:")
        for stop in self.stops:
            print(f"  - {stop['stop']} at {stop['arrival_time']}")

class PublicTransportation:
    def __init__(self):
        self.buses = []

    def add_bus(self, bus):
        """Add a new bus to the transportation system."""
        self.buses.append(bus)

    def find_bus_by_route(self, route_name):
        """Search for buses based on the route name."""
        for bus in self.buses:
            if bus.route_name == route_name:
                return bus
        return None

    def display_all_routes(self):
        """Show all available routes."""
        print("Available Bus Routes:")
        for bus in self.buses:
            print(f"- {bus.route_name}")

# Sample usage
if __name__ == "__main__":
    system = PublicTransportation()

    # Create a new bus with route and driver information
    bus1 = Bus(bus_id="B101", route_name="Route A", driver_name="John Doe")
    bus1.add_stop("Central Station", "08:00 AM")
    bus1.add_stop("City Mall", "08:30 AM")
    bus1.add_stop("Airport", "09:00 AM")

    bus2 = Bus(bus_id="B102", route_name="Route B", driver_name="Jane Smith")
    bus2.add_stop("Downtown", "09:00 AM")
    bus2.add_stop("University", "09:30 AM")
    bus2.add_stop("Museum", "10:00 AM")

    # Add buses to the public transportation system
    system.add_bus(bus1)
    system.add_bus(bus2)

    # Display all available routes
    system.display_all_routes()

    # Search and show the schedule for a specific route
    route_name = "Route A"
    bus = system.find_bus_by_route(route_name)
    if bus:
        print(f"\nSchedule for {route_name}:")
        bus.show_schedule()
    else:
        print(f"No bus found for route: {route_name}")
