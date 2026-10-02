#  AI-Based Emergency Route Finder

### Simulated Road Network Emergency Navigation System

An AI-based emergency route-finding application that demonstrates **Greedy Best-First Search (GBFS)** for selecting a goal-directed route from an emergency location to a hospital.

The system uses a **simulated road network** and a **Euclidean distance heuristic** to decide which road node appears closest to the selected hospital.

> **Note:** This is an educational AI project. It uses a simulated road network and does not provide real-time GPS, live traffic information, or real-world emergency navigation.

---

##  Problem Statement

During an emergency, reaching a hospital quickly is important. A navigation system needs to decide which route to explore when multiple roads are available.

This project demonstrates how an AI search algorithm can make this decision using **Greedy Best-First Search**.

Instead of exploring the road network blindly, the algorithm uses a heuristic to estimate how close each location is to the destination hospital and prioritizes the location that appears closest to the goal.

---

##  Objective

The main objectives of this project are:

* To understand **informed search** in Artificial Intelligence.
* To implement **Greedy Best-First Search**.
* To use **Euclidean distance as a heuristic function**.
* To find a goal-directed route through a simulated road network.
* To visualize the nodes explored during the search.
* To calculate the total distance of the selected route.
* To understand the difference between a fast goal-directed search and an optimal shortest-path algorithm.

---

##  AI Concept Used

### Greedy Best-First Search

Greedy Best-First Search is an **informed search algorithm** that selects the node that appears closest to the goal according to a heuristic.

The evaluation function used in this project is:

**f(n) = h(n)**

Where:

* `f(n)` = evaluation value of the node
* `h(n)` = estimated distance from the current node to the destination

The algorithm does **not** consider the accumulated distance already travelled.

Therefore, it can reach a destination quickly but **does not guarantee the shortest possible route**.

---

##  Heuristic Function

This project uses **Euclidean distance** between two nodes.

```text
h(n) = √((x₂ - x₁)² + (y₂ - y₁)²)
```

The coordinates of the road locations are used to estimate their straight-line distance from the selected hospital.

For example:

```text
Accident Spot → Hospital
```

The algorithm calculates the heuristic value for available neighbouring nodes and prioritizes the node with the smaller heuristic value.

---

##  Simulated Road Network

The project contains a manually defined road network consisting of:

* Accident Spot
* Junction A
* Junction B
* Junction C
* Junction D
* Hospital A
* Hospital B

Each road connection contains an associated distance.

Example:

```text
Accident Spot
     ├── Junction A
     └── Junction B
```

The network is represented as a graph containing **nodes and weighted connections**.

---

##  How the System Works

The overall process is:

```text
Select Emergency Location
          ↓
Select Destination Hospital
          ↓
Calculate Heuristic h(n)
          ↓
Greedy Best-First Search
          ↓
Select Node Closest to Goal
          ↓
Explore the Road Network
          ↓
Reach Hospital
          ↓
Display Selected Route
          ↓
Calculate Route Distance
```

---

##  Search Process

The algorithm maintains a priority-based frontier.

For every available neighbouring node:

1. Calculate its heuristic value.
2. Compare the heuristic values.
3. Prioritize the node with the smallest `h(n)`.
4. Explore that node.
5. Continue until the destination hospital is reached.

The application also records the **exploration sequence**, allowing the user to observe how the AI searched through the network.

---

##  Application Features

### 1. Emergency Location Selection

The user can select an emergency location from the available road nodes.

### 2. Hospital Selection

The user can select either:

* Hospital A
* Hospital B

as the destination.

### 3. AI Route Finding

The application runs Greedy Best-First Search to find a route from the selected starting point to the selected hospital.

### 4. Route Distance

After finding the route, the system calculates the total distance travelled along the selected path.

### 5. Exploration Sequence

The application displays the order in which nodes were explored by the algorithm.

### 6. Heuristic Table

The application displays:

* Location
* Heuristic value `h(n)`
* Whether the node belongs to the final path
* Whether the node was explored

### 7. Visual Road Network

Different node states are visually represented:

* Emergency location
* Hospital
* Selected route
* Explored node
* Normal road node

---

##  Technologies Used

* **Python**
* **Streamlit**
* **Heap-based Priority Queue**
* **Mathematical Euclidean Distance**
* **Graph Representation**
* **Greedy Best-First Search**

---

##  System Architecture

```text
User Input
   ↓
Emergency Location + Hospital
   ↓
Simulated Road Network
   ↓
Euclidean Heuristic
   ↓
Greedy Best-First Search
   ↓
Explored Nodes
   ↓
Final Route
   ↓
Distance Calculation
   ↓
Streamlit Visualization
```

---

##  Example Output

The application provides:

```text
Emergency Route Found Successfully

Path Distance: XX.X km
Nodes Explored: X
Algorithm: Greedy BFS
```

It also displays the selected route in the form:

```text
Accident Spot → Junction A → Junction C → Hospital A
```

along with the exploration sequence and heuristic table.

---

##  Limitations

The current system is a simulation designed to demonstrate an AI search algorithm.

It does not currently include:

* Real-time GPS
* Live traffic conditions
* Dynamic road closures
* Real road maps
* Real-time ambulance location
* Weather conditions
* Traffic congestion
* Emergency vehicle priority
* Multiple real-world hospitals
* Live hospital availability

Most importantly, **Greedy Best-First Search does not guarantee the shortest route**, because it considers only the heuristic `h(n)` and ignores the accumulated path cost.

---

##  Future Improvements

The project can be extended into a more realistic emergency navigation system.

### 1. Real Map Integration

Replace the simulated road network with real geographical road data.

### 2. GPS Integration

Use the actual ambulance or emergency vehicle location as the starting point.

### 3. Real-Time Traffic

Include traffic congestion when calculating route costs.

### 4. Dynamic Routing

Allow the system to recalculate the route when roads become blocked or traffic conditions change.

### 5. A* Search

A future version can use **A* Search**, which combines:

```text
f(n) = g(n) + h(n)
```

where:

* `g(n)` = actual cost from the start node
* `h(n)` = estimated cost to the goal

This can provide a more cost-aware search compared with the current greedy approach.

### 6. Emergency Priority

The system could consider ambulance priority, road accessibility, and emergency severity.

### 7. Hospital Information

The destination selection could consider hospital availability, emergency department capacity, and distance.

---

##  What This Project Demonstrates

This project demonstrates how an AI agent can make a **goal-directed decision under a search problem**.

The main learning is:

> **Greedy Best-First Search uses heuristic information to move toward the goal quickly, but the route it finds is not necessarily the shortest route.**

The project therefore provides a practical visualization of:

```text
Graph Representation
        +
Heuristic Search
        +
Greedy Decision Making
        +
Path Finding
        +
Visualization
```

---

##  Author

**Muthu Subalakshmi S**

Second Year
B.Tech Artificial Intelligence and Data Science
National Engineering College
