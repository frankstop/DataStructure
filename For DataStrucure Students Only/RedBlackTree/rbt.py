import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import sys
import matplotlib.animation as animation

# Define the Node class for Red-Black Tree
class Node:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color  # 'red' or 'black'
        self.left = None
        self.right = None
        self.parent = None

# Define the RedBlackTree class with rotation and color tracking
class RedBlackTree:
    def __init__(self):
        self.NIL = Node(key=None, color='black')  # Sentinel NIL node
        self.root = self.NIL
        self.rotation_info = []  # To store rotation events
        self.color_changes = []  # To store color change events

    # Left rotate the subtree rooted at x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

        # Log the rotation event
        self.rotation_info.append({
            'type': 'Left Rotation',
            'node': x.key,
            'rotated_node': y.key
        })

    # Right rotate the subtree rooted at y
    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent == None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

        # Log the rotation event
        self.rotation_info.append({
            'type': 'Right Rotation',
            'node': y.key,
            'rotated_node': x.key
        })

    # Insert a key into the Red-Black Tree
    def insert(self, key):
        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL

        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                # Duplicate keys are not allowed
                return

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        # If new node is a root node, simply recolor it to black and return
        if node.parent == None:
            node.color = 'black'
            self.color_changes.append({
                'node': node.key,
                'color': 'black'
            })
            return

        # If the grandparent is None, simply return
        if node.parent.parent == None:
            return

        # Fix the tree
        self.insert_fixup(node)

    # Fix the Red-Black Tree after insertion
    def insert_fixup(self, k):
        while k.parent.color == 'red':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # Uncle
                if u.color == 'red':
                    # Case 1
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.append({'node': u.key, 'color': 'black'})
                    self.color_changes.append({'node': k.parent.key, 'color': 'black'})
                    self.color_changes.append({'node': k.parent.parent.key, 'color': 'red'})
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2
                        k = k.parent
                        self.right_rotate(k)
                    # Case 3
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.append({'node': k.parent.key, 'color': 'black'})
                    self.color_changes.append({'node': k.parent.parent.key, 'color': 'red'})
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # Uncle

                if u.color == 'red':
                    # Case 1
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.append({'node': u.key, 'color': 'black'})
                    self.color_changes.append({'node': k.parent.key, 'color': 'black'})
                    self.color_changes.append({'node': k.parent.parent.key, 'color': 'red'})
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Case 2
                        k = k.parent
                        self.left_rotate(k)
                    # Case 3
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.append({'node': k.parent.key, 'color': 'black'})
                    self.color_changes.append({'node': k.parent.parent.key, 'color': 'red'})
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'black'
        self.color_changes.append({'node': self.root.key, 'color': 'black'})

    # Find node by key
    def search_tree_helper(self, node, key):
        if node == self.NIL or key == node.key:
            return node

        if key < node.key:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # Transplant nodes
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Delete a node from the Red-Black Tree
    def delete_node(self, key):
        z = self.search_tree_helper(self.root, key)
        if z == self.NIL:
            return  # Key not found

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            self.color_changes.append({'node': y.key, 'color': y.color})

        if y_original_color == 'black':
            self.delete_fixup(x)

    # Fix the Red-Black Tree after deletion
    def delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.color_changes.append({'node': s.key, 'color': 'black'})
                    self.color_changes.append({'node': x.parent.key, 'color': 'red'})
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 'black' and s.right.color == 'black':
                    s.color = 'red'
                    self.color_changes.append({'node': s.key, 'color': 'red'})
                    x = x.parent
                else:
                    if s.right.color == 'black':
                        s.left.color = 'black'
                        s.color = 'red'
                        self.color_changes.append({'node': s.left.key, 'color': 'black'})
                        self.color_changes.append({'node': s.key, 'color': 'red'})
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.right.color = 'black'
                    self.color_changes.append({'node': s.key, 'color': s.color})
                    self.color_changes.append({'node': x.parent.key, 'color': 'black'})
                    self.color_changes.append({'node': s.right.key, 'color': 'black'})
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.color_changes.append({'node': s.key, 'color': 'black'})
                    self.color_changes.append({'node': x.parent.key, 'color': 'red'})
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 'black' and s.left.color == 'black':
                    s.color = 'red'
                    self.color_changes.append({'node': s.key, 'color': 'red'})
                    x = x.parent
                else:
                    if s.left.color == 'black':
                        s.right.color = 'black'
                        s.color = 'red'
                        self.color_changes.append({'node': s.right.key, 'color': 'black'})
                        self.color_changes.append({'node': s.key, 'color': 'red'})
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.left.color = 'black'
                    self.color_changes.append({'node': s.key, 'color': s.color})
                    self.color_changes.append({'node': x.parent.key, 'color': 'black'})
                    self.color_changes.append({'node': s.left.key, 'color': 'black'})
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'
        self.color_changes.append({'node': x.key, 'color': 'black'})

    # Find the node with the minimum key
    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    # In-order traversal for debugging
    def in_order_helper(self, node):
        if node != self.NIL:
            self.in_order_helper(node.left)
            print(f"{node.key}({node.color})", end=' ')
            self.in_order_helper(node.right)

    # Clear rotation and color change info after handling
    def clear_events(self):
        self.rotation_info = []
        self.color_changes = []

