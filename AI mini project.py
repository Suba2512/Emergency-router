"""
AI-Based Emergency Route Finder Using Greedy Best-First Search
Simulated Road Network Emergency Navigation System
"""

import streamlit as st
import heapq
import math


# ============================================================================== 
# 1. PAGE CONFIGURATION
# ============================================================================== 

st.set_page_config(
    page_title="AI Emergency Route Finder",
    page_icon="🚑",
    layout="wide"
)


# ============================================================================== 
# 2. SIMULATED ROAD NETWORK DATA
# ============================================================================== 

COORDINATES = {
    "Accident Spot": (1.0, 3.0),
    "Junction A": (3.0, 5.0),
    "Junction B": (3.5, 1.5),
    "Junction C": (6.0, 5.5),
    "Junction D": (7.0, 2.0),
    "Hospital A": (9.0, 6.0),
    "Hospital B": (9.0, 1.0)
}

ROAD_NETWORK = {
    "Accident Spot": [
        ("Junction A", 4.0),
        ("Junction B", 3.0)
    ],

    "Junction A": [
        ("Accident Spot", 4.0),
        ("Junction B", 2.5),
        ("Junction C", 4.0)
    ],

    "Junction B": [
        ("Accident Spot", 3.0),
        ("Junction A", 2.5),
        ("Junction D", 4.5)
    ],

    "Junction C": [
        ("Junction A", 4.0),
        ("Junction D", 3.5),
        ("Hospital A", 3.0)
    ],

    "Junction D": [
        ("Junction B", 4.5),
        ("Junction C", 3.5),
        ("Hospital A", 5.0),
        ("Hospital B", 3.0)
    ],

    "Hospital A": [
        ("Junction C", 3.0),
        ("Junction D", 5.0)
    ],

    "Hospital B": [
        ("Junction D", 3.0)
    ]
}


# ============================================================================== 
# 3. HEURISTIC CALCULATION
# ============================================================================== 

def calculate_euclidean_distance(node_a, node_b):
    x1, y1 = COORDINATES[node_a]
    x2, y2 = COORDINATES[node_b]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# ============================================================================== 
# 4. SHORTEST-PATH ROUTE SEARCH
# ============================================================================== 

def greedy_best_first_search(graph, start_node, goal_node):
    """
    A* search using Euclidean distance as the heuristic.
    This keeps the route goal-directed while also minimizing the accumulated travel cost,
    which is essential for emergency response planning.
    """
    if start_node not in graph or goal_node not in graph:
        return None, [], set()

    if start_node == goal_node:
        return [start_node], [start_node], {start_node}

    frontier = []
    counter = 0
    g_costs = {start_node: 0.0}
    came_from = {}
    visited = set()
    explored_sequence = []

    start_h = calculate_euclidean_distance(start_node, goal_node)
    heapq.heappush(frontier, (start_h, 0.0, counter, start_node))

    while frontier:
        _, current_cost, _, current_node = heapq.heappop(frontier)

        if current_node in visited:
            continue

        visited.add(current_node)
        explored_sequence.append(current_node)

        if current_node == goal_node:
            path = []
            node = current_node
            while node is not None:
                path.append(node)
                node = came_from.get(node)
            path.reverse()
            return path, explored_sequence, visited

        for neighbor, edge_cost in graph[current_node]:
            if neighbor in visited:
                continue

            tentative_cost = current_cost + edge_cost
            if tentative_cost < g_costs.get(neighbor, float('inf')):
                g_costs[neighbor] = tentative_cost
                came_from[neighbor] = current_node
                counter += 1
                f_score = tentative_cost + calculate_euclidean_distance(neighbor, goal_node)
                heapq.heappush(frontier, (f_score, tentative_cost, counter, neighbor))

    return None, explored_sequence, visited


# ============================================================================== 
# 5. PATH DISTANCE CALCULATION
# ============================================================================== 

def compute_total_path_distance(graph, path):
    if not path or len(path) < 2:
        return 0.0

    total_distance = 0.0

    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]

        for neighbor, distance in graph[current]:
            if neighbor == next_node:
                total_distance += distance
                break

    return total_distance


