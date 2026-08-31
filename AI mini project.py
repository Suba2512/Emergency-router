"""
AI-Based Emergency Route Finder Using Greedy Best-First Search
Simulated Road Network Emergency Navigation System
"""

import streamlit as st
import plotly.graph_objects as go
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
# Predefined 2D coordinates (x, y) for nodes in the simulated city map
COORDINATES = {
    "Accident Spot": (1.0, 3.0),
    "Junction A": (3.0, 5.0),
    "Junction B": (3.5, 1.5),
    "Junction C": (6.0, 5.5),
    "Junction D": (7.0, 2.0),
    "Hospital A": (9.0, 6.0),
    "Hospital B": (9.0, 1.0)
}

# Graph adjacency list: Node -> list of tuples (neighbor, road_distance_km)
ROAD_NETWORK = {
    "Accident Spot": [("Junction A", 4.0), ("Junction B", 3.0)],
    "Junction A": [("Accident Spot", 4.0), ("Junction B", 2.5), ("Junction C", 4.0)],
    "Junction B": [("Accident Spot", 3.0), ("Junction A", 2.5), ("Junction D", 4.5)],
    "Junction C": [("Junction A", 4.0), ("Junction D", 3.5), ("Hospital A", 3.0)],
    "Junction D": [("Junction B", 4.5), ("Junction C", 3.5), ("Hospital A", 5.0), ("Hospital B", 3.0)],
    "Hospital A": [("Junction C", 3.0), ("Junction D", 5.0)],
    "Hospital B": [("Junction D", 3.0)]
}

