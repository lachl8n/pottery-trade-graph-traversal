# This line imports provided implementations to previous questions
from reference import shortest_path, create_social_network

I_TRADE_TRADER = 0
I_TRADE_LOCATION = 1
I_TRADE_SUPPLY = 2
I_TRADE_DIST = 3

I_TRADE_LOCATION_NAME = 0
I_TRADE_LOCATION_NEIGHBOURS = 1

I_TRADE_NEIGHBOUR_NAME = 0
I_TRADE_NEIGHBOUR_DIST = 1

I_TRADE_CURR_LOCATION = 0
I_TRADE_CURR_DEMAND = 1

I_TRADE_STATUS_LOCATION = 0
I_TRADE_STATUS_SUPPLY = 1

I_TRADE_CONNECTING_TRADERS = 1

NO_UNITS = 0

def find_trader(location, trader_locations):
    """ Accepts a location and searches for its corresponding trader in the
    dictionary of traders and their locations, returning this trader if found
    """
    # Searches through all trader locations to find if the location has a
    # trader, returning nothing if not 
    for (key, value) in trader_locations.items():
        if value == location:
            return key
    return

def find_location(trader, trader_locations):
    """ Accepts a trader and searches for its corresponding location in the 
    dictionary of traders and their locations, returning the location if found
    """
    # Finds corresponding location for a given trader name
    for (key, value) in trader_locations.items():
        if key == trader:
            return value
    return

def find_connections(trader, trader_network):
    """ Accepts a trader and finds its direct connections within the trader
    network, returning its connections if found
    """
    # Finds the direct connections of a trader using the trader name in the
    # trader network
    for connection in trader_network:
        if connection[I_TRADE_TRADER] == trader:
            return connection[I_TRADE_CONNECTING_TRADERS]
    return

def find_supply(location, status_sorted):
    """ Accepts a location and finds its corresponding supply or demand,
    returning the relevant supply if found
    """
    # Finds the supply or demand of a given location in the sorted list of 
    # statuses
    for status in status_sorted:
        if status[I_TRADE_STATUS_LOCATION] == location:
            return status[I_TRADE_STATUS_SUPPLY]
    return

def find_neighbours(target_location, spatial_network):
    """ Accepts a location and finds its corresponding neighbours according to
    the spatial network
    """
    # Finding list of neighbours with their distances in the spatial network
    # using a given location name
    for location in spatial_network:
        location_name = location[I_TRADE_LOCATION_NAME]
        if location_name == target_location:
            location_neighbours = location[I_TRADE_LOCATION_NEIGHBOURS]
            return location_neighbours
    return

def validate_dist_per_unit(distance, units, max_dist_per_unit):
    """ Accepts distance, units and maximum distance per units to validate
    whether the distance per units value exceeds the defined maximum
    """
    # Determines if the distance per unit exceeds the maximum bound defined
    # in the function call
    if (distance / units) > max_dist_per_unit:
        return False
    else:
        return True

