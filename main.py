import dearpygui.dearpygui as dpg
import math
import os

# Initialize DearPyGui
dpg.create_context()

# Font configuration
with dpg.font_registry():
    # Try to find Arial on the system
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",  # Windows
        "/Library/Fonts/Arial.ttf",    # macOS
        "/usr/share/fonts/truetype/msttcorefonts/arial.ttf"  # Some Linux
    ]
    
    arial_path = None
    for path in font_paths:
        if os.path.exists(path):
            arial_path = path
            break
    
    if arial_path:
        # Load Arial with various sizes
        default_font = dpg.add_font(arial_path, 14)
        large_font = dpg.add_font(arial_path, 18)
        small_font = dpg.add_font(arial_path, 12)
        dpg.bind_font(default_font)
    else:
        print("Arial font not found, using default font")

dpg.create_viewport(title="Motorcycle Dynamics Simulator", width=1200, height=800)

# Global variables
nodes = []
beams = []
fixtures = []
masses = []
selected_tool = None
selected_node = None

# Configuration
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 750
SIDEBAR_WIDTH = 200
GRID_COLOR = (50, 50, 50, 255)
GRID_SPACING = 20  # pixels between grid lines
NODE_COLOR = (255, 255, 0, 255)  # Yellow
SELECTED_NODE_COLOR = (0, 255, 0, 255)  # Green
BEAM_COLOR = (200, 200, 200, 255)  # Light gray
FIXTURE_COLOR = (0, 0, 255, 255)  # Blue
MASS_COLOR = (255, 0, 0, 255)  # Red

# Drawing functions
def draw_grid():
    """Draw a grid on the canvas"""
    # Get the size of the drawing area
    width = CANVAS_WIDTH
    height = CANVAS_HEIGHT
    
    # Draw vertical grid lines
    for x in range(0, width, GRID_SPACING):
        dpg.draw_line((x, 0), (x, height), color=GRID_COLOR, parent="canvas")
    
    # Draw horizontal grid lines
    for y in range(0, height, GRID_SPACING):
        dpg.draw_line((0, y), (width, y), color=GRID_COLOR, parent="canvas")

def draw_nodes():
    """Draw all nodes on the canvas"""
    for i, node in enumerate(nodes):
        x, y = node["pos"]
        color = SELECTED_NODE_COLOR if node.get("selected", False) else NODE_COLOR
        dpg.draw_circle((x, y), 5, color=color, fill=color, parent="canvas")
        if 'small_font' in globals():
            dpg.draw_text((x + 10, y), f"N{i}", color=(255, 255, 255, 255), parent="canvas", size=12)
        else:
            dpg.draw_text((x + 10, y), f"N{i}", color=(255, 255, 255, 255), parent="canvas")

def draw_beams():
    """Draw all beams on the canvas"""
    for beam in beams:
        if beam["start"] < len(nodes) and beam["end"] < len(nodes):
            start_pos = nodes[beam["start"]]["pos"]
            end_pos = nodes[beam["end"]]["pos"]
            dpg.draw_line(start_pos, end_pos, color=BEAM_COLOR, thickness=2, parent="canvas")

def draw_fixtures():
    """Draw all fixtures on the canvas"""
    for fixture in fixtures:
        if fixture["node"] < len(nodes):
            node_pos = nodes[fixture["node"]]["pos"]
            dpg.draw_circle(node_pos, 8, color=FIXTURE_COLOR, thickness=2, parent="canvas")

def draw_masses():
    """Draw all masses on the canvas"""
    for mass in masses:
        if mass["node"] < len(nodes):
            node_pos = nodes[mass["node"]]["pos"]
            dpg.draw_circle(node_pos, 8, color=MASS_COLOR, thickness=2, parent="canvas")
            if 'small_font' in globals():
                dpg.draw_text((node_pos[0] + 10, node_pos[1] + 10), f"{mass['value']}kg", color=(255, 255, 255, 255), parent="canvas", size=12)
            else:
                dpg.draw_text((node_pos[0] + 10, node_pos[1] + 10), f"{mass['value']}kg", color=(255, 255, 255, 255), parent="canvas")

def draw_everything():
    """Clear canvas and redraw all elements"""
    dpg.delete_item("canvas", children_only=True)
    draw_grid()
    draw_beams()
    draw_nodes()
    draw_fixtures()
    draw_masses()

# Callback functions
def add_node_callback():
    global selected_tool
    selected_tool = "node"
    print("Node tool selected")
    # Highlight the active tool button
    highlight_active_tool_button("Add Node")

def add_beam_callback():
    global selected_tool
    selected_tool = "beam"
    print("Beam tool selected")
    highlight_active_tool_button("Add Beam")