# ==============================================================================
# 3. HEURISTIC CALCULATION
# ==============================================================================
def calculate_euclidean_distance(node_a: str, node_b: str) -> float:
    """
    Computes Euclidean straight-line distance h(n) between two graph nodes.
    Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    x1, y1 = COORDINATES[node_a]
    x2, y2 = COORDINATES[node_b]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# ==============================================================================
# 4. GREEDY BEST-FIRST SEARCH ALGORITHM
# ==============================================================================
def greedy_best_first_search(graph, start_node, goal_node, coords):
    """
    Executes Greedy Best-First Search where f(n) = h(n).
    Uses a priority queue (heapq) to select the unvisited node closest to the goal.
    """
    if start_node not in graph or goal_node not in graph:
        return None, [], []

    # Priority queue stores: (heuristic_value, insertion_counter, current_node, path_taken)
    frontier = []
    counter = 0
    start_h = calculate_euclidean_distance(start_node, goal_node)
    heapq.heappush(frontier, (start_h, counter, start_node, [start_node]))

    visited = set()
    explored_sequence = []

    while frontier:
        h_val, _, current_node, path = heapq.heappop(frontier)

        if current_node in visited:
            continue

        visited.add(current_node)
        explored_sequence.append(current_node)

        # Goal check
        if current_node == goal_node:
            return path, explored_sequence, visited

        # Expand adjacent road connections
        for neighbor, _ in graph[current_node]:
            if neighbor not in visited:
                counter += 1
                h_neighbor = calculate_euclidean_distance(neighbor, goal_node)
                heapq.heappush(
                    frontier,
                    (h_neighbor, counter, neighbor, path + [neighbor])
                )

    return None, explored_sequence, visited

# ==============================================================================
# 5. PATH DISTANCE CALCULATION
# ==============================================================================
def compute_total_path_distance(graph, path):
    """Calculates cumulative road network distance along the chosen path."""
    if not path or len(path) < 2:
        return 0.0

    total_cost = 0.0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        for neighbor, cost in graph[u]:
            if neighbor == v:
                total_cost += cost
                break
    return total_cost

# ==============================================================================
# 6. GRAPH VISUALIZATION (PLOTLY)
# ==============================================================================
def create_graph_figure(graph, coords, start_node, goal_node, final_path=None, explored_nodes=None):
    """Builds an interactive 2D graph representation of the simulated city network."""
    final_path = final_path or []
    explored_nodes = explored_nodes or []
    path_edges = set()
    for i in range(len(final_path) - 1):
        path_edges.add((final_path[i], final_path[i+1]))
        path_edges.add((final_path[i+1], final_path[i]))

    fig = go.Figure()

    # Draw Road Network Edges
    edge_x = []
    edge_y = []
    mid_x = []
    mid_y = []
    edge_labels = []
    seen_edges = set()

    for node, neighbors in graph.items():
        x0, y0 = coords[node]
        for neighbor, dist in neighbors:
            edge_id = tuple(sorted([node, neighbor]))
            x1, y1 = coords[neighbor]
            
            # Base road line
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

            # Label road distances once per pair
            if edge_id not in seen_edges:
                seen_edges.add(edge_id)
                mid_x.append((x0 + x1) / 2.0)
                mid_y.append((y0 + y1) / 2.0)
                edge_labels.append(f"{dist} km")

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(color="#BDC3C7", width=2.5),
        hoverinfo="none",
        name="Roads (Edges)",
        showlegend=False
    ))

    # Road Distance Labels
    fig.add_trace(go.Scatter(
        x=mid_x, y=mid_y,
        mode="text",
        text=edge_labels,
        textposition="middle center",
        textfont=dict(color="#7F8C8D", size=11, family="Arial Black"),
        hoverinfo="none",
        name="Road Distances",
        showlegend=False
    ))

    # Highlight Final Route (if found)
    if len(final_path) > 1:
        route_x = []
        route_y = []
        for i in range(len(final_path) - 1):
            u, v = final_path[i], final_path[i+1]
            route_x.extend([coords[u][0], coords[v][0], None])
            route_y.extend([coords[u][1], coords[v][1], None])

        fig.add_trace(go.Scatter(
            x=route_x, y=route_y,
            mode="lines",
            line=dict(color="#2980B9", width=6),
            hoverinfo="none",
            name="🔵 Final Selected Route"
        ))

    # Group and render nodes with distinct visual markers
    for node, (x, y) in coords.items():
        h_val = calculate_euclidean_distance(node, goal_node)
        
        if node == start_node:
            marker_color = "#2ECC71"  # Green
            marker_symbol = "circle"
            marker_size = 28
            category = "🟢 Start / Emergency Spot"
        elif node == goal_node:
            marker_color = "#E74C3C"  # Red
            marker_symbol = "cross"
            marker_size = 30
            category = "🔴 Destination Hospital"
        elif node in final_path:
            marker_color = "#3498DB"  # Blue
            marker_symbol = "circle"
            marker_size = 22
            category = "🔵 Route Junction"
        elif node in explored_nodes:
            marker_color = "#F39C12"  # Yellow / Orange
            marker_symbol = "circle"
            marker_size = 20
            category = "🟡 Explored Node"
        else:
            marker_color = "#34495E"  # Dark Slate
            marker_symbol = "circle"
            marker_size = 18
            category = "⚫ Normal Road Node"

        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(
                color=marker_color,
                size=marker_size,
                symbol=marker_symbol,
                line=dict(width=2, color="#FFFFFF")
            ),
            text=[f"<b>{node}</b>"],
            textposition="top center",
            textfont=dict(size=12, color="#2C3E50"),
            hoverinfo="text",
            hovertext=[f"<b>{node}</b><br>Heuristic h(n): {h_val:.2f} km<br>Status: {category}"],
            name=node,
            showlegend=False
        ))

    # Layout styling
    fig.update_layout(
        title="<b>Simulated Road Network & Search State</b>",
        title_x=0.02,
        xaxis=dict(showgrid=True, zeroline=False, showticklabels=False, range=[0, 10.5]),
        yaxis=dict(showgrid=True, zeroline=False, showticklabels=False, range=[0, 7.5]),
        plot_bgcolor="#F8F9FA",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=50, b=20),
        height=520,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

# ==============================================================================
# 7. STREAMLIT USER INTERFACE
# ==============================================================================
def main():
    # Header Section
    st.title("🚑 AI-Based Emergency Route Finder")
    st.subheader("Greedy Best-First Search Based Route Planning")
    st.markdown(
        "Find a goal-directed emergency route through a simulated road network using "
        "**Greedy Best-First Search**."
    )
    st.caption("⚠️ **Notice:** This application utilizes a simulated road network for AI algorithmic demonstration.")
    st.divider()

    # Sidebar Settings
    st.sidebar.header("⚙️ Emergency Route Settings")
    
    available_nodes = list(ROAD_NETWORK.keys())
    hospitals = ["Hospital A", "Hospital B"]
    start_locations = [n for n in available_nodes if n not in hospitals]

    selected_start = st.sidebar.selectbox(
        "Emergency Location",
        options=start_locations,
        index=start_locations.index("Accident Spot") if "Accident Spot" in start_locations else 0
    )

    selected_goal = st.sidebar.selectbox(
        "Destination Hospital",
        options=hospitals,
        index=0
    )

    search_button = st.sidebar.button("🚑 Find Emergency Route", type="primary", use_container_width=True)

    # Main Area Layout
    if search_button:
        if selected_start == selected_goal:
            st.warning("The emergency location and destination hospital cannot be the same.")
            fig = create_graph_figure(ROAD_NETWORK, COORDINATES, selected_start, selected_goal)
            st.plotly_chart(fig, use_container_width=True)
            return

        # Execute Search
        path, explored_order, visited_nodes = greedy_best_first_search(
            ROAD_NETWORK, selected_start, selected_goal, COORDINATES
        )

        if path:
            total_distance = compute_total_path_distance(ROAD_NETWORK, path)

            # Metrics Display
            st.success("✅ **Emergency Route Found Successfully!**")
            m1, m2, m3 = st.columns(3)
            m1.metric(label="📏 Path Distance", value=f"{total_distance:.1f} km")
            m2.metric(label="🔍 Nodes Explored", value=f"{len(explored_order)}")
            m3.metric(label="🧠 Algorithm", value="Greedy BFS")

            # Route Trajectory Display
            st.markdown("#### **Selected Route Path:**")
            st.info(" ➔ ".join([f"**{node}**" for node in path]))

            # Exploration Order
            st.markdown("#### **Exploration Sequence (Node Expansion):**")
            exploration_str = " ➔ ".join([f"**{idx + 1}. {node}**" for idx, node in enumerate(explored_order)])
            st.write(exploration_str)

            # Updated Graph Visualization
            fig = create_graph_figure(
                ROAD_NETWORK, COORDINATES, selected_start, selected_goal, path, explored_order
            )
            st.plotly_chart(fig, use_container_width=True)

            # Heuristic Distance Table
            st.subheader(f"📊 Heuristic Table: $h(n)$ to {selected_goal}")
            st.markdown(
                "The heuristic $h(n)$ represents the straight-line Euclidean distance from each location "
                "to the chosen destination."
            )

            heuristic_data = []
            for node in ROAD_NETWORK.keys():
                h_val = calculate_euclidean_distance(node, selected_goal)
                status = "In Path" if node in path else ("Explored" if node in visited_nodes else "Unvisited")
                heuristic_data.append({
                    "Location Node": node,
                    "Heuristic Distance h(n) [km]": f"{h_val:.2f}",
                    "Status": status
                })

            st.dataframe(heuristic_data, use_container_width=True)

        else:
            st.error("❌ No path could be found between the selected locations.")
            fig = create_graph_figure(ROAD_NETWORK, COORDINATES, selected_start, selected_goal)
            st.plotly_chart(fig, use_container_width=True)

    else:
        # Default State Before Search
        st.info("👉 Select the emergency spot and hospital in the sidebar, then click **'Find Emergency Route'**.")
        fig = create_graph_figure(ROAD_NETWORK, COORDINATES, selected_start, selected_goal)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Expandable Educational Concept Section
    with st.expander("🧠 How Greedy Best-First Search Works"):
        st.markdown(
            """
            ### **Concept & Evaluation Function**
            **Greedy Best-First Search** is an informed search algorithm that expands the node estimated to be closest to the goal.
            
            The node evaluation function is defined as:
            $$f(n) = h(n)$$
            
            Where:
            * $f(n)$ is the total evaluation score of node $n$.
            * $h(n)$ is the **heuristic estimate** of the cost from node $n$ to the goal.

            ### **Euclidean Distance Heuristic**
            In this application, the heuristic is calculated using the standard 2D Euclidean distance formula:
            $$h(n) = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

            ### **Key Characteristics**
            * **Goal-Directed:** Greedy BFS aggressively prioritizes immediate progress toward the destination.
            * **Optimality Trade-off:** While fast, Greedy Best-First Search **does not guarantee the shortest or optimal path**, because it completely ignores the backward path cost $g(n)$ accumulated so far.
            """
        )

if __name__ == "__main__":
    main()