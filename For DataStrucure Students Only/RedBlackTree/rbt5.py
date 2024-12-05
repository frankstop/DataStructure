import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import sys
import matplotlib.animation as animation
import networkx as nx
import pydot

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
        self.events = []  # To store events for visualization

    # Left rotate the subtree rooted at x
    def left_rotate(self, x):
        y = x.right
        self.log_event(f"Left Rotate at node {x.key}", 
                       "Performing left rotation to maintain tree balance.")
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
            self.log_event(f"Node {y.key} is now the root.", 
                           "Updated the root of the tree after rotation.")
        elif x == x.parent.left:
            x.parent.left = y
            self.log_event(f"Node {y.key} is now the left child of {x.parent.key}.", 
                           "Adjusted the left child reference after rotation.")
        else:
            x.parent.right = y
            self.log_event(f"Node {y.key} is now the right child of {x.parent.key}.", 
                           "Adjusted the right child reference after rotation.")

        y.left = x
        x.parent = y

    # Right rotate the subtree rooted at y
    def right_rotate(self, y):
        x = y.left
        self.log_event(f"Right Rotate at node {y.key}", 
                       "Performing right rotation to maintain tree balance.")
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent == None:
            self.root = x
            self.log_event(f"Node {x.key} is now the root.", 
                           "Updated the root of the tree after rotation.")
        elif y == y.parent.right:
            y.parent.right = x
            self.log_event(f"Node {x.key} is now the right child of {y.parent.key}.", 
                           "Adjusted the right child reference after rotation.")
        else:
            y.parent.left = x
            self.log_event(f"Node {x.key} is now the left child of {y.parent.key}.", 
                           "Adjusted the left child reference after rotation.")

        x.right = y
        y.parent = x

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
                self.log_event(f"Insert {key} failed: Duplicate key.", 
                               "Attempted to insert a duplicate key which is not allowed.")
                return False  # Indicate that insertion was unsuccessful

        node.parent = y
        if y == None:
            self.root = node
            self.log_event(f"Inserted root node {node.key}.", 
                           "Inserted the first node as the root of the tree.")
        elif node.key < y.key:
            y.left = node
            self.log_event(f"Inserted node {node.key} as left child of {y.key}.", 
                           f"Node {node.key} is inserted as the left child of node {y.key}.")
        else:
            y.right = node
            self.log_event(f"Inserted node {node.key} as right child of {y.key}.", 
                           f"Node {node.key} is inserted as the right child of node {y.key}.")

        # If new node is a root node, simply recolor it to black and return
        if node.parent == None:
            node.color = 'black'
            self.log_event(f"Recolor node {node.key} to black (root).", 
                           "The root node is always black to satisfy Red-Black Tree properties.")
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
                    self.log_event(f"Insert Fixup Case 1 at node {k.key}", 
                                   "Parent is red and uncle is red. Recoloring required.")
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.log_event(f"Recolor node {u.key} to black.", 
                                   "Recoloring the uncle node to black.")
                    self.log_event(f"Recolor node {k.parent.key} to black.", 
                                   "Recoloring the parent node to black.")
                    self.log_event(f"Recolor node {k.parent.parent.key} to red.", 
                                   "Recoloring the grandparent node to red.")
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2
                        self.log_event(f"Insert Fixup Case 2 at node {k.key}", 
                                       "Parent is red, uncle is black, and node is left child. Right rotation required.")
                        k = k.parent
                        self.right_rotate(k)
                    # Case 3
                    self.log_event(f"Insert Fixup Case 3 at node {k.key}", 
                                   "Parent is red, uncle is black, and node is right child. Left rotation and recoloring required.")
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.log_event(f"Recolor node {k.parent.key} to black.", 
                                   "Recoloring the parent node to black.")
                    self.log_event(f"Recolor node {k.parent.parent.key} to red.", 
                                   "Recoloring the grandparent node to red.")
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # Uncle

                if u.color == 'red':
                    # Case 1
                    self.log_event(f"Insert Fixup Case 1 at node {k.key}", 
                                   "Parent is red and uncle is red. Recoloring required.")
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.log_event(f"Recolor node {u.key} to black.", 
                                   "Recoloring the uncle node to black.")
                    self.log_event(f"Recolor node {k.parent.key} to black.", 
                                   "Recoloring the parent node to black.")
                    self.log_event(f"Recolor node {k.parent.parent.key} to red.", 
                                   "Recoloring the grandparent node to red.")
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Case 2
                        self.log_event(f"Insert Fixup Case 2 at node {k.key}", 
                                       "Parent is red, uncle is black, and node is right child. Left rotation required.")
                        k = k.parent
                        self.left_rotate(k)
                    # Case 3
                    self.log_event(f"Insert Fixup Case 3 at node {k.key}", 
                                   "Parent is red, uncle is black, and node is left child. Right rotation and recoloring required.")
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.log_event(f"Recolor node {k.parent.key} to black.", 
                                   "Recoloring the parent node to black.")
                    self.log_event(f"Recolor node {k.parent.parent.key} to red.", 
                                   "Recoloring the grandparent node to red.")
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'black'
        self.log_event(f"Recolor root node {self.root.key} to black.", 
                       "Ensuring the root node is black to satisfy Red-Black Tree properties.")

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
            self.log_event(f"Transplant: Node {v.key} is now the root.", 
                           "Transplanting node to root as the tree's new root.")
        elif u == u.parent.left:
            u.parent.left = v
            self.log_event(f"Transplant: Node {v.key} is now the left child of {u.parent.key}.", 
                           "Transplanting node as the left child of its parent.")
        else:
            u.parent.right = v
            self.log_event(f"Transplant: Node {v.key} is now the right child of {u.parent.key}.", 
                           "Transplanting node as the right child of its parent.")
        v.parent = u.parent

    # Delete a node from the Red-Black Tree
    def delete_node(self, key):
        z = self.search_tree_helper(self.root, key)
        if z == self.NIL:
            self.log_event(f"Delete {key} failed: Key not found.", 
                           "Attempted to delete a non-existent key.")
            return False  # Indicate that deletion was unsuccessful

        self.log_event(f"Deleting node {z.key}.", 
                       "Initiating deletion of the specified node.")

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
            self.log_event(f"Deleted node {z.key} by transplanting its right child.", 
                           "Node has at most one child; transplanted its right child.")
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
            self.log_event(f"Deleted node {z.key} by transplanting its left child.", 
                           "Node has at most one child; transplanted its left child.")
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
                self.log_event(f"Deleted node {z.key} by transplanting its successor {y.key}.", 
                               "Node has two children; transplanted its in-order successor.")
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                self.log_event(f"Transplanted successor {y.key} with its right child.", 
                               "Adjusted the successor's right child after transplant.")
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            self.log_event(f"Recolor node {y.key} to {y.color}.", 
                           "Recolored the successor node to maintain Red-Black properties.")

        if y_original_color == 'black':
            self.delete_fixup(x)
        return True

    # Fix the Red-Black Tree after deletion
    def delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'red':
                    # Case 1
                    self.log_event(f"Delete Fixup Case 1: Sibling {s.key} is red.", 
                                   "Sibling is red. Perform left rotation and recoloring.")
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.log_event(f"Recolor node {s.key} to black.", 
                                   "Recoloring the sibling to black.")
                    self.log_event(f"Recolor node {x.parent.key} to red.", 
                                   "Recoloring the parent to red.")
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 'black' and s.right.color == 'black':
                    # Case 2
                    self.log_event(f"Delete Fixup Case 2: Sibling {s.key} has two black children.", 
                                   "Sibling has two black children. Recolor sibling to red.")
                    s.color = 'red'
                    self.log_event(f"Recolor node {s.key} to red.", 
                                   "Recoloring the sibling to red.")
                    x = x.parent
                else:
                    if s.right.color == 'black':
                        # Case 3
                        self.log_event(f"Delete Fixup Case 3: Sibling {s.key}'s right child is black.", 
                                       "Sibling's right child is black. Perform right rotation and recoloring.")
                        s.left.color = 'black'
                        s.color = 'red'
                        self.log_event(f"Recolor node {s.left.key} to black.", 
                                       "Recoloring sibling's left child to black.")
                        self.right_rotate(s)
                        s = x.parent.right

                    # Case 4
                    self.log_event(f"Delete Fixup Case 4: Sibling {s.key} has a red right child.", 
                                   "Sibling has a red right child. Perform left rotation and recoloring.")
                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.right.color = 'black'
                    self.log_event(f"Recolor node {s.key} to {s.color}.", 
                                   "Recoloring sibling to match parent color.")
                    self.log_event(f"Recolor node {x.parent.key} to black.", 
                                   "Recoloring parent to black.")
                    self.log_event(f"Recolor node {s.right.key} to black.", 
                                   "Recoloring sibling's right child to black.")
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'red':
                    # Case 1
                    self.log_event(f"Delete Fixup Case 1: Sibling {s.key} is red.", 
                                   "Sibling is red. Perform right rotation and recoloring.")
                    s.color = 'black'
                    x.parent.color = 'red'
                    self.log_event(f"Recolor node {s.key} to black.", 
                                   "Recoloring the sibling to black.")
                    self.log_event(f"Recolor node {x.parent.key} to red.", 
                                   "Recoloring the parent to red.")
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 'black' and s.right.color == 'black':
                    # Case 2
                    self.log_event(f"Delete Fixup Case 2: Sibling {s.key} has two black children.", 
                                   "Sibling has two black children. Recolor sibling to red.")
                    s.color = 'red'
                    self.log_event(f"Recolor node {s.key} to red.", 
                                   "Recoloring the sibling to red.")
                    x = x.parent
                else:
                    if s.left.color == 'black':
                        # Case 3
                        self.log_event(f"Delete Fixup Case 3: Sibling {s.key}'s left child is black.", 
                                       "Sibling's left child is black. Perform left rotation and recoloring.")
                        s.right.color = 'black'
                        s.color = 'red'
                        self.log_event(f"Recolor node {s.right.key} to black.", 
                                       "Recoloring sibling's right child to black.")
                        self.left_rotate(s)
                        s = x.parent.left

                    # Case 4
                    self.log_event(f"Delete Fixup Case 4: Sibling {s.key} has a red left child.", 
                                   "Sibling has a red left child. Perform right rotation and recoloring.")
                    s.color = x.parent.color
                    x.parent.color = 'black'
                    s.left.color = 'black'
                    self.log_event(f"Recolor node {s.key} to {s.color}.", 
                                   "Recoloring sibling to match parent color.")
                    self.log_event(f"Recolor node {x.parent.key} to black.", 
                                   "Recoloring parent to black.")
                    self.log_event(f"Recolor node {s.left.key} to black.", 
                                   "Recoloring sibling's left child to black.")
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'
        self.log_event(f"Recolor node {x.key} to black.", 
                       "Ensuring the final node is black to maintain Red-Black properties.")

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

    # Clear events after handling
    def clear_events(self):
        self.events = []

    # Log events for visualization
    def log_event(self, description, explanation):
        self.events.append({'description': description, 'explanation': explanation})

