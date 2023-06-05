from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        
        # Feel free to add anything else needed here.

    def station_id_from_name(self, station_name):
        """
        Finds the id of a station from the station name.

        Args:
            station_name (str) : Name of the station.
        
        Returns:
            id (str) : ID of the station.
        """
        # Loop through all station ids.
        for id in self.tubemap.stations.keys():
            # Check if the station name matches.
            if(self.tubemap.stations[id].name == station_name):
                return id
        return None


    def initialise_dist_dict(self, start_station_name):
        """
        Initialises a dictionary with all the station ids as keys. Each key value
        is a nested dictionary containing the distance from the starting station (Infinity for
        non starting stations).

        Args:
            start_station_name (str) : name of starting station of path.
        
        Returns:
            dist_dict (dict) : initialised dictionary in required form.
        """
        dist_dict = dict()
        # Get the starting station id.
        start_station_id = self.station_id_from_name(start_station_name)
        # Iterate through all the station ids.
        for station_id in self.tubemap.stations.keys():
            if(station_id == start_station_id):
                # Case 1: Starting station, duration set to 0 from starting station.
                station_info = {'duration' : 0, 'from' : station_id}
                dist_dict[station_id] = station_info
            else:
                # Case 2: Other station, duration set to infinity from None.
                station_info = {'duration' : float('inf'), 'from' : None}
                dist_dict[station_id] = station_info
        return dist_dict

    def next_station(self, dist_dict, checked_stations):
        '''
        Function to find the next station in the list to check.

        Args:
            dist_dict (dict) : dictionary with information for stations and duration from starting station.
            checked_stations list[str] : stations ids that have already been checked.
        
        Returns:
            next_station (str) : id of the next station to be checked, has the shortest duration at current stage
                                of checking.
        '''
        # Initialise shortest distance as infinity.
        shortest_duration = float('inf')
        # Initialise next station as None.
        next_station = None
        # Iterate through all station ids.
        for station_id in dist_dict.keys():
            # Check that the station hasn't been checked and its duration is less than shortest duration found so far.
            if(not station_id in checked_stations and dist_dict[station_id]['duration'] < shortest_duration):
                # Update shortest duration found and the next station to check.
                shortest_duration = dist_dict[station_id]['duration']
                next_station = station_id
        return next_station


    def reverse_iterate_route(self, dist_dict, start_station_id, end_station_id):
        '''
        Reverse iterates through the route creating a list of the stations along the shortest path.

        Args:
            dist_dict (dict) : complete dictionary of all stations and their relevant durations and previous stations on
                                their path.
            start_station_id (str) : id of starting station of path.
            end_station_id (id) : id of end station of path.

        Returns:
            shortest_path list[Station] : resulting shortest path of stations based from the input dist_dict.
        '''
        # Initialise list by adding the end station.
        shortest_path = [self.tubemap.stations[end_station_id]]
        # Track the next station in the path.
        next_station_in_path = end_station_id
        # Loop until the start station is reached.
        while(next_station_in_path != start_station_id):
            # Update the next station in the path.
            next_station_in_path = dist_dict[next_station_in_path]['from']
            # Add the next station to the path list.
            shortest_path.append(self.tubemap.stations[next_station_in_path])
        # Reverse the path list so it is in the correct order.
        shortest_path.reverse()
        return shortest_path



        
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path (in terms of duration) from start_station_name to end_station_name.

        For instance, get_shortest_path('Stockwell', 'South Kensington') should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.

        You can use the Dijkstra algorithm to find the shortest path from start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not exist.
        """
        # Get the end station id.
        end_station_id = self.station_id_from_name(end_station_name)
        # Get the start station id.
        start_station_id = self.station_id_from_name(start_station_name)
        # Check valid input.
        if(end_station_id is None or start_station_id is None):
            return None
        # Initialise the list of distances from start station.
        dist_dict = self.initialise_dist_dict(start_station_name)
        # Track the stations we have checked.
        checked_stations = []
        # Loop until all the stations have been checked.
        while(len(checked_stations) < len(dist_dict.keys())):
            # Get the station id of next station to check.
            current_station_id = self.next_station(dist_dict, checked_stations)
            # Get the neighbours of current station.
            station_neighbours = self.graph[current_station_id]
            # Loop through neighbour stations.
            for neighbour_station_id in station_neighbours.keys():
                # Initialise shortest duration as infinity.
                shortest_time = float('inf')
                # Loop through possible connections to neighbour station and find shortest connection.
                for connection in station_neighbours[neighbour_station_id]:
                    if(connection.time < shortest_time):
                        shortest_time = connection.time
                # Add the shortest connection time to the time to the previous station.
                duration_current_station = dist_dict[current_station_id]['duration'] + shortest_time
                # Check if this path to the neighbour station is the shortest found so far.
                if(duration_current_station < dist_dict[neighbour_station_id]['duration']):
                    # Update the path dictionary with the new step in the path.
                    dist_dict[neighbour_station_id]['duration'] = duration_current_station
                    dist_dict[neighbour_station_id]['from'] = current_station_id
            # Add the current station to checked stations.
            checked_stations.append(current_station_id)
        # Find the final path by reverse iterating from the end station.
        shortest_path = self.reverse_iterate_route(dist_dict, start_station_id, end_station_id)
                
        return shortest_path 


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
