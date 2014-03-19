
class World(object):
    ''' This class represents a world and an agent (robot). On initialization,
    it reads the world from a text file.
	'b' is a breadcrumb
	'x' is a wall
	'A' is an agent
	'-' is an empty space
	'=' is the robot's path
	'F' is the finish spot

    The robot has a location, facing, and sensor values. It can move forward,
    left or right. '''

    def __init__(self, fname):
        ''' Intialize the world from a file. The agent starts at 1,1, which
        is in the top left of the world. '''
        worldFile = open(fname)
        row = 0
        col = 0

                            

        # for facing 0 is north, 1 is east,
        # 2 is south, and 3 is west
        self.agent_facing = 0
        self.world = []
        for line in worldFile:
            col = 0
            if 'dim' in line:
                rowNum = int(line.split()[1])
                for r in range(0, rowNum):
                    self.world.append([])
                continue
            splitLine = line.split()
            for char in splitLine:
                self.world[row].append(char)
                if (char == "S"):
                    self.agent = (row, col)
                col += 1
                
            row += 1
        self.agent_location = (1,1)
        self.world[1][1] = "#"

    def printWorld(self):
        ''' Print the world in human readable format. '''
        colNum = 0
        rowNum = 0
        for row in self.world:
                colNum = 0
                for char in row:
                        if self.agent_location[0] == rowNum and \
                           self.agent_location[1] == colNum:
                                print 'A \t',
                        else:
                                print char, '\t',
                        colNum += 1
                print '\n'
                rowNum += 1
			

    def queryWorldLocation(self, loc):
            ''' See what is at a location in the world. Where location is a
            coordination tuple (x,y) '''
            if loc[0] < 0 or     \
                    loc[0] > len(self.world[0]) or   \
                    loc[1] < 0 or    \
                    loc[1] > len(self.world):
                            print "Bad query: ", loc[0], " ", loc[1], " is not defined."
                            return "-1"
            else:
                    return self.world[loc[0]][loc[1]]

    def isBreadcrumb(self):
            ''' Check if the agent is on a breadcrumb. Returns true if yes and
            False if no. '''
            
            res = self.queryWorldLocation(self.agent_location)
            if res == "b":
                    self.world[self.agent_location[0]][self.agent_location[1]] = " "
                    return True
            else:
                    return False

    def isDash(self):
            ''' Check if the  agent is on a dash. Returns true if yes and
            False if no. '''
            
            res = self.queryWorldLocation(self.agent_location)
            if res == "-":
                    self.world[self.agent_location[0]][self.agent_location[1]] = " "
                    return True
            else:
                    return False

    def isFinal(self):
            ''' Check if the  agent is on the final spot. Returns true if yes and
            False if no. '''
            
            res = self.queryWorldLocation(self.agent_location)
            if res == "F":
                    self.world[self.agent_location[0]][self.agent_location[1]] = " "
                    return True
            else:
                    return False
    
    def getAgentLocation(self):
            ''' Get the location of the agent'''
            return self.agent_location

    def getAgentFacing(self):
            ''' Get the facing of the agent'''
            return self.agent_facing

    def rotateAgent(self, direction):
            ''' rotate the agent either left or right,
            where 0 is left and 2 is right '''
            if direction == 0:
                    self.agent_facing -= 1
                    if self.agent_facing < 0:
                            self.agent_facing = 3
            elif direction == 2:
                    self.agent_facing += 1
                    if self.agent_facing > 3:
                            self.agent_facing = 0
            return self.agent_facing

    def moveAgent(self, direction):
            ''' Move the agent. The direction values are interpreted as:
            0 - left
            1 - forward
            2 - right '''
            self.world[self.agent_location[0]][self.agent_location[1]] = "#"

            # Direction 0 is left, 1 is forward, 2 is right
            # First adjust facing.
            
            newLocation = self.agent_location
            newFacing = self.rotateAgent(direction)

            # move
            if newFacing == 0:
                    newLocation = (newLocation[0]-1, newLocation[1])
            elif newFacing == 1:
                    newLocation = (newLocation[0], newLocation[1]+1)
            elif newFacing == 2:
                    newLocation = (newLocation[0]+1, newLocation[1])
            elif newFacing == 3:
                    newLocation = (newLocation[0], newLocation[1]-1)
            else:
                    print "Bad direction: ", direction

            if self.queryWorldLocation(newLocation) != "-1" \
               and self.queryWorldLocation(newLocation) != "x" :
                    self.agent_location = newLocation


    def getSensorValues(self):
        ''' Get the agent's sensor values.
        The first list returns 1 if no breadcrumb and2 if breadcrumb.
        The second list returns the actual characters in the world.
        or 2 if a breadcrumb. ''' 
        sensed = [0, 0, 0]
        sensorValues = [1, 1, 1]
        loc = self.agent_location
        if self.agent_facing == 0:
            sensed[0] = self.queryWorldLocation((loc[0], loc[1]-1))
            sensed[1] = self.queryWorldLocation((loc[0]-1, loc[1]))
            sensed[2] = self.queryWorldLocation((loc[0], loc[1]+1))
        elif self.agent_facing == 1:
            sensed[0] = self.queryWorldLocation((loc[0]-1, loc[1]))
            sensed[1] = self.queryWorldLocation((loc[0], loc[1]+1))
            sensed[2] = self.queryWorldLocation((loc[0]+1, loc[1]))
        elif self.agent_facing == 2:
            sensed[0] = self.queryWorldLocation((loc[0], loc[1]+1))
            sensed[1] = self.queryWorldLocation((loc[0]+1, loc[1]))
            sensed[2] = self.queryWorldLocation((loc[0], loc[1]-1))
        elif self.agent_facing == 3:
            sensed[0] = self.queryWorldLocation((loc[0]+1, loc[1]))
            sensed[1] = self.queryWorldLocation((loc[0], loc[1]-1))
            sensed[2] = self.queryWorldLocation((loc[0]-1, loc[1]))

        if sensed[0] == 'b':
            sensorValues[0] = 2
        if sensed[1] == 'b':
            sensorValues[1] = 2
        if sensed[2] == 'b':
            sensorValues[2] = 2
        return sensorValues, sensed



