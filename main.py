import streamlit as st
import numpy as np
import random

from ucs import explore_ucs
from bfs import explore_bfs
from dfs import explore_dfs

class WarehouseSimulator:
    def __init__(self):
        self.configure_interface()
        self.create_grid()
        self.robot_start = (0, 0)
        self.warehouse_layout[self.robot_start] = 'R'
        self.package_spots = self.assign_positions('P', self.total_packages)
        self.dropoff_spots = self.assign_positions('D', self.total_packages)
        self.obstacle_spots = self.assign_positions('O', self.total_obstacles)
        self.delivery_bonus = 10
        self.collision_penalty = -5
        self.reset_simulation_state()

    def reset_simulation_state(self):
        self.movement_cost = 0
        self.penalty_total = 0
        self.penalty_count = 0
        self.total_reward = 0
        self.current_location = self.robot_start

    def configure_interface(self):
        st.title("📦 Smart Warehouse Logistics Optimizer")
        st.sidebar.title("🛠️ Simulation Settings")
        self.grid_rows = st.sidebar.number_input("Grid Rows", 5, 10, value=8)
        self.grid_cols = st.sidebar.number_input("Grid Columns", 5, 10, value=8)
        self.total_packages = st.sidebar.number_input("Number of Packages", 2, 6, value=3)
        self.total_obstacles = st.sidebar.number_input("Number of Obstacles", 1, 10, value=5)
        self.random_seed = st.sidebar.number_input("Random Seed", value=42)

        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

        self.chosen_algorithm = st.sidebar.selectbox(
            "Select Search Algorithm",
            ["Uniform Cost Search", "Breadth-First Search", "Depth-First Search"]
        )

    def create_grid(self):
        self.warehouse_layout = np.full((self.grid_rows, self.grid_cols), '-')

    def assign_positions(self, marker, count):
        positions = []
        while len(positions) < count:
            x, y = random.randint(0, self.grid_rows - 1), random.randint(0, self.grid_cols - 1)
            if self.warehouse_layout[x, y] == '-' and (x, y) != self.robot_start:
                self.warehouse_layout[x, y] = marker
                positions.append((x, y))
        return positions

    def execute_simulation(self):
        if st.sidebar.button("🚀 Run Simulation"):
            self.reset_simulation_state()

            if len(self.package_spots) != len(self.dropoff_spots):
                st.error("❌ Mismatch between packages and drop-off points!")
                return

            # 🏭 Initial Layout
            st.subheader("🏭 Initial Warehouse Layout")
            st.table(self.warehouse_layout)

            # 🗺️ Legend
            st.markdown("### 🗺️ Legend:")
            st.markdown("""
            - `•` : Empty space  
            - `O` : Obstacle  
            - `P` : Package  
            - `D` : Drop-off point  
            - '🤖' : Robot's final position (after delivery)
            - `R` : Robot position
            """)

            st.markdown("### Locations:")
            cols = st.columns(3)

            with cols[0]:
                st.markdown("#### 📦 Packages")
                for i, loc in enumerate(self.package_spots, 1):
                    st.write(f"P{i}: {loc}")

            with cols[1]:
                st.markdown("#### 🎯 Drop-offs")
                for i, loc in enumerate(self.dropoff_spots, 1):
                    st.write(f"D{i}: {loc}")

            with cols[2]:
                st.markdown("#### ⛔ Obstacles")
                for i, loc in enumerate(self.obstacle_spots, 1):
                    st.write(f"O{i}: {loc}")


            st.markdown("---")

            # Algorithm name
            st.markdown(f"### 🧠 Algorithm Selected: **{self.chosen_algorithm}**")

            for i in range(self.total_packages):
                pkg_location = self.package_spots[i]
                drop_location = self.dropoff_spots[i]

                if self.chosen_algorithm == "Uniform Cost Search":
                    search_fn = explore_ucs
                elif self.chosen_algorithm == "Breadth-First Search":
                    search_fn = explore_bfs
                else:
                    search_fn = explore_dfs

                # Path to package
                path1, cost1, penalty1, count1 = search_fn(
                    self.warehouse_layout, self.current_location, pkg_location, trip_type='P'
                )
                if path1 is None:
                    st.warning(f"⚠️ No path to package {i+1} at {pkg_location}")
                    continue

                self.movement_cost += cost1
                self.penalty_total += penalty1
                self.penalty_count += count1
                self.current_location = pkg_location

                # Path to drop-off
                path2, cost2, penalty2, count2 = search_fn(
                    self.warehouse_layout, self.current_location, drop_location, trip_type='D'
                )
                if path2 is None:
                    st.warning(f"⚠️ No path to drop-off {i+1} at {drop_location}")
                    continue

                self.movement_cost += cost2
                self.penalty_total += penalty2
                self.penalty_count += count2
                self.total_reward += self.delivery_bonus
                self.current_location = drop_location

                full_path = path1 + path2[1:]

                # 📦 Delivery Summary
                st.markdown(f"""
                ### 📦 Delivery {i+1} Summary
                **Pickup From:** `{pkg_location}`  
                **Drop-off To:** `{drop_location}`  
                **Total Steps:** `{len(full_path) - 1}`  
                **Movement Cost:** `{cost1 + cost2}`  
                **Obstacles Hit:** `{count1 + count2}`  
                **Penalty Incurred:** `{penalty1 + penalty2}`  
                **Reward Earned:** `+10`
                
                **Path Taken:** `{full_path}`
                """)

                # 🗺️ Grid after delivery (showing robot at final location)
                final_grid = np.full((self.grid_rows, self.grid_cols), '•')
                for pos in self.package_spots: final_grid[pos] = 'P'
                for pos in self.dropoff_spots: final_grid[pos] = 'D'
                for pos in self.obstacle_spots: final_grid[pos] = 'O'
                final_grid[drop_location] = '🤖'

                st.write("🗺️ Warehouse Grid After Delivery:")
                st.table(final_grid)

                st.success(f"✅ Package {i+1} Delivered!")

            # 🧾 Final Score Summary
            final_score = self.total_reward - self.movement_cost - self.penalty_total

            st.markdown("---")
            st.markdown("## 🧾 Final Simulation Report")
            st.write(f"📦 Total Packages Delivered: {self.total_packages}")
            st.write(f"💰 Total Reward: {self.total_reward}")
            st.write(f"🚶 Total Movement Cost: {self.movement_cost}")
            st.write(f"⚠️ Obstacle Penalty: {self.penalty_total} (Hits: {self.penalty_count})")
            st.success(f"🏁 Final Score: {final_score}")

if __name__ == "__main__":
    sim = WarehouseSimulator()
    sim.execute_simulation()
