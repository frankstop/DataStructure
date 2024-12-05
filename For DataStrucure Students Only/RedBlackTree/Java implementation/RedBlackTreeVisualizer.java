import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;

// Node class representing each node in the Red-Black Tree
class RBNode {
    int key;
    String color; // "RED" or "BLACK"
    RBNode left, right, parent;

    RBNode(int key) {
        this.key = key;
        this.color = "RED"; // New nodes are initially red
        this.left = null;
        this.right = null;
        this.parent = null;
    }
}

// Red-Black Tree implementation
class RedBlackTree {
    private RBNode root;
    private final RBNode NIL;

    // Lists to track rotations and color changes for visualization
    public List<String> rotationInfo = new ArrayList<>();
    public List<String> colorChanges = new ArrayList<>();

    public RedBlackTree() {
        NIL = new RBNode(0);
        NIL.color = "BLACK";
        root = NIL;
    }

    // Left rotate around node x
    private void leftRotate(RBNode x) {
        RBNode y = x.right;
        x.right = y.left;
        if (y.left != NIL) {
            y.left.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;

        // Log rotation
        rotationInfo.add("Left Rotation at node " + x.key);
    }

    // Right rotate around node y
    private void rightRotate(RBNode y) {
        RBNode x = y.left;
        y.left = x.right;
        if (x.right != NIL) {
            x.right.parent = y;
        }
        x.parent = y.parent;
        if (y.parent == null) {
            root = x;
        } else if (y == y.parent.right) {
            y.parent.right = x;
        } else {
            y.parent.left = x;
        }
        x.right = y;
        y.parent = x;

        // Log rotation
        rotationInfo.add("Right Rotation at node " + y.key);
    }

    // Insert a key into the Red-Black Tree
    public void insert(int key) {
        RBNode node = new RBNode(key);
        node.left = NIL;
        node.right = NIL;

        RBNode y = null;
        RBNode x = root;

        while (x != NIL) {
            y = x;
            if (node.key < x.key) {
                x = x.left;
            } else if (node.key > x.key) {
                x = x.right;
            } else {
                // Duplicate keys not allowed
                return;
            }
        }

        node.parent = y;
        if (y == null) {
            root = node;
        } else if (node.key < y.key) {
            y.left = node;
        } else {
            y.right = node;
        }

        if (node.parent == null) {
            node.color = "BLACK";
            colorChanges.add("Node " + node.key + " set to BLACK (root)");
            return;
        }

        if (node.parent.parent == null) {
            return;
        }

        insertFixup(node);
    }

    // Fix Red-Black Tree properties after insertion
    private void insertFixup(RBNode k) {
        while (k.parent.color.equals("RED")) {
            if (k.parent == k.parent.parent.right) {
                RBNode u = k.parent.parent.left; // uncle
                if (u.color.equals("RED")) {
                    // Case 1
                    u.color = "BLACK";
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    colorChanges.add("Node " + u.key + " set to BLACK");
                    colorChanges.add("Node " + k.parent.key + " set to BLACK");
                    colorChanges.add("Node " + k.parent.parent.key + " set to RED");
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.left) {
                        // Case 2
                        k = k.parent;
                        rightRotate(k);
                    }
                    // Case 3
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    colorChanges.add("Node " + k.parent.key + " set to BLACK");
                    colorChanges.add("Node " + k.parent.parent.key + " set to RED");
                    leftRotate(k.parent.parent);
                }
            } else {
                RBNode u = k.parent.parent.right; // uncle

                if (u.color.equals("RED")) {
                    // Case 1
                    u.color = "BLACK";
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    colorChanges.add("Node " + u.key + " set to BLACK");
                    colorChanges.add("Node " + k.parent.key + " set to BLACK");
                    colorChanges.add("Node " + k.parent.parent.key + " set to RED");
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.right) {
                        // Case 2
                        k = k.parent;
                        leftRotate(k);
                    }
                    // Case 3
                    k.parent.color = "BLACK";
                    k.parent.parent.color = "RED";
                    colorChanges.add("Node " + k.parent.key + " set to BLACK");
                    colorChanges.add("Node " + k.parent.parent.key + " set to RED");
                    rightRotate(k.parent.parent);
                }
            }
            if (k == root) {
                break;
            }
        }
        root.color = "BLACK";
        colorChanges.add("Node " + root.key + " set to BLACK (root)");
    }

    // Transplant subtree u with subtree v
    private void transplant(RBNode u, RBNode v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        v.parent = u.parent;
    }

    // Delete a node from the Red-Black Tree
    public void delete(int key) {
        RBNode z = searchTreeHelper(root, key);
        if (z == NIL) {
            return; // Key not found
        }

        RBNode y = z;
        String yOriginalColor = y.color;
        RBNode x;
        if (z.left == NIL) {
            x = z.right;
            transplant(z, z.right);
        } else if (z.right == NIL) {
            x = z.left;
            transplant(z, z.left);
        } else {
            y = minimum(z.right);
            yOriginalColor = y.color;
            x = y.right;
            if (y.parent == z) {
                x.parent = y;
            } else {
                transplant(y, y.right);
                y.right = z.right;
                y.right.parent = y;
            }

            transplant(z, y);
            y.left = z.left;
            y.left.parent = y;
            y.color = z.color;
            colorChanges.add("Node " + y.key + " color set to " + y.color);
        }

        if (yOriginalColor.equals("BLACK")) {
            deleteFixup(x);
        }
    }

    // Fix Red-Black Tree properties after deletion
    private void deleteFixup(RBNode x) {
        while (x != root && x.color.equals("BLACK")) {
            if (x == x.parent.left) {
                RBNode s = x.parent.right;
                if (s.color.equals("RED")) {
                    s.color = "BLACK";
                    x.parent.color = "RED";
                    colorChanges.add("Node " + s.key + " set to BLACK");
                    colorChanges.add("Node " + x.parent.key + " set to RED");
                    leftRotate(x.parent);
                    s = x.parent.right;
                }

                if (s.left.color.equals("BLACK") && s.right.color.equals("BLACK")) {
                    s.color = "RED";
                    colorChanges.add("Node " + s.key + " set to RED");
                    x = x.parent;
                } else {
                    if (s.right.color.equals("BLACK")) {
                        s.left.color = "BLACK";
                        s.color = "RED";
                        colorChanges.add("Node " + s.left.key + " set to BLACK");
                        colorChanges.add("Node " + s.key + " set to RED");
                        rightRotate(s);
                        s = x.parent.right;
                    }

                    s.color = x.parent.color;
                    x.parent.color = "BLACK";
                    s.right.color = "BLACK";
                    colorChanges.add("Node " + s.key + " set to " + s.color);
                    colorChanges.add("Node " + x.parent.key + " set to BLACK");
                    colorChanges.add("Node " + s.right.key + " set to BLACK");
                    leftRotate(x.parent);
                    x = root;
                }
            } else {
                RBNode s = x.parent.left;
                if (s.color.equals("RED")) {
                    s.color = "BLACK";
                    x.parent.color = "RED";
                    colorChanges.add("Node " + s.key + " set to BLACK");
                    colorChanges.add("Node " + x.parent.key + " set to RED");
                    rightRotate(x.parent);
                    s = x.parent.left;
                }

                if (s.right.color.equals("BLACK") && s.left.color.equals("BLACK")) {
                    s.color = "RED";
                    colorChanges.add("Node " + s.key + " set to RED");
                    x = x.parent;
                } else {
                    if (s.left.color.equals("BLACK")) {
                        s.right.color = "BLACK";
                        s.color = "RED";
                        colorChanges.add("Node " + s.right.key + " set to BLACK");
                        colorChanges.add("Node " + s.key + " set to RED");
                        leftRotate(s);
                        s = x.parent.left;
                    }

                    s.color = x.parent.color;
                    x.parent.color = "BLACK";
                    s.left.color = "BLACK";
                    colorChanges.add("Node " + s.key + " set to " + s.color);
                    colorChanges.add("Node " + x.parent.key + " set to BLACK");
                    colorChanges.add("Node " + s.left.key + " set to BLACK");
                    rightRotate(x.parent);
                    x = root;
                }
            }
        }
        x.color = "BLACK";
        colorChanges.add("Node " + x.key + " set to BLACK");
    }

    // Search for a node with a given key
    private RBNode searchTreeHelper(RBNode node, int key) {
        if (node == NIL || key == node.key) {
            return node;
        }

        if (key < node.key) {
            return searchTreeHelper(node.left, key);
        }
        return searchTreeHelper(node.right, key);
    }

    // Find the node with the minimum key
    private RBNode minimum(RBNode node) {
        while (node.left != NIL) {
            node = node.left;
        }
        return node;
    }

    // In-order traversal (for debugging)
    public void inOrder() {
        inOrderHelper(this.root);
        System.out.println();
    }

    private void inOrderHelper(RBNode node) {
        if (node != NIL) {
            inOrderHelper(node.left);
            System.out.print(node.key + "(" + node.color + ") ");
            inOrderHelper(node.right);
        }
    }

    public RBNode getRoot() {
        return this.root;
    }
}

