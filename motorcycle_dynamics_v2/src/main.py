# File: motorcycle_dynamics_v2/src/main.py

import dearpygui.dearpygui as dpg
from gui.ui_components import create_ui

def main():
    dpg.create_context()
    create_ui()
    dpg.create_viewport(title="Motorcycle Dynamics Simulator", width=1200, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()