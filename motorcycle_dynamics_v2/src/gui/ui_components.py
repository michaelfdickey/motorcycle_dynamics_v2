from dearpygui.core import *
from dearpygui.simple import *

def create_ui():
    with window("Motorcycle Dynamics Simulator", width=1200, height=800):
        with group("Button Column", horizontal=False):
            add_button("Start Simulation", callback=start_simulation)
            add_button("Stop Simulation", callback=stop_simulation)
            add_button("Reset", callback=reset_simulation)
            add_button("Settings", callback=open_settings)
        
        with child("Drawing Box", width=800, height=600):
            add_drawlist("drawing_area", width=800, height=600)
            # Additional drawing logic can be added here

def start_simulation():
    # Logic to start the simulation
    pass

def stop_simulation():
    # Logic to stop the simulation
    pass

def reset_simulation():
    # Logic to reset the simulation
    pass

def open_settings():
    # Logic to open settings window
    pass