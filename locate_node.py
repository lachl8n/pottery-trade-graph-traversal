I_SR_PATH_LAST_LOCATION = -1
I_SR_PATH = 0
I_SR_PATH_LENGTH = 1
I_SR_NEIGHBOURS = 1

INFINITY = float('inf')

I_SR_LOCATION_NAME = 0

def locate_node(target_value, spatial_network):
    """ Accepts the target location and the spatial network of locations as a
    list of locations with corresponding neighbours as input and searches 
    through the spatial network to find the location with all information
    """
    # Finds the location in the spatial network to return its neighbours
    # each with their corresponding distances
    for location in spatial_network:
        if location[I_SR_LOCATION_NAME] == target_value:
            return location

def shortest_path(spatial_network, source, target, max_bound):
    """ Accepts the source location, target location, maximum bound and the
    spatial network as as input and finds the shortest distance between the
    source and target locations by compiling a list of all paths where
    locations are visited only once and identifying the path of least distance
    """
    paths_with_target = []
    path = [([source], 0)]
    visited = []
    path_template = []
    end_nodes = []
    
    # Iterating repeatedly through a tree of nodes where each child node
    # represents a neighbour to a location until all paths have been generated
    # and each end with an end node
    while True:
        path_template = path[I_SR_PATH]
        visited = path_template[I_SR_PATH]
        curr_node = locate_node(visited[I_SR_PATH_LAST_LOCATION], 
                                spatial_network)
        neighbours = curr_node[I_SR_NEIGHBOURS]
        path_template = (visited, path_template[I_SR_PATH_LENGTH])
        
        # Compiling list of all paths where the target is found to give
        # options for the shortest path
        if curr_node[I_SR_PATH] == target and \
           path_template not in paths_with_target:
            paths_with_target.append(path_template)
        
        # Creating new pathways for each neighbour that the location has
        # with the corresponding distance subtotal
        search_executed = False
        for neighbour in neighbours:
            if neighbour[I_SR_LOCATION_NAME] not in visited:
                search_executed = True
                new_path = path_template[I_SR_PATH] + \
                           [neighbour[I_SR_LOCATION_NAME]]
                new_distance = path_template[I_SR_PATH_LENGTH] + \
                               neighbour[I_SR_PATH_LENGTH]
                path.append((new_path, new_distance))
            else:
                # Identifying end node by checking if neighbours are visited
                # where an end node is defined as locations whose neighbours
                # are all visited
                has_unvisited_neighbours = False
                for location in neighbours:
                    if location[I_SR_LOCATION_NAME] not in visited:
                        has_unvisited_neighbours = True
                if not has_unvisited_neighbours:
                    end_nodes.append(curr_node[I_SR_LOCATION_NAME])
        
        # Removing and re-appending the node to the end of the path list to
        # allow iteration to continue (always checking the first item)
        if not search_executed:
            path.append(path_template)
        path.remove(path_template)
        
        # Loop terminus condition by determining if all pathways have a
        # concluding end node by iterating through all generated paths
        end_in_end_nodes = []
        for location in path:
            last_location = location[0][I_SR_PATH_LAST_LOCATION]
            if last_location in list(end_nodes):
                end_in_end_nodes.append(True)
            else:
                end_in_end_nodes.append(False)
        # Breaks out of the iteration if all paths end with an end node
        if end_in_end_nodes.count(True) == len(path):
            break
    
    # After all possible pathways have been considered, find the path with
    # the shortest distance by iteratively comparing the distances of all paths
    # where the target is found
    min_path = paths_with_target[0][I_SR_PATH]
    min_path_length = paths_with_target[0][I_SR_PATH_LENGTH]
    for path in paths_with_target:
        # If unspecified, maximum bound is infinite (i.e. the traveller will
        # travel for as long as needed)
        if max_bound is None:
            max_bound = INFINITY
        
        # Skip iteration if the distance exceeds the maximum bound
        if path[I_SR_PATH_LENGTH] > max_bound:
            continue
        
        # Re-assign shortest path length if one exists
        if path[I_SR_PATH_LENGTH] < min_path_length:
            min_path = path[I_SR_PATH]
            min_path_length = path[I_SR_PATH_LENGTH]
        elif path[I_SR_PATH_LENGTH] == min_path_length:
            if len(path[I_SR_PATH]) > len(min_path):
                # If there are paths of the same length, find which visits
                # more locations
                min_path = path[I_SR_PATH]
                min_path_length = path[I_SR_PATH_LENGTH]
            elif len(path[I_SR_PATH]) == len(min_path):
                # If paths have the same distance and same number of 
                # locations, find path of lower alphanumeric value
                if path[I_SR_PATH] < min_path:
                    min_path = path[I_SR_PATH]
                    min_path_length = path[I_SR_PATH_LENGTH]   
    # If the shortest path length is still greater than the maximum bound,
    # there is no solution
    if min_path_length > max_bound:
        return (None, None)
    else:
        shortest_path = '-'.join(min_path)
        shortest_path_and_distance = (shortest_path, min_path_length)
        return shortest_path_and_distance