// Visualization panel for drawing the Red-Black Tree
class DrawPanel extends JPanel {
    private RedBlackTree tree;
    private int nodeSize = 30;
    private int levelSeparation = 50;
    private Font font = new Font("Arial", Font.BOLD, 12);

    public DrawPanel(RedBlackTree tree) {
        this.tree = tree;
        this.setBackground(Color.WHITE);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (tree.getRoot() != null && tree.getRoot().key != 0) {
            drawTree(g, tree.getRoot(), getWidth() / 2, 30, getWidth() / 4);
        }
    }

    // Recursive method to draw the tree
    private void drawTree(Graphics g, RBNode node, int x, int y, int xOffset) {
        if (node == null || node.key == 0) {
            return;
        }

        // Draw left child
        if (node.left != null && node.left.key != 0) {
            g.setColor(Color.BLACK);
            g.drawLine(x, y, x - xOffset, y + levelSeparation);
            drawTree(g, node.left, x - xOffset, y + levelSeparation, xOffset / 2);
        }

        // Draw right child
        if (node.right != null && node.right.key != 0) {
            g.setColor(Color.BLACK);
            g.drawLine(x, y, x + xOffset, y + levelSeparation);
            drawTree(g, node.right, x + xOffset, y + levelSeparation, xOffset / 2);
        }

        // Draw the node
        if (node.color.equals("RED")) {
            g.setColor(Color.RED);
        } else {
            g.setColor(Color.BLACK);
        }
        g.fillOval(x - nodeSize / 2, y - nodeSize / 2, nodeSize, nodeSize);
        g.setColor(Color.WHITE);
        g.setFont(font);
        String text = String.valueOf(node.key);
        FontMetrics fm = g.getFontMetrics();
        int textWidth = fm.stringWidth(text);
        int textAscent = fm.getAscent();
        g.drawString(text, x - textWidth / 2, y + textAscent / 2 - 2);
    }
}

