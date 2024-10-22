import bpy
import sys
import os

def ensure_object_mode():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

# Get the input Blender file path and output STL path from command line arguments
input_blend_path = sys.argv[-2]
output_stl_path = sys.argv[-1]

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=input_blend_path)

# Ensure we're in object mode
ensure_object_mode()

# Select all mesh objects
for obj in bpy.context.scene.collection.all_objects:
    if obj.type == 'MESH':
        obj.select_set(True)

# Count selected objects and their faces
selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
print(f"Found {len(selected_objects)} mesh objects")
for obj in selected_objects:
    print(f"Object: {obj.name}, Faces: {len(obj.data.polygons)}")

# Export the selected objects as ASCII STL
# updated from https://blender.stackexchange.com/questions/322693/how-to-export-combinations-of-models-as-stl
bpy.ops.wm.stl_export(
    filepath=output_stl_path,
    check_existing=False,
    global_scale=1.0,
    use_scene_unit=True
)

print(f"Blender file loaded from: {input_blend_path}")
print(f"ASCII STL exported to: {output_stl_path}")

# Verify file size and content
if os.path.exists(output_stl_path):
    file_size = os.path.getsize(output_stl_path)
    print(f"STL file size: {file_size} bytes")
else:
    print("Error: STL file was not created")
    
    