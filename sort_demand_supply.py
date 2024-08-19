I_SDS_SUPPLY = 1

def sort_demand_supply(status):
    """ Accepts dictionary of supply and demand status for each location and
    sorts them from highest demand to highest supply, with identical statuses
    sorted alphanumerically
    """
    # Sorts a list of alphanumerically sorted locations by their demand/supply
    # with highest demand at the start and highest supply at the end
    return sorted(sorted(status.items()), key=lambda x: x[I_SDS_SUPPLY])