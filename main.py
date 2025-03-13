import streamlit as st
import numpy as np
import random
from ucs import ucs
from bfs import bfs
from dfs import dfs

class Warehouse:
    def __init__(self):
        self.setup_sidebar()
        self.initialize_warehouse()
        self.robot_pos = (0, 0)
        self.warehouse[self.robot_pos] = 'R'
        self.package_positions = self.place_items('P', self.P)
        self.dropoff_positions = self.place_items('D', self.P)
        self.obstacle_positions = self.place_items('O', self.O)
        self.total_cost = 0
        self.reward_per_delivery = 10
        self.penalty_obstacle_hit = -5
        self.current_pos = self.robot_pos

    def setup_sidebar(self):
        st.title("Dynamic Goal-Based Agent for Warehouse Logistics Optimization")
        st.sidebar.title("Setup Warehouse")
        self.N = st.sidebar.number_input("Warehouse Rows (N)", min_value=5, max_value=10, value=8)
        self.M = st.sidebar.number_input("Warehouse Columns (M)", min_value=5, max_value=10, value=8)
        self.P = st.sidebar.number_input("Number of Packages (P)", min_value=2, max_value=6, value=3)
        self.O = st.sidebar.number_input("Number of Obstacles (O)", min_value=1, max_value=10, value=5)
        self.seed_value = st.sidebar.number_input("Random Seed", value=42)
        random.seed(self.seed_value)
        np.random.seed(self.seed_value)
        self.algorithm = st.sidebar.selectbox("Choose Search Algorithm", ["UCS", "BFS", "DFS"])

    def initialize_warehouse(self):
        self.warehouse = np.full((self.N, self.M), '-')

    def place_items(self, symbol, count):
        positions = []
        while len(positions) < count:
            pos = (random.randint(0, self.N-1), random.randint(0, self.M-1))
            if self.warehouse[pos] == '-':
                self.warehouse[pos] = symbol
                positions.append(pos)
        return positions

    def build_and_display_results(self):
        if st.sidebar.button("Build Warehouse and Display Results"):
            st.write("Initial Warehouse Configuration:")
            st.table(self.warehouse)

            st.markdown(f"<h2><b>Done Using {self.algorithm} Method:</b></h2>", unsafe_allow_html=True)

            for pkg_pos, drop_pos in zip(self.package_positions, self.dropoff_positions):
                # Path to package
                if self.algorithm == "UCS":
                    path_pkg, cost_pkg = ucs(self.warehouse, self.current_pos, pkg_pos)
                    path_dropoff, cost_dropoff = ucs(self.warehouse, pkg_pos, drop_pos)
                elif self.algorithm == "BFS":
                    path_pkg, cost_pkg = bfs(self.warehouse, self.current_pos, pkg_pos)
                    path_dropoff, cost_dropoff = bfs(self.warehouse, pkg_pos, drop_pos)
                elif self.algorithm == "DFS":
                    path_pkg, cost_pkg = dfs(self.warehouse, self.current_pos, pkg_pos)
                    path_dropoff, cost_dropoff = dfs(self.warehouse, pkg_pos, drop_pos)

                if path_pkg is None or path_dropoff is None:
                    st.write(f"Cannot complete delivery from {self.current_pos} to {pkg_pos} to {drop_pos}")
                    continue

                self.total_cost += cost_pkg + cost_dropoff

                st.write(f"\nDelivered package from {pkg_pos} to {drop_pos}")
                st.write(f"Path taken: {path_pkg + path_dropoff[1:]}")
                st.write(f"Cost for this delivery: {cost_pkg + cost_dropoff}")

                # Display the path in table format
                path_table = np.full((self.N, self.M), '-')
                for pos in path_pkg + path_dropoff[1:]:
                    path_table[pos] = 'R'
                path_table[drop_pos] = 'D'
                st.write("Path Table:")
                st.table(path_table)

                self.current_pos = drop_pos

            total_reward = self.reward_per_delivery * self.P
            final_score = total_reward - self.total_cost

            st.markdown("<h2><b>Final Results:</b></h2>", unsafe_allow_html=True)
            st.write(f"Total Movement Cost: {self.total_cost}")
            st.write(f"Total Reward: {total_reward}")
            st.write(f"Final Score: {final_score}")

if __name__ == "__main__":
    app = Warehouse()
    app.build_and_display_results()