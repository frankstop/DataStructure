import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import sys

# Define the Node class
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

# Define the AVLTree class
class AVLTree:
    # Helper function to get the height of a node
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # Helper function to calculate the balance factor of a node
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Right rotate the subtree rooted with y
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1

        return x

    # Left rotate the subtree rooted with x
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1

        return y

    # Insert a key into the AVL tree
    def insert(self, root, key):
        # Perform standard BST insertion
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            # Duplicate keys are not allowed in AVL tree
            return root

        # Update height of this ancestor node
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1

        # Get the balance factor to check if this node became unbalanced
        balance = self.get_balance(root)

        # If unbalanced, there are 4 cases to handle
        # Case 1 - Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Case 2 - Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Case 3 - Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Find the node with the smallest value
    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    # Delete a node from the AVL tree
    def delete(self, root, key):
        # Perform standard BST deletion
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Node with one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Node with two children
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        # Update height of the current node
        if not root:
            return root
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1

        # Get the balance factor
        balance = self.get_balance(root)

        # If unbalanced, handle the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Case 2 - Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 3 - Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Case 4 - Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Helper function to print the tree (in-order traversal)
    def in_order(self, root):
        if root:
            self.in_order(root.left)
            print(f"{root.key} (H={root.height})", end=" ")
            self.in_order(root.right)

# Define the AVLTreeVisualizer class
class AVLTreeVisualizer:
    def __init__(self):
        self.tree = AVLTree()
        self.root = None
        self.positions = {}
        self.levels = {}
        self.x_offset = 0

        # Initialize matplotlib figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.3)  # Make space for buttons and text boxes

        # Compute initial positions and plot
        self.compute_positions()
        self.plot_tree()

        # Add Insert and Delete buttons
        self.add_buttons()

        # Add TextBoxes for input
        self.add_textboxes()

        plt.show()

    # Compute positions of nodes
    def compute_positions(self):
        self.positions = {}
        self.levels = {}
        self.x_offset = 0
        self._compute_positions_helper(self.root, depth=0)

    def _compute_positions_helper(self, node, depth):
        if node is None:
            return
        # Traverse left subtree
        self._compute_positions_helper(node.left, depth + 1)
        # Assign position
        self.positions[node.key] = (self.x_offset, depth)
        self.levels[node.key] = depth
        self.x_offset += 1
        # Traverse right subtree
        self._compute_positions_helper(node.right, depth + 1)

    # Plot the AVL tree
    def plot_tree(self):
        self.ax.clear()
        if self.root is not None:
            self.compute_positions()

            # Draw edges
            for node_key, (x, y) in self.positions.items():
                node = self._find_node(self.root, node_key)
                if node.left:
                    child_key = node.left.key
                    child_x, child_y = self.positions[child_key]
                    self.ax.plot([x, child_x], [y, child_y], 'k-', lw=1)
                if node.right:
                    child_key = node.right.key
                    child_x, child_y = self.positions[child_key]
                    self.ax.plot([x, child_x], [y, child_y], 'k-', lw=1)

            # Draw nodes
            for node_key, (x, y) in self.positions.items():
                self.ax.scatter(x, y, s=1000, c='skyblue', edgecolors='black', zorder=3)
                self.ax.text(x, y, f"{node_key}\nH={self._find_node(self.root, node_key).height}",
                             fontsize=10, ha='center', va='center')

        # Adjust plot settings
        self.ax.set_ylim(-1, self.x_offset + 1)
        self.ax.invert_yaxis()  # To have the root at the top
        self.ax.axis('off')
        self.fig.canvas.draw_idle()

    # Find a node by key
    def _find_node(self, root, key):
        if root is None:
            return None
        if key == root.key:
            return root
        elif key < root.key:
            return self._find_node(root.left, key)
        else:
            return self._find_node(root.right, key)

    # Add Insert and Delete buttons
    def add_buttons(self):
        # Define button axes
        ax_insert = plt.axes([0.3, 0.15, 0.1, 0.075])
        ax_delete = plt.axes([0.6, 0.15, 0.1, 0.075])

        # Create buttons
        self.btn_insert = Button(ax_insert, 'Insert')
        self.btn_delete = Button(ax_delete, 'Delete')

        # Assign callbacks
        self.btn_insert.on_clicked(self.insert_callback)
        self.btn_delete.on_clicked(self.delete_callback)

    # Add TextBoxes for user input
    def add_textboxes(self):
        # Insert TextBox
        ax_insert_box = plt.axes([0.3, 0.05, 0.1, 0.05])
        self.textbox_insert = TextBox(ax_insert_box, 'Insert Key:', initial="")
        self.textbox_insert.on_submit(self.submit_insert)

        # Delete TextBox
        ax_delete_box = plt.axes([0.6, 0.05, 0.1, 0.05])
        self.textbox_delete = TextBox(ax_delete_box, 'Delete Key:', initial="")
        self.textbox_delete.on_submit(self.submit_delete)

    # Callback for Insert button
    def insert_callback(self, event):
        # Activate Insert TextBox
        self.textbox_insert.set_active(True)

    # Callback for Delete button
    def delete_callback(self, event):
        # Activate Delete TextBox
        self.textbox_delete.set_active(True)

    # Submit handler for Insert TextBox
    def submit_insert(self, text):
        if text.strip() == "":
            print("Insert operation cancelled or empty input.")
            return
        try:
            key = int(text)
            self.root = self.tree.insert(self.root, key)
            print(f"Inserted {key}")
            self.plot_tree()
        except ValueError:
            print("Invalid input. Please enter an integer for insertion.")
        finally:
            self.textbox_insert.set_val("")  # Clear the textbox

    # Submit handler for Delete TextBox
    def submit_delete(self, text):
        if text.strip() == "":
            print("Delete operation cancelled or empty input.")
            return
        try:
            key = int(text)
            self.root = self.tree.delete(self.root, key)
            print(f"Deleted {key}")
            self.plot_tree()
        except ValueError:
            print("Invalid input. Please enter an integer for deletion.")
        finally:
            self.textbox_delete.set_val("")  # Clear the textbox

# Usage Example
if __name__ == "__main__":
    # Initialize the visualizer
    visualizer = AVLTreeVisualizer()

    # Optional: Insert initial nodes
    initial_insertions = [10, 20, 30, 40, 50, 25]
    print("Inserting initial nodes:")
    for key in initial_insertions:
        visualizer.root = visualizer.tree.insert(visualizer.root, key)
        print(f"Inserted {key}: ", end="")
        visualizer.tree.in_order(visualizer.root)
        print()
    visualizer.plot_tree()

    # Keep the matplotlib window open
    try:
        plt.show()
    except KeyboardInterrupt:
        sys.exit()