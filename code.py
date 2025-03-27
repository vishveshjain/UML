import graphviz
import re

# --- split_ascii_diagrams function remains the same as the previous working version ---
def split_ascii_diagrams(ascii_uml):
    """Splits side-by-side ASCII diagrams into separate strings."""
    lines = ascii_uml.strip().splitlines()
    if not lines:
        return []

    separator_indices = []
    if len(lines) > 1:
        potential_seps = [match.start() for match in re.finditer(r'\s{2,}', lines[0])]
        for sep_idx in potential_seps:
            is_consistent_sep = True
            for line in lines[1:]:
                 if len(line) > sep_idx and not line[sep_idx:sep_idx+2].isspace():
                      pass # Loosen check slightly

            next_char_idx = -1
            if len(lines[0]) > sep_idx:
                match_next = re.search(r'\S', lines[0][sep_idx:])
                if match_next:
                    next_char_idx = sep_idx + match_next.start()

            if next_char_idx != -1:
                 separator_indices.append((sep_idx, next_char_idx))

    separator_indices.sort()

    diagram_strings = []
    start_col = 0
    for sep_end, next_start in separator_indices:
        col_lines = [line[start_col:sep_end].rstrip() for line in lines]
        diagram_strings.append("\n".join(col_lines))
        start_col = next_start

    col_lines = [line[start_col:].rstrip() for line in lines]
    diagram_strings.append("\n".join(col_lines))

    diagram_strings = [s for s in diagram_strings if s.strip()]
    return diagram_strings
# --- End of split_ascii_diagrams ---


# --- CORRECTED parse_single_class_ascii ---
def parse_single_class_ascii(class_ascii):
    """Parses a single block of ASCII representing one class diagram."""
    current_class = {}
    lines = class_ascii.strip().splitlines()
    section = 'name' # Tracks current parsing section: name, attributes, methods
    name_found = False

    print(f"--- Parsing Single Diagram Block ---") # Debug
    print(class_ascii)                             # Debug
    print(f"---------------------------------") # Debug

    for line_num, line in enumerate(lines):
        line = line.strip()
        print(f"  Line {line_num}: '{line}' (Section: {section})") # Debug

        if not line:
            continue

        # --- Section switching logic based on separators ---
        if re.match(r"^\+\-+?\+$", line):
            if not name_found:
                # Separator before name (e.g., top border) - do nothing special
                pass
            elif section == 'name':
                # Separator immediately after name line -> Switch to attributes
                print("    Separator found, switching to attributes section") # Debug
                section = 'attributes'
                # Initialize lists now that name is confirmed and section changes
                current_class['attributes'] = []
                current_class['methods'] = []
            elif section == 'attributes':
                # Separator after attributes section -> Switch to methods
                print("    Separator found, switching to methods section") # Debug
                section = 'methods'
            elif section == 'methods':
                 # Separator after methods section (e.g., bottom border) - no state change needed
                 print("    Separator after methods (bottom border)") # Debug
                 pass
            continue # Don't process separator line itself for content

        # --- Content processing logic based on current section ---
        if line.startswith('|') and line.endswith('|'):
            content = line[1:-1].strip() # Get content between '|'

            if not name_found:
                 # First non-empty content is the name
                 if content:
                     print(f"    Found Name: {content}") # Debug
                     current_class['name'] = content
                     name_found = True
                     # Stay in 'name' section until a separator forces switch
            elif section == 'attributes':
                # Any non-empty content in this section is an attribute
                if content:
                    print(f"    Found Attribute: {content}") # Debug
                    # Use setdefault just in case initialization was missed (shouldn't happen now)
                    current_class.setdefault('attributes', []).append(content)
            elif section == 'methods':
                 # Any non-empty content in this section is a method
                 if content:
                    print(f"    Found Method: {content}") # Debug
                    current_class.setdefault('methods', []).append(content)
        else:
             print(f"    Ignoring non-content/border line: {line}") # Debug

    print(f"  Finished parsing block. Result: {current_class if name_found else 'No Name Found'}") # Debug
    return current_class if name_found else None
# --- End of CORRECTED parse_single_class_ascii ---


def ascii_to_uml(ascii_uml, output_file="uml_diagram", view=False):
    """Converts ASCII UML to a visual diagram using graphviz."""
    print("Original ASCII:\n", ascii_uml)
    diagram_strings = split_ascii_diagrams(ascii_uml)
    print(f"\nSplit into {len(diagram_strings)} potential diagram blocks.")

    classes = []
    for i, class_ascii in enumerate(diagram_strings):
        parsed_class = parse_single_class_ascii(class_ascii)
        if parsed_class:
            classes.append(parsed_class)

    print("\nFinal Parsed Classes:", classes)

    if not classes:
         print("No valid classes found to render.")
         return

    dot = graphviz.Digraph('UML', comment='UML Class Diagram', format='png')
    dot.attr('node', shape='rectangle')

    for cls in classes:
        cls.setdefault('attributes', [])
        cls.setdefault('methods', [])

        node_label = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'>\n"
        node_label += f"<TR><TD BGCOLOR='lightblue'>{cls.get('name', 'Unnamed Class')}</TD></TR>\n"
        # --- Attributes Section Rendering ---
        node_label += f"<TR><TD ALIGN='LEFT'>"
        for attr in cls['attributes']:
             attr_safe = graphviz.escape(attr)
             # Display exactly as parsed from ASCII (including +/- prefix)
             node_label += f"{attr_safe}<BR/>"
        node_label += "</TD></TR>\n"
        # --- Methods Section Rendering ---
        node_label += f"<TR><TD ALIGN='LEFT'>"
        for method in cls['methods']:
             method_safe = graphviz.escape(method)
             # Display exactly as parsed from ASCII (including +/- prefix)
             node_label += f"{method_safe}<BR/>"
        node_label += "</TD></TR>\n"
        node_label += "</TABLE>>"

        node_id = cls.get('name', f'Unnamed_{id(cls)}')
        dot.node(node_id, label=node_label)

    print("\nDOT Source:\n", dot.source)  # Debugging

    try:
        dot.render(output_file, view=view, cleanup=True)
        print(f"UML diagram saved to {output_file}.png")
    except graphviz.backend.execute.ExecutableNotFound as e:
        print(f"\nERROR: Graphviz executable not found: {e}")
        print("Please ensure Graphviz is installed and its 'bin' directory is in your system's PATH.")
    except Exception as e:
        print(f"\nError during rendering: {e}")


# Example Usage
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

ascii_to_uml(ascii_uml, output_file="trip_uml", view=True)