# ============================================================================== 
# 6. STREAMLIT ROAD NETWORK VISUALIZATION
# ============================================================================== 

def display_network(graph, coords, start_node, goal_node, final_path=None, explored_nodes=None):
    final_path = final_path or []
    explored_nodes = explored_nodes or []

    node_data = []

    for node in coords:
        if node == start_node:
            icon = "🟢"
            status = "Emergency"
            css_class = "start"
        elif node == goal_node:
            icon = "🔴"
            status = "Hospital"
            css_class = "hospital"
        elif node in final_path:
            icon = "🔵"
            status = "Selected Route"
            css_class = "route"
        elif node in explored_nodes:
            icon = "🟡"
            status = "Explored"
            css_class = "explored"
        else:
            icon = "⚪"
            status = "Road Node"
            css_class = "normal"

        node_data.append(
            f"""
            <div class="node-card {css_class}">
                <div class="node-icon">{icon}</div>
                <div class="node-name">{node}</div>
                <div class="node-status">{status}</div>
            </div>
            """
        )

    st.markdown(
        """
        <style>
        .network-container {
            background: #f7f9fc;
            border: 1px solid #dfe6ee;
            border-radius: 15px;
            padding: 25px;
            margin-top: 10px;
        }
        .network-title {
            text-align: center;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            color: #1f2937;
        }
        .node-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            align-items: center;
        }
        .node-card {
            border-radius: 12px;
            padding: 14px;
            text-align: center;
            background: white;
            border: 2px solid #d1d5db;
            min-height: 105px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .node-card.start {
            border-color: #22c55e;
            background: #f0fdf4;
        }
        .node-card.hospital {
            border-color: #ef4444;
            background: #fef2f2;
        }
        .node-card.route {
            border-color: #3b82f6;
            background: #eff6ff;
        }
        .node-card.explored {
            border-color: #f59e0b;
            background: #fffbeb;
        }
        .node-icon {
            font-size: 28px;
            margin-bottom: 5px;
        }
        .node-name {
            font-weight: 700;
            font-size: 14px;
            color: #1f2937;
        }
        .node-status {
            font-size: 11px;
            color: #6b7280;
            margin-top: 3px;
        }
        .route-display {
            background: #eff6ff;
            border-left: 5px solid #2563eb;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-weight: 600;
        }
        .legend {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
            font-size: 13px;
        }
        </style>
        <div class="network-container">
            <div class="network-title">🗺️ Simulated Road Network</div>
            <div class="node-grid">
        """,
        unsafe_allow_html=True
    )

    for card in node_data:
        st.markdown(card, unsafe_allow_html=True)

    st.markdown(
        """
            </div>
            <div class="legend">
                <span>🟢 Emergency Location</span>
                <span>🔴 Hospital</span>
                <span>🔵 Selected Route</span>
                <span>🟡 Explored Node</span>
                <span>⚪ Normal Road Node</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 🛣️ Road Connections")

    road_rows = []
    seen_edges = set()

    for node, neighbors in graph.items():
        for neighbor, distance in neighbors:
            edge = tuple(sorted([node, neighbor]))
            if edge not in seen_edges:
                seen_edges.add(edge)

                is_route = False
                for i in range(len(final_path) - 1):
                    if (
                        final_path[i] == node and final_path[i + 1] == neighbor
                    ) or (
                        final_path[i] == neighbor and final_path[i + 1] == node
                    ):
                        is_route = True
                        break

                marker = "🔵" if is_route else "⚪"
                road_rows.append(f"{marker} **{node}** ↔ **{neighbor}** — {distance} km")

    columns = st.columns(2)
    for index, road in enumerate(road_rows):
        with columns[index % 2]:
            st.markdown(road)


# ============================================================================== 
# 7. STREAMLIT APPLICATION
# ============================================================================== 

def main():
    st.title("🚑 AI-Based Emergency Route Finder")
    st.subheader("Shortest-Path Emergency Route Planning")
    st.markdown(
        """
        Find the most efficient emergency route through a
        **simulated road network** using
        **A\\* Search with Euclidean distance heuristic**.
        """
    )

    st.warning(
        "⚠️ This application uses a simulated road network for AI algorithm demonstration. It does not provide real-time GPS or traffic navigation."
    )
    st.divider()

    st.sidebar.header("⚙️ Emergency Route Settings")

    available_nodes = list(ROAD_NETWORK.keys())
    hospitals = ["Hospital A", "Hospital B"]
    start_locations = [node for node in available_nodes if node not in hospitals]

    selected_start = st.sidebar.selectbox(
        "Emergency Location",
        options=start_locations,
        index=(start_locations.index("Accident Spot") if "Accident Spot" in start_locations else 0)
    )

    selected_goal = st.sidebar.selectbox(
        "Destination Hospital",
        options=hospitals,
        index=0
    )

    search_button = st.sidebar.button("🚑 Find Emergency Route", type="primary", use_container_width=True)

    if not search_button:
        st.info("👉 Select the emergency location and hospital from the sidebar, then click **Find Emergency Route**.")
        display_network(ROAD_NETWORK, COORDINATES, selected_start, selected_goal)
        return

    if selected_start == selected_goal:
        st.warning("The emergency location and destination hospital cannot be the same.")
        display_network(ROAD_NETWORK, COORDINATES, selected_start, selected_goal)
        return

    path, explored_order, visited_nodes = greedy_best_first_search(ROAD_NETWORK, selected_start, selected_goal)

    if path:
        total_distance = compute_total_path_distance(ROAD_NETWORK, path)
        st.success("✅ Emergency Route Found Successfully!")

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("📏 Path Distance", f"{total_distance:.1f} km")
        metric2.metric("🔍 Nodes Explored", str(len(explored_order)))
        metric3.metric("🧠 Algorithm", "A* Search")

        st.markdown("### 🚑 Selected Emergency Route")
        route_text = " ➜ ".join(path)
        st.markdown(f"""
        <div class="route-display">
            {route_text}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔍 Exploration Sequence")
        exploration_text = " ➜ ".join([f"{index + 1}. {node}" for index, node in enumerate(explored_order)])
        st.info(exploration_text)

        display_network(ROAD_NETWORK, COORDINATES, selected_start, selected_goal, path, explored_order)

        st.subheader(f"📊 Heuristic Table: h(n) to {selected_goal}")
        st.markdown(
            """
            The heuristic **h(n)** represents the estimated straight-line Euclidean distance from each location to the selected destination.
            """
        )

        heuristic_data = []
        for node in ROAD_NETWORK.keys():
            h_value = calculate_euclidean_distance(node, selected_goal)
            if node in path:
                status = "🔵 In Final Path"
            elif node in visited_nodes:
                status = "🟡 Explored"
            else:
                status = "⚪ Unvisited"

            heuristic_data.append({
                "Location": node,
                "Heuristic h(n) [km]": f"{h_value:.2f}",
                "Status": status
            })

        st.dataframe(heuristic_data, use_container_width=True, hide_index=True)
    else:
        st.error("❌ No path could be found between the selected locations.")
        display_network(ROAD_NETWORK, COORDINATES, selected_start, selected_goal, explored_nodes=explored_order)

    st.divider()

    with st.expander("🧠 How the Route Search Works"):
        st.markdown(
            """
            ### A* Search

            This emergency router uses **A\\* Search**, which combines:
            - the actual travel cost from the start node, and
            - the heuristic estimate to the hospital.

            ### Evaluation Function

            **f(n) = g(n) + h(n)**

            Where:
            - **g(n)** = cost accumulated from the starting node to n
            - **h(n)** = estimated straight-line distance from n to the destination

            ### Euclidean Distance Heuristic

            The app uses Euclidean distance:

            **h(n) = √((x₂ - x₁)² + (y₂ - y₁)²)**

            ### Key Characteristics
            - 🎯 **Goal-Directed:** Prioritizes promising routes toward the hospital.
            - ⚡ **Efficient:** Finds the best route quickly in a small network.
            - ✅ **Optimal for this use case:** Minimizes total travel distance for emergency response.
            """
        )


# ============================================================================== 
# 8. RUN APPLICATION
# ============================================================================== 

if __name__ == "__main__":
    main()