def trade(spatial_network, status_sorted, trader_locations, trader_network, 
          max_dist_per_unit=3):
    """ For the location with the highest demand, finds the trade of lowest
    distance-per-unit value
    """
    curr_location = ''
    curr_demand = NO_UNITS

    # Finding the location of highest demand that has a trader
    for i in range(len(status_sorted) + 1):
        # If the iterator is at the end of the list of location statuses,
        # there are no valid trades that can be carried out
        if i >= len(status_sorted):
            return (None, None, None)
        
        # Search for a trader using the location currently selected in the
        # iteration and save the location and demand if a trader exists
        curr_trader = find_trader(status_sorted[i][I_TRADE_CURR_LOCATION], 
                                  trader_locations)
        if curr_trader:
            curr_location = status_sorted[i][I_TRADE_CURR_LOCATION]
            curr_demand = status_sorted[i][I_TRADE_CURR_DEMAND]

            # Find traders that have direct connections to the current trader
            # and move to the next if there are none
            curr_trader_connections = find_connections(curr_trader, 
                                                       trader_network)
            if not curr_trader_connections:
                continue
            
            # If the current trader has direct connections, there must be at
            # least one with supply to be valid, otherwise skip to next trader
            no_valid_traders = True
            for connection in curr_trader_connections:
                connection_location = find_location(connection, 
                                                    trader_locations)
                if not connection_location:
                    continue

                supply = find_supply(connection_location, status_sorted)
                if not supply:
                    continue
                elif supply > NO_UNITS:
                    no_valid_traders = False
                    break
            if no_valid_traders:
                continue
            break
    
    # Make list of trade options from the connecting traders of the trader
    # at the consumer location
    valid_traders = []
    for connection in curr_trader_connections:
        # Find the location for each connecting trader 
        connection_location = find_location(connection, trader_locations)
        if not connection_location:
            continue

        # Identify whether the supplier location is directly neighbouring by
        # a single adjacent road by testing if the location of the connecting
        # trader is a neighbour of the consumer location
        curr_location_neighbours = find_neighbours(curr_location, 
                                                   spatial_network)
        if not curr_location_neighbours:
            continue
        
        # If the directly connected trader is a neighbour of the consumer
        # location, the direct distance is recorded. Otherwise, the shortest
        # distance between the two locations is found with unbound maximum
        connection_is_neighbour = False
        for neighbour in curr_location_neighbours:
            if neighbour[I_TRADE_NEIGHBOUR_NAME] == connection_location:
                connection_is_neighbour = True
                connection_path = curr_location + '-' + connection_location
                connection_distance = (connection_path, 
                                       neighbour[I_TRADE_NEIGHBOUR_DIST])
                break
        if not connection_is_neighbour:
            connection_distance = shortest_path(spatial_network, curr_location, 
                                                connection_location, None)
        if not connection_distance:
            continue

        # Find the supply of the particular location and only add it to the
        # list of valid trade options if it has a positive supply
        supply = find_supply(connection_location, status_sorted)
        if not supply or supply <= NO_UNITS:
            continue
        elif supply > NO_UNITS:
            valid_traders.append((connection, connection_location, supply, 
                                  connection_distance[1]))

    
    # Finding trade option with the highest supply and testing if it is under 
    # the maximum distance per unit
    max_trade = (valid_traders[0][I_TRADE_TRADER], 
                 valid_traders[0][I_TRADE_LOCATION], 
                 valid_traders[0][I_TRADE_SUPPLY], 
                 valid_traders[0][I_TRADE_DIST])
    valid_dist_per_unit = validate_dist_per_unit(max_trade[I_TRADE_DIST], 
                                                 max_trade[I_TRADE_SUPPLY], 
                                                 max_dist_per_unit)
    max_units = valid_traders[0][I_TRADE_SUPPLY]
    # If there is more than one valid trade option, find the one with the 
    # greatest supply
    if len(valid_traders) > 1:
        for trade in valid_traders[1:]:
            if trade[I_TRADE_SUPPLY] > max_units:
                if validate_dist_per_unit(trade[I_TRADE_DIST], 
                                          trade[I_TRADE_SUPPLY], 
                                          max_dist_per_unit):
                    valid_dist_per_unit = True
                    max_trade = (trade[I_TRADE_TRADER], 
                                 trade[I_TRADE_LOCATION], 
                                 trade[I_TRADE_SUPPLY], trade[I_TRADE_DIST])
                    max_units = trade[I_TRADE_SUPPLY]
    # After the valid trade of maximum units is found, find how many items can
    # be supplied by the supplier location and display trade. If there are no
    # valid trade options, return an empty tuple
    if not valid_dist_per_unit:
        trade_output = (None, None, None)
    else:
        # If there is greater demand than supply, the trade can only give the
        # supply of the supplier location. If there is greater supply than
        # demand, the entire demand request can be met
        if abs(max_trade[I_TRADE_SUPPLY]) - abs(curr_demand) < 0:
            units_supplied = max_trade[I_TRADE_SUPPLY]
        else:
            units_supplied = abs(curr_demand)
        
        trade_output = (max_trade[I_TRADE_LOCATION], curr_location, 
                        units_supplied)
    return(trade_output)