# Basics of ROS

### To Launch
1. Make sure to source your setup files, this must be done with each new shell. The command is "source /path/setup.bash" or "source /opt/ros/humble/setup.bash". The "humble" part can be changed based off which version you're using.

In order to do this automatically, use the command 'echo "same command" >> ~/.bashrc'

### Random Commands I Guess?
To check the executables, "ros2 pkg executables *pkg_name*"
To run an executable, the command is "ros2 run *pkg_name* *executable*"

### ROS Nodes
The ROS2  Graph is a series of black boxes, each node controls a single thing (eg moving specific motors or sending sensor data)