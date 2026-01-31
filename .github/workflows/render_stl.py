import pyvista as pv
import sys
import os

def render_stl(stl_path, output_dir):
    if not os.path.exists(stl_path):
        print(f"Error: STL file not found at {stl_path}")
        sys.exit(1)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading STL from {stl_path}...")
    mesh = pv.read(stl_path)
    
    # Setup plotter
    # window_size defines the image resolution
    plotter = pv.Plotter(off_screen=True, window_size=[1280, 720])
    plotter.set_background('white')
    
    # Add mesh with some nice default styling
    plotter.add_mesh(mesh, color='lightblue', lighting=True, show_edges=False)
    
    views = {
        "iso": plotter.view_isometric,
        "top": plotter.view_xy,       # Top view (looking down Z)
        "front": plotter.view_xz,     # Front view (looking down Y)
        "side": plotter.view_yz       # Side view (looking down X)
    }

    for name, view_func in views.items():
        try:
            view_func()
            plotter.camera.zoom(1.2) # Zoom in slightly to fit better
            output_path = os.path.join(output_dir, f"screenshot_{name}.png")
            plotter.screenshot(output_path)
            print(f"Saved {name} view to {output_path}")
        except Exception as e:
            print(f"Failed to render {name} view: {e}")
            
    plotter.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_stl.py <path_to_stl> <output_dir>")
        # Clean exit if run without args for testing imports
        sys.exit(0)
        
    render_stl(sys.argv[1], sys.argv[2])
