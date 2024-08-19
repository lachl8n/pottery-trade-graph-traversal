I_CSN_TRADER = 0
I_CSN_CONNECTING_TRADER = 1

def create_social_network(traders):
    """ Accepts list of tuples as input and creates a social network as a 
    list of all traders with their direct connections between each other to
    indicate which traders can trade with one another
    """
    social_network = []
    
    # Making a list of all unique traders in traders by creating a set of 
    # all traders with relationships
    all_traders = set()
    for connection in traders:
        all_traders.add(connection[I_CSN_TRADER])
        all_traders.add(connection[I_CSN_CONNECTING_TRADER])
    unique_traders = sorted(list(all_traders))
    
    # Using list of unique traders to find all direct connection by
    # finding all tuples where the trader exists (i.e. has a connection)
    # and adding connection to social network
    for trader in unique_traders:
        direct_connections = []
        for connection in traders:
            if trader in connection:
                if connection[I_CSN_TRADER] == trader:
                    connecting_trader = connection[I_CSN_CONNECTING_TRADER]
                    direct_connections.append(connecting_trader)
                elif connection[I_CSN_CONNECTING_TRADER] == trader:
                    connecting_trader = connection[I_CSN_TRADER]
                    direct_connections.append(connecting_trader)
        social_network.append((trader, sorted(direct_connections)))
    return(sorted(social_network))