# Define the RedBlackTreeVisualizer class with enhanced visualization
class RedBlackTreeVisualizer:
    def __init__(self, bulk_insert=None):
        self.tree = RedBlackTree()
        self.positions = {}
        self.G = nx.DiGraph()
        self.bulk_insert = bulk_insert  # Tuple (start, end) or None
        self.is_bulk = bulk_insert is not None
        self.is_manual = not self.is_bulk  # Flag to indicate manual operations

        # Initialize lists to store annotations
        self.annotations = []

        # Initialize matplotlib figure and axes
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        plt.subplots_adjust(bottom=0.2)  # Adjust to make space for buttons and text boxes

        # Initialize plot elements
        self.nodes_scatter = None
        self.node_keys = []
        self.hover_annotation = None

        # Add Insert and Delete buttons only if not in bulk insertion mode
        if not self.is_bulk:
            self.add_buttons()
            self.add_textboxes()

        # Bulk insertion setup
        self.bulk_insert_list = []
        self.bulk_insert_index = 0
        self.animation_obj = None
        if self.is_bulk:
            self.bulk_insert_list = list(range(self.bulk_insert[0], self.bulk_insert[1] + 1))
            # Initialize animation for bulk insertion with optimized settings
            self.animation_obj = animation.FuncAnimation(
                self.fig,
                self.bulk_insert_step,
                frames=self.chunked_bulk_insert(),
                interval=1000,  # Adjusted interval for visibility
                repeat=False,
                blit=False  # Disable blitting for compatibility
            )

        # Connect the hover event
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)

        # Show initial empty tree
        self.plot_tree()

        # Display the plot
        plt.show()

    def chunked_bulk_insert(self, chunk_size=5):
        """
        Generator to yield chunks of keys to insert per frame.
        This reduces the number of animation frames and optimizes performance.
        """
        for i in range(0, len(self.bulk_insert_list), chunk_size):
            yield self.bulk_insert_list[i:i+chunk_size]

    # Compute positions of nodes using NetworkX's graphviz_layout
    def compute_positions(self):
        self.G.clear()
        self.node_keys = []
        self._add_edges(self.tree.root)
        try:
            pos = nx.nx_pydot.graphviz_layout(self.G, prog='dot')
        except:
            # Fallback to spring layout if graphviz is not available
            pos = nx.spring_layout(self.G)
        # Normalize positions for better visualization
        pos = self.normalize_positions(pos)
        return pos

    def normalize_positions(self, pos):
        # Normalize the positions to fit within the plot
        xs = [x for x, y in pos.values()]
        ys = [y for x, y in pos.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        scale_x = max_x - min_x if max_x - min_x != 0 else 1
        scale_y = max_y - min_y if max_y - min_y != 0 else 1
        normalized_pos = {k: ((x - min_x) / scale_x * 10, (y - min_y) / scale_y * 10)
                          for k, (x, y) in pos.items()}
        return normalized_pos

    def _add_edges(self, node):
        if node != self.tree.NIL:
            self.G.add_node(node.key, color=node.color)
            self.node_keys.append(node.key)
            if node.left and node.left != self.tree.NIL:
                self.G.add_edge(node.key, node.left.key)
                self._add_edges(node.left)
            if node.right and node.right != self.tree.NIL:
                self.G.add_edge(node.key, node.right.key)
                self._add_edges(node.right)

    # Plot the Red-Black Tree with enhanced visualization
    def plot_tree(self):
        self.ax.clear()
        if self.tree.root != self.tree.NIL:
            self.positions = self.compute_positions()

            # Draw edges
            edge_x = []
            edge_y = []
            for edge in self.G.edges():
                x1, y1 = self.positions[edge[0]]
                x2, y2 = self.positions[edge[1]]
                edge_x.extend([x1, x2, None])
                edge_y.extend([y1, y2, None])

            # Draw all edges at once
            self.ax.plot(edge_x, edge_y, 'k-', lw=1)

            # **Node Representation as Scatter Points**
            node_x = []
            node_y = []
            node_colors = []
            self.node_keys = []
            for key in self.G.nodes():
                node = self.tree.search_tree_helper(self.tree.root, key)
                node_x.append(self.positions[key][0])
                node_y.append(self.positions[key][1])
                node_colors.append('red' if node.color == 'red' else 'black')
                self.node_keys.append(key)
            self.nodes_scatter = self.ax.scatter(node_x, node_y, c=node_colors, s=500, zorder=3, edgecolors='black')

            # Add labels
            for key in self.G.nodes():
                x, y = self.positions[key]
                node = self.tree.search_tree_helper(self.tree.root, key)
                label_color = 'white' if node.color == 'red' else 'white'
                self.ax.text(x, y, str(key), fontsize=12, ha='center', va='center', color=label_color)

        # Add annotations
        for annotation in self.annotations:
            self.ax.text(annotation['x'], annotation['y'], annotation['text'],
                         fontsize=10, color='blue', ha='center', va='center',
                         bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))

        # Display tree properties
        if self.tree.root != self.tree.NIL:
            black_height = self.compute_black_height(self.tree.root)
            self.ax.text(0.5, -12, f"Black Height of Tree: {black_height}", transform=self.ax.transAxes,
                         fontsize=12, ha='center')

        # Adjust plot settings for better scalability
        self.ax.set_aspect('equal')
        self.ax.set_ylim(-15, 15)
        self.ax.set_xlim(-15, 15)
        self.ax.axis('off')
        self.fig.canvas.draw_idle()

    # Compute the black height of the tree
    def compute_black_height(self, node):
        if node == self.tree.NIL:
            return 0
        left_black_height = self.compute_black_height(node.left)
        right_black_height = self.compute_black_height(node.right)
        black_height = max(left_black_height, right_black_height)
        if node.color == 'black':
            black_height += 1
        return black_height

    # Find a node by key
    def _find_node(self, root, key):
        return self.tree.search_tree_helper(root, key)

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
            for event in self.tree.events:
                # Determine annotation position based on event type
                if "Rotate" in event['description']:
                    self.annotations.append({'x': 0, 'y': 12, 'text': event['description'] + "\n" + event['explanation']})
                elif "Recolor" in event['description']:
                    self.annotations.append({'x': 0, 'y': 13, 'text': event['description'] + "\n" + event['explanation']})
                elif "Delete" in event['description'] or "Insert" in event['description']:
                    self.annotations.append({'x': 0, 'y': 14, 'text': event['description'] + "\n" + event['explanation']})
            # Clear events after handling
            self.tree.clear_events()

    # Clear annotations
    def clear_annotations(self):
        self.annotations = []

    # Bulk insertion step for animation
    def bulk_insert_step(self, frame_keys):
        """
        Inserts a batch of keys per frame to optimize performance.
        """
        for key in frame_keys:
            success = self.tree.insert(key)
            if success:
                print(f"Bulk Inserted {key}")
            else:
                print(f"Key {key} already exists. Insertion skipped.")
            # Handle rotation and color change visualization
            self.handle_events()
            self.plot_tree()

    # Hover event handler
    def on_hover(self, event):
        if event.inaxes == self.ax and self.nodes_scatter:
            cont, ind = self.nodes_scatter.contains(event)
            if cont:
                idx = ind["ind"][0]
                key = self.node_keys[idx]
                pos = self.positions[key]
                if not self.hover_annotation:
                    self.hover_annotation = self.ax.annotate(
                        f"{key}",
                        xy=pos,
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->")
                    )
                else:
                    self.hover_annotation.xy = pos
                    self.hover_annotation.set_text(f"{key}")
                    self.hover_annotation.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if self.hover_annotation:
                    self.hover_annotation.set_visible(False)
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
        print("  python3 rbt_visualizer.py            # Run with interactive mode")
        print("  python3 rbt_visualizer.py start end  # Bulk insert integers from start to end")
        sys.exit(1)

    # Initialize the visualizer with or without bulk insertion
    visualizer = RedBlackTreeVisualizer(bulk_insert=bulk_insert)

    if not bulk_insert:
        # Optional: Insert initial nodes for interactive mode
        initial_insertions = [1, 2, 3, 5, 6, 8, 10, 9, 15]
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