def add_fixture_callback():
    global selected_tool
    selected_tool = "fixture"
    print("Fixture tool selected")
    highlight_active_tool_button("Add Fixture")

def add_mass_callback():
    global selected_tool
    selected_tool = "mass"
    print("Mass tool selected")
    highlight_active_tool_button("Add Mass")

def delete_callback():
    global selected_tool
    selected_tool = "delete"
    print("Delete tool selected")
    highlight_active_tool_button("Delete")

def clear_all_callback():
    global nodes, beams, fixtures, masses
    nodes = []
    beams = []
    fixtures = []
    masses = []
    print("All entities cleared")
    draw_everything()

def highlight_active_tool_button(active_button_label):
    """Highlight the active tool button and reset others"""
    buttons = ["Add Node", "Add Beam", "Add Fixture", "Add Mass", "Delete"]
    
    for button in buttons:
        if button == active_button_label:
            dpg.configure_item(f"{button}_button", background_color=(0, 100, 0))
        else:
            dpg.configure_item(f"{button}_button", background_color=(0, 0, 0, 0))

def canvas_click(sender, app_data):
    """Handle mouse clicks on the canvas"""
    print(f"Raw app_data: {app_data}")
    
    # Get viewport mouse position
    viewport_pos = dpg.get_mouse_pos(local=False)
    print(f"Viewport mouse position: {viewport_pos}")
    
    # Get canvas position within the window
    canvas_pos = dpg.get_item_pos("canvas")
    canvas_rect = dpg.get_item_rect_size("canvas")
    print(f"Canvas position: {canvas_pos}, canvas size: {canvas_rect}")
    
    # Calculate mouse position relative to canvas
    canvas_window_pos = dpg.get_item_pos("canvas_window")
    canvas_window_rect = dpg.get_item_rect_size("canvas_window")
    print(f"Canvas window position: {canvas_window_pos}, size: {canvas_window_rect}")
    
    # Calculate adjusted position
    x = viewport_pos[0] - canvas_window_pos[0]
    y = viewport_pos[1] - canvas_window_pos[1]
    
    # Account for window borders and any other offset
    x -= 8  # Adjust if needed
    y -= 30  # Adjust for title bar height
    
    print(f"Canvas clicked at calculated position: {x}, {y}")
    
    # Ensure coordinates are within canvas bounds
    if x < 0 or y < 0 or x > CANVAS_WIDTH or y > CANVAS_HEIGHT:
        print(f"Click outside canvas bounds, ignoring")
        return
    
    # Handle different tool actions
    if selected_tool == "node":
        nodes.append({"pos": (x, y), "selected": False})
        print(f"Added node at {x}, {y}")
    elif selected_tool == "beam" and len(nodes) >= 1:
        # Find closest node
        closest_idx = find_closest_node(x, y)
        if closest_idx is not None:
            handle_beam_selection(closest_idx)
    elif selected_tool == "fixture" and len(nodes) > 0:
        closest_idx = find_closest_node(x, y)
        if closest_idx is not None:
            # Check if there's already a fixture on this node
            fixture_exists = False
            for fixture in fixtures:
                if fixture["node"] == closest_idx:
                    fixture_exists = True
                    break
                    
            if not fixture_exists:
                fixtures.append({"node": closest_idx})
                print(f"Added fixture to node {closest_idx}")
            else:
                print(f"Node {closest_idx} already has a fixture")
    elif selected_tool == "mass" and len(nodes) > 0:
        closest_idx = find_closest_node(x, y)
        if closest_idx is not None:
            # Check if there's already a mass on this node
            mass_exists = False
            for mass in masses:
                if mass["node"] == closest_idx:
                    mass_exists = True
                    break
                    
            if not mass_exists:
                # Get mass value from input field
                mass_value = dpg.get_value("mass_value_input")
                masses.append({"node": closest_idx, "value": mass_value})
                print(f"Added {mass_value}kg mass to node {closest_idx}")
            else:
                print(f"Node {closest_idx} already has a mass")
    elif selected_tool == "delete":
        # Check for deletion of a node
        node_idx = find_closest_node(x, y)
        if node_idx is not None:
            # Delete any beams connected to this node first
            beams_to_keep = []
            for beam in beams:
                if beam["start"] != node_idx and beam["end"] != node_idx:
                    beams_to_keep.append(beam)
            beams.clear()
            beams.extend(beams_to_keep)
            
            # Delete any fixtures on this node
            fixtures_to_keep = []
            for fixture in fixtures:
                if fixture["node"] != node_idx:
                    fixtures_to_keep.append(fixture)
            fixtures.clear()
            fixtures.extend(fixtures_to_keep)
            
            # Delete any masses on this node
            masses_to_keep = []
            for mass in masses:
                if mass["node"] != node_idx:
                    masses_to_keep.append(mass)
            masses.clear()
            masses.extend(masses_to_keep)
            
            # Delete the node
            nodes.pop(node_idx)
            print(f"Deleted node {node_idx} and related elements")
            
            # Adjust indices in beams, fixtures and masses
            for beam in beams:
                if beam["start"] > node_idx:
                    beam["start"] -= 1
                if beam["end"] > node_idx:
                    beam["end"] -= 1
            
            for fixture in fixtures:
                if fixture["node"] > node_idx:
                    fixture["node"] -= 1
            
            for mass in masses:
                if mass["node"] > node_idx:
                    mass["node"] -= 1
    
    draw_everything()

