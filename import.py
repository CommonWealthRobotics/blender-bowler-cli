import bpy
import sys
import os

# Get the input STL file path and output Blender file path from command line arguments
input_stl_path = sys.argv[-2]
output_blend_path = sys.argv[-1]

# Clear the default cube (if it exists)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the STL file
bpy.ops.import_mesh.stl(filepath=input_stl_path)

# Select the imported object and center it
obj = bpy.context.selected_objects[0]
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
bpy.ops.view3d.camera_to_view_selected()

# Save the blend file
bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)

print(f"STL imported from: {input_stl_path}")
print(f"Blender file saved to: {output_blend_path}")