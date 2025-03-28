# ASCII UML to Visual UML Converter

## Overview
This project provides a Python-based solution to convert ASCII art UML diagrams into graphical UML diagrams using **Graphviz**. It is designed to enhance the visualization of UML class diagrams from text-based representations to high-quality images.

## Features
- Parses ASCII UML diagrams into structured data.
- Generates graphical UML diagrams with nodes for classes, attributes, and methods.
- Uses `Graphviz` for diagram rendering.

## Installation
1. Install Python dependencies:
   ```bash
   pip install graphviz
Install Graphviz system-level executables:

For Windows, download from Graphviz and add the bin directory to your system's PATH.

For macOS, use Homebrew:
  ```bash
    brew install graphviz
```
For Linux, use your package manager (e.g., apt-get install graphviz).
Usage
Example Code
Run the following Python script to convert ASCII UML diagrams:
```
import graphviz

# Example function to convert ASCII UML to Graphical UML
def ascii_to_uml(ascii_uml, output_file="uml_diagram", view=False):
    # Implementation here
    pass

ascii_uml = """
+---------------------+
| InputData           |
+---------------------+
| - distanceField     |
| - gasolineCostField |
+---------------------+
"""
ascii_to_uml(ascii_uml, output_file="uml_diagram")
```

## Screenshots:

# Example Usage
```
ascii_uml = """
+-------------------------+       +-----------------------------+
|      InputData          |       |         TripPost            |
+-------------------------+       +-----------------------------+
| - distanceField         |       | - distance                  |
| - gasolineCostField     |       | - gasolineCost              |
| - gasMileageField       |       | - gasMileage                |
| - hotelCostField        |       | - hotelCost                 |
| - foodCostField         |       | - foodCost                  |
| - daysField             |       | - days                      |
| - attractionsField      |       | - attractions               |
| - resultField           |       +-----------------------------+
| - distanceUnit          |       | calculateTotalCost()        |
| - gasolineCostUnit      |       +-----------------------------+
| - gasMileageUnit        |
+-------------------------+
| + InputData()           |
| - calculateTripCost()   |
| - kilometersToMiles()   |
| - litersToGallons()     |
| - kmPerLiterToMilesPerGallon()|
+-------------------------+
"""
```

![trip_uml](https://github.com/user-attachments/assets/c095aaca-b28e-416f-b1e9-eecd666bacbc)



