import bpy
import sys
import os
import math

try:
    # Get the input STL file path and output Blender file path from command line arguments
    input_stl_path = sys.argv[-2]
    output_blend_path = sys.argv[-1]

    # Check if the output Blender file already exists
    if os.path.exists(output_blend_path):
        # Load the existing Blender file
        bpy.ops.wm.open_mainfile(filepath=output_blend_path)
        print("Add mesh to EXISTING file")
    else:
        # Clear the default cube (if it exists)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        print("DELETE objects for new file")

    # Import the STL file
    bpy.ops.import_mesh.stl(filepath=input_stl_path)

    # Select the imported object and center it
    imported_obj = bpy.context.selected_objects[0]
    bpy.ops.object.select_all(action='DESELECT')
    imported_obj.select_set(True)
    bpy.context.view_layer.objects.active = imported_obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Create a camera if it doesn't exist
    if not bpy.context.scene.camera:
        bpy.ops.object.camera_add()
        camera = bpy.context.active_object
        bpy.context.scene.camera = camera
    else:
        camera = bpy.context.scene.camera

    # Position the camera to view the imported object
    bound_box = imported_obj.bound_box
    center = imported_obj.location
    size = max((max(v[i] for v in bound_box) - min(v[i] for v in bound_box)) for i in range(3))
    camera.location = (center.x, center.y - size * 2, center.z + size)
    camera.rotation_euler = (math.radians(60), 0, 0)

    # Set up the scene for rendering (optional)
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    # Save the blend file
    bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)
    #
    print(f"STL imported from: {input_stl_path}")
    print(f"Blender file saved to: {output_blend_path}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    # Optionally, you can print more detailed error information:
    import traceback
    print("Detailed error information:")
    print(traceback.format_exc())