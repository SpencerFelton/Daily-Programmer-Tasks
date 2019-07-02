NORTH = (0,1)
NORTHEAST = (1,1)
EAST = (1,0)
SOUTHEAST = (1,-1)
SOUTH = (0,-1)
SOUTHWEST = (-1,-1)
WEST = (-1,0)
NORTHWEST = (-1,1)

def find_smaller_blobs(current_blob, blob_list):
    """
    Given a blob, find any smaller blobs.
    If no blobs are smaller, find any equal size blobs.
    Returns a list of tuples.
    """
    potent_blobs = []
    current_blob_weight = current_blob[2]
    for blobs in blob_list:
        if blobs[2] < current_blob_weight: #Look for any blobs smaller than the current one
            potent_blobs.append(blobs)

    if len(potent_blobs) == 0: # If theres no blobs smaller, look for an equal size one
        for blobs in blob_list:
            if blobs == current_blob:
                continue
            if blobs[2] == current_blob_weight:
                potent_blobs.append(blobs)
    return potent_blobs

def find_closest_blob(current_blob, potent_blobs):
    """
    Given a blob and list of potential blobs, find the closest blob. Clockwise biased. Favours blobs closest in size to itself.
    Returns a tuple.
    """
    if potent_blobs == []:
        return ([current_blob[0], current_blob[1], current_blob[2]], 0)
    dist = []
    poss_blob = []
    current_pos = (current_blob[0], current_blob[1])
    curr_size = current_blob[2]
    for blobs in potent_blobs:
        blob_pos = (blobs[0],blobs[1])
        x_diff, y_diff = blob_pos[0] - current_pos[0], blob_pos[1] - current_pos[1] #x and y differences
        if x_diff < 0: #convert distances to positive values
            x_diff *= -1
        if y_diff < 0:
            y_diff *= -1

        steps = 0
        while x_diff + y_diff != 0:
            if x_diff > 0 and y_diff > 0: # move diagonally
                x_diff -= 1
                y_diff -= 1
                steps += 1
            elif x_diff == 0 and y_diff > 0: # move vertically
                y_diff -= 1
                steps += 1
            elif x_diff > 0 and y_diff == 0: # move horizontally
                x_diff -= 1
                steps += 1
        dist.append([blobs,steps])

    min_dist = min(i[1] for i in dist) # find the minimum distance

    poss_blob_dist = []
    for blobs in dist:
        if blobs[1] == min_dist: # find all blobs with the same distance as the minimum
            poss_blob_dist.append(blobs[0])

    blob_sizes = []
    for blobs in poss_blob_dist: # obtain size if all blobs at mimimum dist
        blob_sizes.append(blobs[2])


    largest_blob = max(set(blob_sizes)) # find the size of the largest blob at minimum dist

    poss_blob = []
    for blobs in poss_blob_dist: # only consider blobs of largest size and minimum dist
        if blobs[2] == largest_blob:
            poss_blob.append(blobs)

    # find closest blob clockwise
    blob_diffs = []
    for blobs in poss_blob:
            x_diff = blobs[0] - current_blob[0]
            y_diff = blobs[1] - current_blob[1]
            blob_diffs.append([blobs, x_diff, y_diff])

    clockwise_blobs= []
    for x in range(0, 4): # loop over 4 quarters of a circle (12 - 12)
        if x == 0:
            for blob in blob_diffs:
                if blob[1] >= 0 and blob[2] >= 0:
                    clockwise_blobs.append(blob)
            if len(clockwise_blobs) != 0:
                clockwise_blobs.append(0) # indicator for 12-3
                break
        if x == 1:
            for blob in blob_diffs:
                if blob[1] >= 0 and blob[2] <= 0:
                    clockwise_blobs.append(blob)
            if len(clockwise_blobs) != 0:
                clockwise_blobs.append(1) # indicator for 3-6
                break
        if x == 2:
            for blob in blob_diffs:
                if blob[1] <= 0 and blob[2] <= 0:
                    clockwise_blobs.append(blob)
            if len(clockwise_blobs) != 0:
                clockwise_blobs.append(2) # indicator for 6-9
                break
        if x == 3:
            for blob in blob_diffs:
                if blob[1] <= 0 and blob[2] >= 0:
                    clockwise_blobs.append(blob)
                clockwise_blobs.append(3) # indicator for 9-12

    quarter_value = clockwise_blobs[len(clockwise_blobs)-1] # tells us which quarter we're working in
    closest_blob = []

    if quarter_value == 0: # find the blob with smallest x value ie closest to 12
        for blobs in clockwise_blobs:
            if(blobs == 0): # ignore the quarter value
                continue
            if len(closest_blob) == 0:
                closest_blob.append(blobs[0]) # if it's the first blob, append to list
            else:
                if blobs[0][0] < closest_blob[0][0]: # if the current blob is closer than the previous closest blob, replace it
                    closest_blob[0] = blobs[0]
                if blobs[0][0] == closest_blob[0][0]: # if the current blob has the same xvalue than the previous closest blob, check for largest y value
                    if blobs[0][1] > closest_blob[0][1]:
                        closest_blob[0] = blobs[0]

    if quarter_value == 1: # find the blob with the largest y value ie closest to 3, y value here is -ve so we use >
        for blobs in clockwise_blobs:
            if(blobs == 1):
                continue
            if len(closest_blob) == 0:
                closest_blob.append(blobs[0]) # if it's the first blob, append to list
            else:
                if blobs[0][1] > closest_blob[0][1]: # if the current blob is closer than the previous closest blob, replace it
                    closest_blob[0] = blobs[0]
                if blobs[0][1] == closest_blob[0][1]: # if the current blob has the same y value as the previous closest blob, check for the largest x value
                    if blobs[0][0] > closest_blob[0][0]:
                        closest_blob[0] = blobs[0]

    if quarter_value == 2: # find the blob with largest x value ie closest to 6. x values here are -ve, so we use >
        for blobs in clockwise_blobs:
            if(blobs == 2):
                continue
            if len(closest_blob) == 0:
                closest_blob.append(blobs[0]) # if it's the first blob, append to list
            else:
                if blobs[0][0] > closest_blob[0][0]: # if the current blob is closer than the previous closest blob, replace it
                    closest_blob[0] = blobs[0]
                if blobs[0][0] == closest_blob[0][0]: # if the current blob has the same x value as the previous closest blob, check for the smallest (most -ve) y value
                    if blobs[0][1] < closest_blob[0][1]:
                        closest_blob[0] = blobs[0]

    if quarter_value == 3: # find the blob with the smallest y value ie closest to 9
        for blobs in clockwise_blobs:
            if(blobs == 3):
                continue
            if len(closest_blob) == 0:
                closest_blob.append(blobs[0]) # if it's the first blob, append to list
            else:
                if blobs[0][1] < closest_blob[0][1]: # if the current blob is closer than the previous closest blob, replace it
                    closest_blob[0] = blobs[0]
                if blobs[0][1] == closest_blob[0][1]: # if the current blob has the same y value as the previous closest blob, check for the smallest (most -ve) x value
                    if blobs[0][0] < closest_blob[0][0]:
                        closest_blob[0] = blobs[0]
    return(closest_blob)

