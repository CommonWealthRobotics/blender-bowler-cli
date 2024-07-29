import bpy
import sys
import os

def ensure_object_mode():
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

# Get the input Blender file path, voxel size, and output STL path from command line arguments
input_blend_path = sys.argv[-3]
voxel_size = float(sys.argv[-2])  # Convert to float
output_stl_path = sys.argv[-1]

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=input_blend_path)

# Ensure we're in object mode
ensure_object_mode()

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

# Apply remesh to selected objects
for obj in bpy.context.selected_objects:
    bpy.context.view_layer.objects.active = obj
    obj.data.remesh_voxel_size = voxel_size
    bpy.ops.object.voxel_remesh()

# Count selected objects and their faces
selected_objects = bpy.context.selected_objects
print(f"Found {len(selected_objects)} mesh objects")
for obj in selected_objects:
    print(f"Object: {obj.name}, Faces: {len(obj.data.polygons)}")

# Export the selected objects as ASCII STL
bpy.ops.export_mesh.stl(
    filepath=output_stl_path,
    check_existing=False,
    use_selection=True,
    global_scale=1.0,
    use_scene_unit=True,
    ascii=True,
    use_mesh_modifiers=True
)

print(f"Blender file loaded from: {input_blend_path}")
print(f"Voxel size used for remesh: {voxel_size}")
print(f"ASCII STL exported to: {output_stl_path}")

# Verify file size and content
if os.path.exists(output_stl_path):
    file_size = os.path.getsize(output_stl_path)
    print(f"STL file size: {file_size} bytes")

    # Print the first few lines of the file to verify it's ASCII
    with open(output_stl_path, 'r') as f:
        print("First 5 lines of the STL file:")
        for i, line in enumerate(f):
            if i >= 5:
                break
            print(line.strip())
else:
    print("Error: STL file was not created")