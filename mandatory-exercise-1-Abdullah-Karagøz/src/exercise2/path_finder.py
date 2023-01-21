from utils import duckietown, visualize_path

def minimum_battery_consumption(grid, h = 0, w = 0, first_time = True, memo = list()):

    # TODO: find out the minimum percentage of battery needed to reach the charging station 
    # if the value at grid[i][j] is negative then it is an obstacle
    # otherwise it is the battery consumption (in percentage) required to traverse the cell
    # the starting position for Donald is grid[0][0] and the goal position is grid[height-1][width-1]
    
    # If the function runs first time we initialize the height h and width w and size of the memo.
    # Memo is as big as the grid.
    if first_time: 
        h = len(grid)-1  # h is heigth
        w = len(grid[0])-1 # w is width
        memo = [[-2] * (w+1) for _ in range(h+1)]
    
    # We start from the goal and move backwards to the start moving North and West, finding least-cost
    # to each nodes along the way, using recursion with memoization. We save least cost data in a 
    # 2D array named "memo". At the end we return the memo.
    
    # This is for security, to avoid potential errors
    if (h < 0 or w < 0):
        return float('Inf')
    # All empty values in memo are marked with -2, if it's empty then we calculate it.
    if memo[h][w] == -2:
        # Negative values are obstacles, so we mark them as having infinite costs
        if grid[h][w] < 0:
            memo[h][w] = float('Inf')
        # Start node
        elif (w == 0 and h == 0):
            memo[h][w] = grid[h][w]
        # It's on far West, so no more to move to West
        elif w == 0:
            memo[h][w] = grid[h][w] + minimum_battery_consumption(grid, h-1, w, False, memo)[h-1][w]
        # It's on far North, so no more to move to North
        elif h == 0:
            memo[h][w] = grid[h][w] + minimum_battery_consumption(grid, h, w-1, False, memo)[h][w-1]
        else:
            # we choose the least cost between "from north" and "from west".
            memo[h][w] = grid[h][w] + min(minimum_battery_consumption(grid, h-1, w, False, memo)[h-1][w], 
                                          minimum_battery_consumption(grid, h, w-1, False, memo)[h][w-1])
    
    
    return memo
    



def least_battery_consuming_path(grid, cost):

    # TODO: find the optimal sequence of actions {'East', 'South'} to reach the charging station
    
    # We have now 2D array showing costs. The code below is just to go backwards (North and West) and
    # choose the least cost each time.
    path = list()
    
    h = len(cost) - 1  # h is heigth
    w = len(cost[0]) - 1 # w is width
    
    cost_array = list()
    
    
    # We move to West and North to draw the path
    while h > 0 and w > 0:
        if cost[h-1][w] < cost[h][w-1]:
            path.append('South')
            h -= 1
        else:
            path.append('East')
            w -= 1
    
    # We are on the far West side, so we move just to North
    while h > 0:
        path.append('South')
        h -= 1
    
    # We are on far North side, so we just move to West
    while w > 0:
        path.append('East')
        w -= 1
    
    
    path.reverse()
    return path
    
    
if __name__ == '__main__':

    # properties of the grid
    height = 30
    width = 50
    obstacles_file = 'obstacles.txt'

    # constructs the grid and initializes cell values
    grid = duckietown(height, width, obstacles_file)
    
    #grid = [[1,2,-1], [4,8,2], [7,5,3]]
    
    # path finding algorithm using dynamic programming
    
    cost = minimum_battery_consumption(grid)

    path = least_battery_consuming_path(grid, cost)

    # sets the speed of Donald to a number between 1 and 10 (fastest = 10)
    donald_speed = 10

    # visualizes the path
    visualize_path(grid, path, donald_speed)
    
    print(cost[-1][-1])