# Define the RedBlackTreeVisualizer class with enhanced visualization
class RedBlackTreeVisualizer:
    def __init__(self, bulk_insert=None):
        self.tree = RedBlackTree()
        self.positions = {}
        self.x_offset = 0

        # Variables to store last rotation and color change events
        self.last_rotation = None
        self.last_color_changes = []

        # Initialize a list to store imbalance highlights and rotation annotations
        self.rotation_annotations = []
        self.color_annotations = []

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

        # Bulk insertion setup
        self.bulk_insert = bulk_insert  # Tuple (start, end) or None
        self.bulk_insert_list = []
        self.bulk_insert_index = 0
        if self.bulk_insert:
            self.bulk_insert_list = list(range(self.bulk_insert[0], self.bulk_insert[1] + 1))
            # Initialize animation for bulk insertion with save_count to suppress the warning
            self.ani = animation.FuncAnimation(
                self.fig,
                self.bulk_insert_step,
                interval=100,
                repeat=False,
                save_count=len(self.bulk_insert_list)  # Set save_count based on bulk insert range
            )

        plt.show()

    # Compute positions of nodes using in-order traversal
    def compute_positions(self):
        self.positions = {}
        self.x_offset = 0
        self._compute_positions_helper(self.tree.root, depth=0)

    def _compute_positions_helper(self, node, depth):
        if node == self.tree.NIL:
            return
        # Traverse left subtree
        self._compute_positions_helper(node.left, depth + 1)
        # Assign position
        self.positions[node.key] = (self.x_offset, -depth)
        self.x_offset += 1
        # Traverse right subtree
        self._compute_positions_helper(node.right, depth + 1)

    # Plot the Red-Black Tree with enhanced visualization
    def plot_tree(self):
        self.ax.clear()
        if self.tree.root != self.tree.NIL:
            self.compute_positions()

            # Draw edges
            for node_key, (x, y) in self.positions.items():
                node = self._find_node(self.tree.root, node_key)
                if node.left and node.left != self.tree.NIL:
                    child_key = node.left.key
                    child_x, child_y = self.positions[child_key]
                    self.ax.plot([x, child_x], [y, child_y], 'k-', lw=1)
                if node.right and node.right != self.tree.NIL:
                    child_key = node.right.key
                    child_x, child_y = self.positions[child_key]
                    self.ax.plot([x, child_x], [y, child_y], 'k-', lw=1)

            # Draw nodes
            for node_key, (x, y) in self.positions.items():
                node = self._find_node(self.tree.root, node_key)
                # Determine node color
                color = 'red' if node.color == 'red' else 'black'
                text_color = 'white' if node.color == 'black' else 'black'

                # Highlight nodes involved in rotation
                if any(ann.get('node') == node_key or ann.get('rotated_node') == node_key for ann in self.rotation_annotations):
                    edgecolor = 'gold'
                    linewidth = 2
                else:
                    edgecolor = 'black'
                    linewidth = 1

                self.ax.scatter(x, y, s=1000, c=color, edgecolors=edgecolor, linewidth=linewidth, zorder=3)
                self.ax.text(x, y, f"{node.key}", fontsize=10, ha='center', va='center', color=text_color)

        # Add rotation annotations
        for annotation in self.rotation_annotations:
            self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                         fontsize=12, color='blue', ha='center', va='center',
                         bbox=dict(facecolor='yellow', alpha=0.5))

        # Add color change annotations
        for annotation in self.color_annotations:
            self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                         fontsize=10, color='green', ha='center', va='center',
                         bbox=dict(facecolor='lightgreen', alpha=0.5))

        # Adjust plot settings
        self.ax.set_ylim(-self.x_offset, 1)
        self.ax.set_xlim(-1, self.x_offset)
        self.ax.invert_yaxis()  # To have the root at the top
        self.ax.axis('off')
        self.fig.canvas.draw_idle()

    # Find a node by key
    def _find_node(self, root, key):
        if root == self.tree.NIL:
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
            # Clear previous annotations
            self.clear_annotations()
            self.tree.insert(key)
            print(f"Inserted {key}")
            # Handle rotation and color change visualization
            self.handle_events()
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
            # Clear previous annotations
            self.clear_annotations()
            self.tree.delete_node(key)
            print(f"Deleted {key}")
            # Handle rotation and color change visualization
            self.handle_events()
            self.plot_tree()
        except ValueError:
            print("Invalid input. Please enter an integer for deletion.")
        finally:
            self.textbox_delete.set_val("")  # Clear the textbox

    # Handle rotation and color change events for visualization
    def handle_events(self):
        # Handle rotation events
        for rotation in self.tree.rotation_info:
            node = rotation['node']
            rotated_node = rotation['rotated_node']
            rotation_type = rotation['type']
            node_pos = self.positions.get(node, (0,0))
            rotated_node_pos = self.positions.get(rotated_node, (0,0))
            mid_x = (node_pos[0] + rotated_node_pos[0]) / 2
            mid_y = (node_pos[1] + rotated_node_pos[1]) / 2
            self.rotation_annotations.append({
                'x': mid_x,
                'y': mid_y,
                'text': rotation_type,
                'node': node,              # Added key
                'rotated_node': rotated_node  # Added key
            })

        # Handle color change events
        for change in self.tree.color_changes:
            node = change['node']
            color = change['color']
            node_pos = self.positions.get(node, (0,0))
            self.color_annotations.append({
                'x': node_pos[0],
                'y': node_pos[1] + 0.2,  # Slightly above the node
                'text': f"{node}: {color}"
            })

        # Clear events after handling
        self.tree.clear_events()

    # Clear annotations
    def clear_annotations(self):
        self.rotation_annotations = []
        self.color_annotations = []

    # Bulk insertion step for animation
    def bulk_insert_step(self, frame):
        if self.bulk_insert_index < len(self.bulk_insert_list):
            key = self.bulk_insert_list[self.bulk_insert_index]
            self.bulk_insert_index += 1
            self.tree.insert(key)
            print(f"Bulk Inserted {key}")
            self.handle_events()
            self.plot_tree()
        else:
            # Stop the animation once all insertions are done
            self.ani.event_source.stop()

