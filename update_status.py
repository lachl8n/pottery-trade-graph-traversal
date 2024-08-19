# This line imports provided implementations to previous questions
from reference import trade, sort_demand_supply

NO_ITERATIONS = 0
INFINITY = float('inf')
I_ITER_TRADE_SUPPLIER = 0
I_ITER_TRADE_CONSUMER = 1
I_ITER_TRADE_SUPPLY = 2

def update_status(trade, status):
    """ Accepts a trade and dictionary of locations with their respective
    supply/demand status and changes values in accordance with the trade
    """
    # Updates the values of the status dictionary using the supply given and 
    # received in the trade 
    for (key, value) in status.items():
        if key == trade[I_ITER_TRADE_SUPPLIER]:
            status[key] -= trade[I_ITER_TRADE_SUPPLY]
        elif key == trade[I_ITER_TRADE_CONSUMER]:
            status[key] += trade[I_ITER_TRADE_SUPPLY]
    return status

def trade_iteratively(num_iter, spatial_network, status, trader_locations, 
                      trader_network, max_dist_per_unit=3):
    """ Accepts the maximum iterations, the spatial network, supply/demand of 
    each location, the locations of traders, the connections between traders 
    and the maximum distance per unit the trader can travel and iteratively 
    finds all trades until the max iterations and returns the updated 
    supply/demand of locations and all trades that occurred
    """
    trades = []
    all_trades_complete = False
    
    # If the maximum iterations is not specified, it is unbounded (infinite)
    if not num_iter:
        num_iter = INFINITY
    
    # Trades between locations iteratively until all possible valid trades are
    # complete or until the maximum iterations have been reached
    while not all_trades_complete:
        if num_iter <= NO_ITERATIONS:
            all_trades_complete = True
        else:
            status_sorted = sort_demand_supply(status)
            curr_trade = trade(spatial_network, status_sorted, 
                               trader_locations, trader_network, 
                               max_dist_per_unit)
            
            # Valid trades are added to the list of trades. No trade returned 
            # indicates all possible trades have been exhausted and halts
            # iteration
            if curr_trade != (None, None, None):
                trades.append(curr_trade)
            else:
                all_trades_complete = True
                continue
            
            # Update the status dictionary in preparation for the next
            # iteration and move towards termination via decrementing max 
            # iterations
            num_iter -= 1
            status = update_status(curr_trade, status)
            status.update()
    
    # Returns the final supply and demand values and all trades that occurred
    final_supply_sorted = sort_demand_supply(status)
    return(final_supply_sorted, trades)