def find_closest_node(x, y, max_distance=15):
    """Find index of the closest node to the given coordinates"""
    min_dist = float('inf')
    closest_idx = None
    
    for i, node in enumerate(nodes):
        node_x, node_y = node["pos"]
        dist = math.sqrt((x - node_x)**2 + (y - node_y)**2)
        if dist < min_dist and dist <= max_distance:
            min_dist = dist
            closest_idx = i
            
    return closest_idx

def handle_beam_selection(node_idx):
    """Handle selection of nodes for beam creation"""
    global selected_node
    
    for node in nodes:
        node["selected"] = False
    
    # If no node is selected, select this one
    if selected_node is None:
        selected_node = node_idx
        nodes[node_idx]["selected"] = True
        print(f"Selected node {node_idx} for beam start")
    # If this is a different node, create a beam
    elif selected_node != node_idx:
        beams.append({"start": selected_node, "end": node_idx})
        print(f"Added beam from node {selected_node} to node {node_idx}")
        nodes[selected_node]["selected"] = False
        selected_node = None
    # If it's the same node, deselect it
    else:
        nodes[node_idx]["selected"] = False
        selected_node = None
        print("Deselected node")

# Create GUI
with dpg.window(label="Motorcycle Dynamics Simulator", tag="main_window", no_close=True):
    with dpg.group(horizontal=True):
        # Left sidebar for tools
        with dpg.child_window(width=SIDEBAR_WIDTH, height=CANVAS_HEIGHT, tag="sidebar"):
            dpg.add_text("Tools", color=(255, 255, 0))
            dpg.add_separator()
            with dpg.group():
                dpg.add_button(label="Add Node", callback=add_node_callback, width=180, tag="Add Node_button")
                dpg.add_button(label="Add Beam", callback=add_beam_callback, width=180, tag="Add Beam_button")
                dpg.add_button(label="Add Fixture", callback=add_fixture_callback, width=180, tag="Add Fixture_button")
                dpg.add_button(label="Add Mass", callback=add_mass_callback, width=180, tag="Add Mass_button")
                dpg.add_separator()
                dpg.add_button(label="Delete", callback=delete_callback, width=180, tag="Delete_button")
                dpg.add_button(label="Clear All", callback=clear_all_callback, width=180)
            
            dpg.add_separator()
            dpg.add_text("Properties")
            # Add property editors here later (mass value, etc.)
            
            # Mass value editor
            with dpg.group(horizontal=True):
                dpg.add_text("Mass Value (kg): ")
                dpg.add_input_int(default_value=100, tag="mass_value_input", width=100)

            dpg.add_separator()
            dpg.add_text("Statistics")
            dpg.add_text("Nodes: 0", tag="node_stats")
            dpg.add_text("Beams: 0", tag="beam_stats")
            dpg.add_text("Fixtures: 0", tag="fixture_stats")
            dpg.add_text("Masses: 0", tag="mass_stats")
        
        # Main drawing canvas
        with dpg.child_window(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, tag="canvas_window"):
            with dpg.drawlist(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, tag="canvas"):
                # Initialize with grid
                draw_grid()
                
                # Handle mouse clicks on the canvas
                with dpg.item_handler_registry(tag="canvas_handler"):
                    dpg.add_item_clicked_handler(callback=canvas_click)
                dpg.bind_item_handler_registry("canvas", "canvas_handler")

# Set up viewport
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)

# Update statistics periodically
def update_stats():
    dpg.set_value("node_stats", f"Nodes: {len(nodes)}")
    dpg.set_value("beam_stats", f"Beams: {len(beams)}")
    dpg.set_value("fixture_stats", f"Fixtures: {len(fixtures)}")
    dpg.set_value("mass_stats", f"Masses: {len(masses)}")

# Start main loop
while dpg.is_dearpygui_running():
    update_stats()
    dpg.render_dearpygui_frame()

dpg.destroy_context()