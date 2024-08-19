I_CSN_LOCATION = 0
I_CSN_CONNECTING_LOCATION = 1
I_CSN_DIST = 2

def create_spatial_network(itineraries):
    """ Accepts list of tuples as input with all locations and their
    relationships with other locations and creates a spatial network as a 
    list of all locations with their neighbours and corresponding distances
    """
    
    spatial_network = []
    
    # Making a list of all unique locations in itineraries using set
    all_locations = set()
    for road in itineraries:
        all_locations.add(road[I_CSN_LOCATION])
        all_locations.add(road[I_CSN_CONNECTING_LOCATION])
    unique_locations = sorted(list(all_locations))
    
    # Using list of unique locations to find all neighbouring locations by
    # finding all tuples where the location exists (i.e. has a relationship)
    # and adding information to spatial network
    for location in unique_locations:
        neighbours = []
        for road in itineraries:
            if location in road:
                if road[I_CSN_LOCATION] == location:
                    neighbours.append((road[I_CSN_CONNECTING_LOCATION], 
                                       road[I_CSN_DIST]))
                elif road[I_CSN_CONNECTING_LOCATION] == location:
                    neighbours.append((road[I_CSN_LOCATION], road[I_CSN_DIST]))
        neighbours = sorted(sorted(neighbours), key=lambda x: int(x[1]))
        spatial_network.append((location, neighbours))
    return(spatial_network)