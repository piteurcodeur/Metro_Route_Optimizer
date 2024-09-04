# Metro Route Optimizer  

## Description  

This project is a metro route planner application that allows users to input their itinerary and obtain the corresponding route information. The application is developed in **Python** with a graphical user interface using **Tkinter**.

## Installation  

To install this project, follow these steps:

Clone the Git repository: git clone https://github.com/piteurcodeur/Metro_Route_Optimizer.git  
Install the dependencies: pip install -r requirements.txt  
Run the GUI.py file: python GUI.py

## Usage  

To use the application, follow these steps:

Launch the application by running the **GUI.py** file.  
Enter your city, start station, and end station in the corresponding fields.
Click the **"Search"** button to obtain the route information.
The application will display the itinerary with the corresponding route information, including the lines and stations.

## Code  

The code is organized into several parts:

1. The **MasterGraphe** class represents the graph of metro stations and . calculates the shortest route.
2. The GUI part uses Tkinter to create the graphical user interface.
3. The chemin function finds the shortest route between two stations.
4. The find_itineraire function retrieves the itinerary with the corresponding route information.

## Graph Search Algorithm  

The graph search algorithm used in this project is **Dijkstra's algorithm**, which finds the shortest path between two nodes in a graph. The algorithm is implemented in the **"chemin"** function.

## Dependencies  

### This project depends on the following libraries:

- Tkinter for the graphical user interface
- PIL for image manipulation
- difflib for string matching


## License

This project is under the [MIT License](https://github.com/piteurcodeur/Metro_Route_Optimizer?tab=MIT-1-ov-file). You can use and modify the code according to the terms of the license.
