The  task is to write a python code, for finding square boxes in an image and then place aruco markers exactly overlapping on it with 
the following rules-
box color green - aruco with id 1
box color orange - aruco with id 2
box color black - aruco with id 3
box color pink peach- aruco with id 4


So First i defined a function that returns the angle by which aruco image should be rotated to get straight aruco
Then i defined another function that rotates an aruco image about the center of aruco by an angle to get straight aruco
Then i defined another function that detect the straight aruco in a image and crops the image to get only the image of aruco marker
Then i defined a function that returns the id of the aruco in a image
First i detect the contours of the shapes in the given image,then i detect the square by using the fact they have 4 equal sides
then i get the center of the square dettected by using cv2.moments
then by using if and elif i pasted the desired aruco in the desired square by using cv2.WrapPrespective and cv2.fillConvexPoly
And hence i get the final image