def move_to_blob(current_blob, closest_blob, update_coord_matrix):
    """
    Finds the difference in coordinates between two blobs. Updates the new blob position into another list.
    Returns a list.
    """
    curr_blob_x, curr_blob_y = current_blob[0], current_blob[1]
    clos_blob_x, clos_blob_y = closest_blob[0][0], closest_blob[0][1]

    x_diff = clos_blob_x - curr_blob_x
    y_diff = clos_blob_y - curr_blob_y

    direction = (0,0)

    if x_diff == 0 and y_diff > 0:
        direction = NORTH

    if x_diff > 0 and y_diff > 0:
        direction = NORTHEAST

    if x_diff > 0 and y_diff == 0:
        direction = EAST

    if x_diff > 0 and y_diff < 0:
        direction = SOUTHEAST

    if x_diff == 0 and y_diff < 0:
        direction = SOUTH

    if x_diff < 0 and y_diff < 0:
        direction = SOUTHWEST

    if x_diff < 0 and y_diff == 0:
        direction = WEST

    if x_diff < 0 and y_diff > 0:
        direction = NORTHWEST


    updated_pos = (current_blob[0] + direction[0], current_blob[1] + direction[1], current_blob[2])
    update_coord_matrix.append(updated_pos)
    return(update_coord_matrix)

def merge(blob_list):
    merge_list = []
    for blobs in range(0, len(blob_list)):
        merge_coords = []
        for merge_blobs in merge_list:
            x,y = merge_blobs[0], merge_blobs[1]
            merge_coords.append([x,y])
        if [blob_list[blobs][0],blob_list[blobs][1]] in merge_coords:
            continue
        merge_list.append(list(blob_list[blobs])) # add current blob to list to merge
        for other_blobs in range(0, len(blob_list)): # consider the other blobs
            if blob_list[other_blobs] == blob_list[blobs]: # if it's the same blob, ignore it
                continue
            if blob_list[other_blobs][0] == blob_list[blobs][0] and blob_list[other_blobs][1] == blob_list[blobs][1]:
                merge_list[blobs][2] += blob_list[other_blobs][2]
    return(merge_list)


if __name__ == '__main__':
    #x = [(0,2,1),(2,1,2),(0,0,1)]
    """test = [(0,0,3),
            (-1,0,1),
            (1,0,1),
            (-1,-1,1),
            (1,-1,1),
            (0,-1,1),
            (0,1,1),
            (1,1,1),
            (-1,1,1)]"""
    #test = [(0,0,3), (2,1,1)]
    test = [(-289429971, 243255720, 2),
 (2368968216, -4279093341, 3),
 (-2257551910, -3522058348, 2),
 (2873561846, -1004639306, 3)]
    update_coord_matrix = []
    #y = x.copy()
    #y.remove(x[1])
    #test_copy = test.copy()
    #test_copy.remove(test[1])
    while len(update_coord_matrix) != 1:
        update_coord_matrix = [] # use two lists, one for calculating movement and one for storing the movement
        for blobs in range(0, len(test)):
            pot = find_smaller_blobs(test[blobs], test)
            closest_blob = find_closest_blob(test[blobs], pot)
            move_to_blob(test[blobs], closest_blob, update_coord_matrix)
        update_coord_matrix = merge(update_coord_matrix)
        test = update_coord_matrix.copy()
    print(update_coord_matrix)
    #pot = find_smaller_blobs(x[1], y)
    #find_closest_blob(x[1], pot)
