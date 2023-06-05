import json

from tube.components import Station
from tube.components import Line
from tube.components import Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def zone_set(self, zone_string):
        """
        Generates the relevant set of zones for a station.

        Args: 
            zone_string (str) : zone of the station. Could end in .5 meaning the station belongs to 2 zones.

        Returns:
            station_zone (set[int]) : zones of the station.
        """
        station_zone = set()
        # Check if zone set is two zones.
        if(zone_string.endswith(".5")):
            # Add the two relevent zones to the set.
            zone = int(zone_string[0])
            station_zone = {zone, zone+1}
        else:
            # Otherwise add the zone to the set.
            station_zone = {int(zone_string)}
        return station_zone

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` attributes should be updated.

        You can use the `json` python package to easily load the JSON file at `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.

        Returns:
            None
        """
        # Load data from the filepath.
        try:
            with open(filepath, "r") as jsonfile:
                map_data = json.load(jsonfile)
        except:
            return

        # Assign map stations.
        map_stations = map_data["stations"]
        for station in map_stations:
            # Get the zone set.
            station_zone = self.zone_set(station["zone"])
            # Create station.
            new_station = Station(station["id"], station["name"], station_zone)
            # Add to station dictionary.
            self.stations[new_station.id] = new_station

        # Assign map lines.
        map_lines = map_data["lines"]
        for line in map_lines:
            # Create line.
            new_line = Line(line["line"], line["name"])
            # Add to line dictionary.
            self.lines[new_line.id] = new_line

        # Assign map connections.
        map_connections = map_data["connections"]
        for connection in map_connections:
            # Get stations and put in a set.
            station_1 = self.stations[connection["station1"]]
            station_2 = self.stations[connection["station2"]]
            stations = {station_1, station_2}
            # Create connection.
            new_connection = Connection(stations, self.lines[connection["line"]], int(connection["time"]))
            # Add to connections list.
            self.connections.append(new_connection)
        return


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
