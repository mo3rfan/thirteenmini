# export.py
import sys
import os
import FreeCAD

def export_stl(doc, base_name, output_dir="dist"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Filter for the specific object "Body002"
    objs_to_export = [obj for obj in doc.Objects if obj.Name == "Body002"]
    
    if not objs_to_export:
        print("Error: Object 'Body002' not found in document.")
        return

    stl_path = os.path.join(output_dir, f"{base_name}.stl")
    
    try:
        import Mesh
        Mesh.export(objs_to_export, stl_path)
        print(f"Exported STL for Body002 to {stl_path}")
    except Exception as e:
        print(f"Error exporting STL: {e}")




def main():
    fcstd_file = None
    for arg in sys.argv:
        if arg.lower().endswith(".fcstd"):
            fcstd_file = arg
            break

    if not fcstd_file:
        print("Usage: FreeCADCmd -c export.py <file.FCStd>")
        return

    base_name = os.path.splitext(os.path.basename(fcstd_file))[0]

    if not os.path.exists(fcstd_file):
        print(f"Error: File not found at {fcstd_file}")
        return

    try:
        doc = FreeCAD.open(fcstd_file)
        if not doc:
            print(f"Error: Could not open file {fcstd_file}")
            return
            
        print(f"Successfully opened {fcstd_file}")
        
        # Calculate output directories relative to the input file
        base_dir = os.path.dirname(os.path.abspath(fcstd_file))
        dist_dir = os.path.join(base_dir, "dist")
        export_stl(doc, base_name, output_dir=dist_dir)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'doc' in locals() and doc:
            FreeCAD.closeDocument(doc.Name)

main()