# Usage Example
if __name__ == "__main__":
    # Initialize variables for bulk insertion
    bulk_insert = None

    # Parse command-line arguments
    if len(sys.argv) == 3:
        try:
            start = int(sys.argv[1])
            end = int(sys.argv[2])
            if start > end:
                print("Start value should be less than or equal to end value.")
                sys.exit(1)
            bulk_insert = (start, end)
            print(f"Bulk inserting integers from {start} to {end}.")
        except ValueError:
            print("Invalid arguments. Please provide two integers for bulk insertion.")
            sys.exit(1)
    elif len(sys.argv) == 1:
        # No arguments provided, proceed with default behavior
        pass
    else:
        print("Invalid number of arguments.")
        print("Usage:")
        print("  python3 rbt.py            # Run with interactive mode")
        print("  python3 rbt.py start end  # Bulk insert integers from start to end")
        sys.exit(1)

    # Initialize the visualizer with or without bulk insertion
    visualizer = RedBlackTreeVisualizer(bulk_insert=bulk_insert)

    if not bulk_insert:
        # Optional: Insert initial nodes
        initial_insertions = [10, 20, 30, 15, 25, 5]
        print("Inserting initial nodes:")
        for key in initial_insertions:
            visualizer.tree.insert(key)
            print(f"Inserted {key}")
        # After all initial insertions, handle any rotations and color changes
        visualizer.handle_events()
        visualizer.plot_tree()

    # Keep the matplotlib window open
    try:
        plt.show()
    except KeyboardInterrupt:
        sys.exit()