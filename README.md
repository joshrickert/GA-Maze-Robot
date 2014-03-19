# GA Maze Robot
*Created by Josh Rickert for CSE 231 at Michigan State University, Spring 2010*

*Updated for Python 3.4.0*

This script uses a genetic algorithm to teach a 'robot' to navigate a 'maze' (provided by a text file). The robot has a location, facing, and sensor values. It can move forward, left or right. Each robot has a Braitenberg matrix genome that parses its sensor input into instructions to move. The successful robot will follow a breadcrumb trail 'b' to a goal point 'F'.

## Instructions
Load main.py and run runGA() from the console.

The default parameters for the simulation are optimized for a successful navigation. To demonstrate the effectiveness of the algorithm, decrease the starting population, offspring population size, or other parameters to produce a stupider result.

## Algorithm:
Three main classes:

1. GA() maintains the population of individuals and simulates their interactions.
2. Individual() represents a single individual and an instance of its environment.
3. World() is imported and represents the environmental simulation for a single individual.

During the simulation, for each generation:

1. Create the offspring by choosing fit parents and crossing their genes
2. Mutate the offspring at user-determined rates
3. Add the offspring to the main population
4. Kill off the weakest members of the population
5. Output the strongest member of the population

## Legend for World Display
* 'b' is a breadcrumb
* 'x' is a wall
* 'A' is an agent
* '-' is an empty space
* '=' is the robot's path
* 'F' is the finish spot