import bpy
import sys
import os

# Get the input Blender file path and output STL path from command line arguments
input_blend_path = sys.argv[-2]
output_stl_path = sys.argv[-1]

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=input_blend_path)

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

# Count selected objects and their faces
selected_objects = bpy.context.selected_objects
print(f"Found {len(selected_objects)} mesh objects")
for obj in selected_objects:
    print(f"Object: {obj.name}, Faces: {len(obj.data.polygons)}")

# Export the selected objects as STL
bpy.ops.export_mesh.stl(
    filepath=output_stl_path,
    check_existing=False,
    use_selection=True,
    global_scale=1.0,
    use_scene_unit=True,
    ascii=False,
    use_mesh_modifiers=True
)

print(f"Blender file loaded from: {input_blend_path}")
print(f"STL exported to: {output_stl_path}")

# Verify file size
if os.path.exists(output_stl_path):
    file_size = os.path.getsize(output_stl_path)
    print(f"STL file size: {file_size} bytes")
else:
    print("Error: STL file was not created")