// Main class for the Red-Black Tree Visualizer
public class RedBlackTreeVisualizer extends JFrame {
    private RedBlackTree tree;
    private DrawPanel drawPanel;
    private JTextField insertField;
    private JTextField deleteField;
    private JButton insertButton;
    private JButton deleteButton;
    private JButton bulkInsertButton;
    private JTextField bulkStartField;
    private JTextField bulkEndField;

    public RedBlackTreeVisualizer() {
        tree = new RedBlackTree();
        setTitle("Red-Black Tree Visualizer");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Control panel for buttons and text fields
        JPanel controlPanel = new JPanel();
        controlPanel.setLayout(new FlowLayout());

        // Insert components
        insertField = new JTextField(5);
        insertButton = new JButton("Insert");
        controlPanel.add(new JLabel("Insert Key:"));
        controlPanel.add(insertField);
        controlPanel.add(insertButton);

        // Delete components
        deleteField = new JTextField(5);
        deleteButton = new JButton("Delete");
        controlPanel.add(new JLabel("Delete Key:"));
        controlPanel.add(deleteField);
        controlPanel.add(deleteButton);

        // Bulk insert components
        bulkStartField = new JTextField(5);
        bulkEndField = new JTextField(5);
        bulkInsertButton = new JButton("Bulk Insert");
        controlPanel.add(new JLabel("Bulk Insert Start:"));
        controlPanel.add(bulkStartField);
        controlPanel.add(new JLabel("End:"));
        controlPanel.add(bulkEndField);
        controlPanel.add(bulkInsertButton);

        add(controlPanel, BorderLayout.NORTH);

        // Draw panel for visualization
        drawPanel = new DrawPanel(tree);
        add(drawPanel, BorderLayout.CENTER);

        // Action listener for Insert button
        insertButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String text = insertField.getText().trim();
                if (text.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "Insert field is empty.");
                    return;
                }
                try {
                    int key = Integer.parseInt(text);
                    tree.insert(key);
                    tree.rotationInfo.clear();
                    tree.colorChanges.clear();
                    drawPanel.repaint();
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Please enter a valid integer.");
                } finally {
                    insertField.setText("");
                }
            }
        });

        // Action listener for Delete button
        deleteButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String text = deleteField.getText().trim();
                if (text.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "Delete field is empty.");
                    return;
                }
                try {
                    int key = Integer.parseInt(text);
                    tree.delete(key);
                    tree.rotationInfo.clear();
                    tree.colorChanges.clear();
                    drawPanel.repaint();
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Please enter a valid integer.");
                } finally {
                    deleteField.setText("");
                }
            }
        });

        // Action listener for Bulk Insert button
        bulkInsertButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String startText = bulkStartField.getText().trim();
                String endText = bulkEndField.getText().trim();
                if (startText.isEmpty() || endText.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "Bulk insert fields are empty.");
                    return;
                }
                try {
                    int start = Integer.parseInt(startText);
                    int end = Integer.parseInt(endText);
                    if (start > end) {
                        JOptionPane.showMessageDialog(null, "Start value should be less than or equal to end value.");
                        return;
                    }
                    for (int key = start; key <= end; key++) {
                        tree.insert(key);
                        // Optional: Add a delay for visualization purposes
                        try {
                            Thread.sleep(50); // 50 milliseconds
                        } catch (InterruptedException ie) {
                            Thread.currentThread().interrupt();
                        }
                    }
                    tree.rotationInfo.clear();
                    tree.colorChanges.clear();
                    drawPanel.repaint();
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Please enter valid integers for bulk insert.");
                }
            }
        });

        setVisible(true);
    }

    // Main method to run the visualizer
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new RedBlackTreeVisualizer();
            }
        });
    }
}