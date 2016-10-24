# mineclearing
Evaluation of Starfleet Academy Mine Clearing Algorithms

# Usage
To run the program:

> python mineclearing.py /path/to/field_file.txt /path/to/script_file.txt

Example files are provided (field1.txt and script1.txt and field2.txt and script2.txt).

> python mineclearing.py in/test_field1.txt in/test_script1.txt
> python mineclearing.py in/test_field2.txt in/test_script2.txt

# Unit Tests
To run unit tests:

> nosetests

# Comments
## Cuboid
The Cuboid class is used to represent a the cross-section view of the minefield.

### Issues Encountered
I tried to design and code everything as cleanly as possible, but I ran into two
big challenges in particular:

1. How to deal with 'improper' user input:
   Very late in the development cycle, I discovered that users were allowed to
   give 'improperly-formatted' cuboid string representations as inputs.

   For example, in one of the examples given in the problem prompt,
   a field file contained the following:
    >..a..
    >.....
    >.....
    >.....
    >..a..

   I had assumed that users would only be given "proper" formats for the field,
   such that it only contains the minimum rows / cols to display the ship at
   the center of the field with all mines in view.

   I was going to leave it up to validators on user input to handle these
   kinds of cases, but not working through the examples carefully really
   cost me.

   Thus, I hastily wrote the `_resize` function at the last minute to handle
   resizing the matrix representing the Cuboid in the event of improper user
   input. This function is not properly optimized / unit tested because of time
   constraints, unfortunately (it does appear to work in functional tests,
   however).

2. How to print the Cuboid such that the ship is centered and all mines are in
   view.

   For the sake of optimization, I decided to not create a new matrix every time
   a move or fire commands updates the matrix. Instead, I went for a 'lazy'
   approach of assembling and printing a new matrix based off of ship and remaining
   mine positions when the user calls the `__str__` function to get a string of the
   Cuboid.

   Doing this approach proved to be difficult to accomplish, as there were
   many variables to keep track of in calculating how many rows and columns would
   be in the string version of the matrix (hence the relatively convoluted code
   for the `__str__` function).

   I played with the idea of calculating the leftmost / rightmost mine positions
   and the topmost / bottommost mine position and keeping track of those positions
   to calculate a the dimensions of the printed matrix. I call these 'boundary'
   positions 'limits' (hence the `get_vert_limits` and `get_hor_limits`
   functions). These x and y 'limits' are used for calculation of the string
   representation row and column sizes).


## Simulation
The Simulation class is used to represent a simulation of a mine-clearing script
running against a minefield.

The design of Simulation was fairly straightforward. I wanted it to be able to
take inputs for both a minefield and a script and then run the script on the
minefield while printing the results.


## If I had more time, I would...
* Give users the option of passing in their own versions of 'fire' and 'move'
  command dictionaries to Simulations. Doing this enhancement would allow for
  greater flexibility and extensibility of the commands that the Simulation can
  interpret. I designed the `__init__` function with this thought in mind and it
  would be fairly simple to add this enhancement.
* Go back and optimize all functions and further clean up the code. `_resize`
  in particular needs serious work in testing and optimization before for I am
  fully confident about using it.
* Do back and do more extensive functional testing. I don't think I was able to
  explore every corner case possible.


## What I would do differently
If I could do this project over again, I would make sure that I thoroughly work
through all examples of user input in detail before proceeding with design.

I would also use numpy arrays instead of normal arrays. I have heard good things
about numpy array performance and a lot of the functions that I was writing were
probably already implemented in numpy.

I would also work out another strategy for printing the matrix than the one that
I ended up with, as well as take some time to research strategies / libraries
that would make this task easier and simpler.
