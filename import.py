import bpy
import sys
import os
import math

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

# Create a camera if it doesn't exist
if not bpy.context.scene.camera:
    bpy.ops.object.camera_add()
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
else:
    camera = bpy.context.scene.camera

# Position the camera to view the object
bound_box = obj.bound_box
center = obj.location
size = max((max(v[i] for v in bound_box) - min(v[i] for v in bound_box)) for i in range(3))
camera.location = (center.x, center.y - size * 2, center.z + size)
camera.rotation_euler = (math.radians(60), 0, 0)

# Set up the scene for rendering (optional)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Save the blend file
bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)

print(f"STL imported from: {input_stl_path}")
print(f"Blender file saved to: {output_blend_path}")