# motorcycle_dynamics_v2
This project is a motorcycle dynamics simulator designed to model the behavior of two-wheel single track vehicles. 

## Overview
The simulator provides a user-friendly interface for visualizing and interacting with motorcycle dynamics. Users can manipulate various parameters and observe the effects on the motorcycle's behavior in real-time.

## Project Structure
- **src/**: Contains the source code for the application.
  - **main.py**: Entry point of the application.
  - **gui/**: Contains user interface components.
    - **ui_components.py**: Functions to create the user interface layout.
  - **simulation/**: Contains the simulation logic and models.
    - **dynamics.py**: Logic for motorcycle dynamics simulation.
    - **models.py**: Data models related to motorcycle dynamics.
  - **utils/**: Contains utility functions.
    - **helpers.py**: Helper functions for various tasks.

- **assets/**: Contains assets used in the project.
  - **fonts/**: Directory for font files.
    - **default_font.ttf**: Default font for the user interface.

- **requirements.txt**: Lists the dependencies required for the project.

## Setup Instructions
1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the application by executing the `main.py` file:
```
python src/main.py
```
This will launch the motorcycle dynamics simulator, allowing you to interact with the user interface and explore motorcycle dynamics.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.