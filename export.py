import bpy
import sys
import os

def select_exportable_objects():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and len(obj.data.polygons) > 0:
            obj.select_set(True)
    return any(obj.select_get() for obj in bpy.context.scene.objects)

# Get the input Blender file path and output STL path from command line arguments
input_blend_path = sys.argv[-2]
output_stl_path = sys.argv[-1]

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=input_blend_path)

# Select objects with faces
if not select_exportable_objects():
    print("Error: No mesh objects with faces found in the scene.")
    sys.exit(1)

# Ensure we're in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Apply all transformations
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Recalculate normals
bpy.ops.object.calculate_normals()

# Export the selected objects as STL
try:
    bpy.ops.export_mesh.stl(
        filepath=output_stl_path,
        use_selection=True,
        global_scale=1.0,
        use_scene_unit=True,
        ascii=False,
        use_mesh_modifiers=True
    )
    print(f"Blender file loaded from: {input_blend_path}")
    print(f"STL exported to: {output_stl_path}")
except Exception as e:
    print(f"Error exporting STL: {str(e)}")
    sys.exit(1)

# Verify the exported file
if os.path.exists(output_stl_path) and os.path.getsize(output_stl_path) > 0:
    print("STL file exported successfully.")
else:
    print("Error: STL file was not created or is empty.")
    sys.exit(1)