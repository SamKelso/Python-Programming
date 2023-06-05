from tube.map import TubeMap

class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """
        graph = dict()
        # Check for valid argument.
        if(not isinstance(tubemap, TubeMap)):
            return graph
        # Iterate through stations to find their neighbours.
        for station_id in tubemap.stations.keys():
            station_neighbours_dict = dict()
            # Iterate through tubemap connections to find ones including current station.
            for connection in tubemap.connections:
                # Create list of the station ids for current connection.
                connection_ids = []
                for station in connection.stations:
                    connection_ids.append(station.id)
                # Check if the current station is in the connection.
                if(station_id in connection_ids):
                    # Remove the current station leaving just the neighbouring station.
                    connection_ids.remove(station_id)
                    neighbour_station_id = connection_ids[0]
                    # Add the connection to the graph. Check if the neighbour station has already been added due to another connection.
                    if(neighbour_station_id in station_neighbours_dict.keys()):
                        station_neighbours_dict[neighbour_station_id].append(connection)
                    else:
                        station_neighbours_dict[neighbour_station_id] = [connection]
            # Add the station neighbour connections to the graph.
            graph[station_id] = station_neighbours_dict
        return graph


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph['110'])


if __name__ == "__main__":
    test_graph()
