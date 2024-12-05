import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import sys
import matplotlib.animation as animation
import matplotlib.patches as patches

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
                return False  # Indicate that insertion was unsuccessful

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
            return True

        # If the grandparent is None, simply return
        if node.parent.parent == None:
            return True

        # Fix the tree
        self.insert_fixup(node)
        return True

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
                    self.color_changes.extend([
                        {'node': u.key, 'color': 'black'},
                        {'node': k.parent.key, 'color': 'black'},
                        {'node': k.parent.parent.key, 'color': 'red'}
                    ])
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2
                        k = k.parent
                        self.right_rotate(k)
                    # Case 3
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.extend([
                        {'node': k.parent.key, 'color': 'black'},
                        {'node': k.parent.parent.key, 'color': 'red'}
                    ])
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # Uncle

                if u.color == 'red':
                    # Case 1
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.extend([
                        {'node': u.key, 'color': 'black'},
                        {'node': k.parent.key, 'color': 'black'},
                        {'node': k.parent.parent.key, 'color': 'red'}
                    ])
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Case 2
                        k = k.parent
                        self.left_rotate(k)
                    # Case 3
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.color_changes.extend([
                        {'node': k.parent.key, 'color': 'black'},
                        {'node': k.parent.parent.key, 'color': 'red'}
                    ])
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
            return False  # Indicate that deletion was unsuccessful

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
        return True

    # Fix the Red-Black Tree after deletion
    def delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.color_changes.extend([
                        {'node': s.key, 'color': 'black'},
                        {'node': x.parent.key, 'color': 'red'}
                    ])
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
                        self.color_changes.extend([
                            {'node': s.left.key, 'color': 'black'},
                            {'node': s.key, 'color': 'red'}
                        ])
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.right.color = 'black'
                    self.color_changes.extend([
                        {'node': s.key, 'color': s.color},
                        {'node': x.parent.key, 'color': 'black'},
                        {'node': s.right.key, 'color': 'black'}
                    ])
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'red':
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.color_changes.extend([
                        {'node': s.key, 'color': 'black'},
                        {'node': x.parent.key, 'color': 'red'}
                    ])
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
                        self.color_changes.extend([
                            {'node': s.right.key, 'color': 'black'},
                            {'node': s.key, 'color': 'red'}
                        ])
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.left.color = 'black'
                    self.color_changes.extend([
                        {'node': s.key, 'color': s.color},
                        {'node': x.parent.key, 'color': 'black'},
                        {'node': s.left.key, 'color': 'black'}
                    ])
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

        # Initialize lists to store annotations
        self.rotation_annotations = []
        self.color_annotations = []

        # Initialize matplotlib figure and axes
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        plt.subplots_adjust(bottom=0.2)  # Adjust to make space for buttons and text boxes

        # Initialize plot elements
        self.edges = []
        self.nodes = {}
        self.node_texts = {}
        self.rotation_texts = []
        self.color_texts = []

        # Add Insert and Delete buttons only if not in bulk insertion mode
        self.bulk_insert = bulk_insert  # Tuple (start, end) or None
        self.is_bulk = bulk_insert is not None
        self.is_manual = not self.is_bulk  # Flag to indicate manual operations
        if not self.is_bulk:
            self.add_buttons()
            self.add_textboxes()

        # Bulk insertion setup
        self.bulk_insert_list = []
        self.bulk_insert_index = 0
        self.animation = None
        if self.is_bulk:
            self.bulk_insert_list = list(range(self.bulk_insert[0], self.bulk_insert[1] + 1))
            # Initialize animation for bulk insertion with optimized settings
            self.animation = animation.FuncAnimation(
                self.fig,
                self.bulk_insert_step,
                frames=self.chunked_bulk_insert(),
                interval=1,  # Reduced interval for faster insertions
                repeat=False,
                blit=False  # Disable blitting for compatibility
            )

        # Show initial empty tree
        self.plot_tree()

        # Display the plot
        plt.show()

    def chunked_bulk_insert(self, chunk_size=100):
        """
        Generator to yield chunks of keys to insert per frame.
        This reduces the number of animation frames and optimizes performance.
        """
        for i in range(0, len(self.bulk_insert_list), chunk_size):
            yield self.bulk_insert_list[i:i+chunk_size]

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
            edge_x = []
            edge_y = []
            for node_key, (x, y) in self.positions.items():
                node = self._find_node(self.tree.root, node_key)
                if node.left and node.left != self.tree.NIL:
                    child_key = node.left.key
                    child_x, child_y = self.positions[child_key]
                    edge_x.extend([x, child_x, None])
                    edge_y.extend([y, child_y, None])
                if node.right and node.right != self.tree.NIL:
                    child_key = node.right.key
                    child_x, child_y = self.positions[child_key]
                    edge_x.extend([x, child_x, None])
                    edge_y.extend([y, child_y, None])

            # Draw all edges at once
            self.ax.plot(edge_x, edge_y, 'k-', lw=0.5)

            # **Simplified Node Representation:**
            # Optionally, represent nodes as small points without labels
            # Uncomment the following lines if you want to display nodes as points

            # node_x = [pos[0] for pos in self.positions.values()]
            # node_y = [pos[1] for pos in self.positions.values()]
            # self.ax.scatter(node_x, node_y, c='black', s=10, zorder=3)

        # **Omit Annotations During Bulk Insertions**
        if not self.is_bulk:
            # Add rotation annotations
            for annotation in self.rotation_annotations:
                self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                             fontsize=6, color='blue', ha='center', va='center',
                             bbox=dict(facecolor='yellow', alpha=0.5))

            # Add color change annotations
            for annotation in self.color_annotations:
                self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                             fontsize=5, color='green', ha='center', va='center',
                             bbox=dict(facecolor='lightgreen', alpha=0.5))

        # Adjust plot settings for better scalability
        self.ax.set_aspect('auto')
        self.ax.set_ylim(-self.x_offset / 2 - 1, 1)
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
        ax_insert = plt.axes([0.3, 0.1, 0.1, 0.05])
        ax_delete = plt.axes([0.6, 0.1, 0.1, 0.05])

        # Create buttons
        self.btn_insert = Button(ax_insert, 'Insert')
        self.btn_delete = Button(ax_delete, 'Delete')

        # Assign callbacks
        self.btn_insert.on_clicked(self.insert_callback)
        self.btn_delete.on_clicked(self.delete_callback)

    # Add TextBoxes for user input
    def add_textboxes(self):
        # Insert TextBox
        ax_insert_box = plt.axes([0.3, 0.02, 0.1, 0.04])
        self.textbox_insert = TextBox(ax_insert_box, 'Insert Key:', initial="")
        self.textbox_insert.on_submit(self.submit_insert)

        # Delete TextBox
        ax_delete_box = plt.axes([0.6, 0.02, 0.1, 0.04])
        self.textbox_delete = TextBox(ax_delete_box, 'Delete Key:', initial="")
        self.textbox_delete.on_submit(self.submit_delete)

    # Callback for Insert button
    def insert_callback(self, event):
        # Activate Insert TextBox
        self.textbox_insert.set_active(True)
        self.is_manual = True  # Set manual operation flag

    # Callback for Delete button
    def delete_callback(self, event):
        # Activate Delete TextBox
        self.textbox_delete.set_active(True)
        self.is_manual = True  # Set manual operation flag

    # Submit handler for Insert TextBox
    def submit_insert(self, text):
        if text.strip() == "":
            print("Insert operation cancelled or empty input.")
            self.is_manual = False  # Reset manual operation flag
            return
        try:
            key = int(text)
            # Clear previous annotations
            self.clear_annotations()
            success = self.tree.insert(key)
            if success:
                print(f"Inserted {key}")
            else:
                print(f"Key {key} already exists. Insertion skipped.")
            # Handle rotation and color change visualization
            self.handle_events()
            self.plot_tree()
        except ValueError:
            print("Invalid input. Please enter an integer for insertion.")
        finally:
            self.textbox_insert.set_val("")  # Clear the textbox
            self.is_manual = False  # Reset manual operation flag

    # Submit handler for Delete TextBox
    def submit_delete(self, text):
        if text.strip() == "":
            print("Delete operation cancelled or empty input.")
            self.is_manual = False  # Reset manual operation flag
            return
        try:
            key = int(text)
            # Clear previous annotations
            self.clear_annotations()
            success = self.tree.delete_node(key)
            if success:
                print(f"Deleted {key}")
            else:
                print(f"Key {key} not found. Deletion skipped.")
            # Handle rotation and color change visualization
            self.handle_events()
            self.plot_tree()
        except ValueError:
            print("Invalid input. Please enter an integer for deletion.")
        finally:
            self.textbox_delete.set_val("")  # Clear the textbox
            self.is_manual = False  # Reset manual operation flag

    # Handle rotation and color change events for visualization
    def handle_events(self):
        if not self.is_bulk and self.is_manual:
            # Handle rotation events
            for rotation in self.tree.rotation_info:
                node = rotation['node']
                rotated_node = rotation['rotated_node']
                rotation_type = rotation['type']
                node_pos = self.positions.get(node, (0, 0))
                rotated_node_pos = self.positions.get(rotated_node, (0, 0))
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
                node_pos = self.positions.get(node, (0, 0))
                self.color_annotations.append({
                    'x': node_pos[0],
                    'y': node_pos[1] + 0.3,  # Slightly above the node
                    'text': f"{node}: {color}"
                })

        # Clear events after handling
        self.tree.clear_events()

    # Clear annotations
    def clear_annotations(self):
        self.rotation_annotations = []
        self.color_annotations = []

    # Bulk insertion step for animation
    def bulk_insert_step(self, frame_keys):
        """
        Inserts a batch of keys per frame to optimize performance.
        """
        # Insert multiple keys in this step
        for key in frame_keys:
            success = self.tree.insert(key)
            if success:
                print(f"Bulk Inserted {key}")
            else:
                print(f"Key {key} already exists. Insertion skipped.")
            # No need to handle events or annotations during bulk insertion
        self.plot_tree()

    # Limit plot redraws by batching
    def plot_tree(self):
        """
        Optimized plot function that minimizes redraws and handles large trees efficiently.
        """
        self.ax.clear()
        if self.tree.root != self.tree.NIL:
            self.compute_positions()

            # Draw edges
            edge_x = []
            edge_y = []
            for node_key, (x, y) in self.positions.items():
                node = self._find_node(self.tree.root, node_key)
                if node.left and node.left != self.tree.NIL:
                    child_key = node.left.key
                    child_x, child_y = self.positions[child_key]
                    edge_x.extend([x, child_x, None])
                    edge_y.extend([y, child_y, None])
                if node.right and node.right != self.tree.NIL:
                    child_key = node.right.key
                    child_x, child_y = self.positions[child_key]
                    edge_x.extend([x, child_x, None])
                    edge_y.extend([y, child_y, None])

            # Draw all edges at once
            self.ax.plot(edge_x, edge_y, 'k-', lw=0.5)

            # **Optional: Represent Nodes as Small Points**
            # Uncomment the following lines if you want to display nodes as small points without labels
            # node_x = [pos[0] for pos in self.positions.values()]
            # node_y = [pos[1] for pos in self.positions.values()]
            # self.ax.scatter(node_x, node_y, c='black', s=10, zorder=3)

        # **Omit Annotations During Bulk Insertions**
        if not self.is_bulk:
            # Add rotation annotations
            for annotation in self.rotation_annotations:
                self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                             fontsize=6, color='blue', ha='center', va='center',
                             bbox=dict(facecolor='yellow', alpha=0.5))

            # Add color change annotations
            for annotation in self.color_annotations:
                self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                             fontsize=5, color='green', ha='center', va='center',
                             bbox=dict(facecolor='lightgreen', alpha=0.5))

        # Adjust plot settings for better scalability
        self.ax.set_aspect('auto')
        self.ax.set_ylim(-self.x_offset / 2 - 1, 1)
        self.ax.set_xlim(-1, self.x_offset)
        self.ax.invert_yaxis()  # To have the root at the top
        self.ax.axis('off')
        self.fig.canvas.draw_idle()

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
        # No arguments provided, proceed with interactive mode
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
        # Optional: Insert initial nodes for interactive mode
        initial_insertions = [10, 20, 30, 15, 25, 5]
        print("Inserting initial nodes:")
        for key in initial_insertions:
            success = visualizer.tree.insert(key)
            if success:
                print(f"Inserted {key}")
            else:
                print(f"Key {key} already exists. Insertion skipped.")
        # After all initial insertions, handle any rotations and color changes
        visualizer.handle_events()
        visualizer.plot_tree()

    # Keep the matplotlib window open
    try:
        plt.show()
    except KeyboardInterrupt:
        sys.exit()