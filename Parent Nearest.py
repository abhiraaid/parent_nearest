bl_info = {
    "name": "Parent Nearest",
    "description": "Parent Objects by Position, Rotation, and Scale with Suffix",
    "author": "abhiraaid",
    "blender": (4, 2, 0),
    "category": "Object",
}

import bpy

class OBJECT_OT_ParentByPositionRotation(bpy.types.Operator):
    bl_idname = "object.parent_by_position_rotation"
    bl_label = "Parent Nearest"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        check_rotation = context.window_manager.parent_by_position_rotation_check_rotation
        check_scale = context.window_manager.parent_by_position_rotation_check_scale
        suffix = context.window_manager.parent_by_position_rotation_suffix
        selected_objects = context.selected_objects

        for obj in selected_objects:
            child_assigned = False
            for other in context.scene.objects:
                if other != obj and other.parent != obj:
                    if obj.location == other.location:
                        rotation_match = not check_rotation or obj.rotation_euler == other.rotation_euler
                        scale_match = not check_scale or obj.scale == other.scale
                        if rotation_match and scale_match and not child_assigned:
                            # Keep the transform of the child object
                            other_matrix_world = other.matrix_world.copy()
                            other.parent = obj
                            other.matrix_world = other_matrix_world
                            # Rename the child object with the specified suffix
                            other.name = f"{other.name}{suffix}"
                            # Toggle visibility of the child object
                            other.hide_set(True)
                            other.hide_render = True  # Remove from render
                            child_assigned = True
                        elif rotation_match and scale_match and child_assigned:
                            # If multiple matching child objects found, unparent them
                            other.parent = None
        
        return {'FINISHED'}

class OBJECT_PT_ParentByPositionRotationPanel(bpy.types.Panel):
    bl_label = "Parent Nearest"
    bl_idname = "OBJECT_PT_parent_by_position_rotation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.prop(wm, "parent_by_position_rotation_check_rotation")
        layout.prop(wm, "parent_by_position_rotation_check_scale")
        layout.prop(wm, "parent_by_position_rotation_suffix")
        layout.operator("object.parent_by_position_rotation")

def register():
    bpy.utils.register_class(OBJECT_OT_ParentByPositionRotation)
    bpy.utils.register_class(OBJECT_PT_ParentByPositionRotationPanel)
    bpy.types.WindowManager.parent_by_position_rotation_check_rotation = bpy.props.BoolProperty(
        name="Check Rotation",
        description="Consider rotation when finding matching objects",
        default=True,
    )
    bpy.types.WindowManager.parent_by_position_rotation_check_scale = bpy.props.BoolProperty(
        name="Check Scale",
        description="Consider scale when finding matching objects",
        default=True,
    )
    bpy.types.WindowManager.parent_by_position_rotation_suffix = bpy.props.StringProperty(
        name="Suffix",
        description="Suffix to add to child objects",
        default="_child"
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ParentByPositionRotation)
    bpy.utils.unregister_class(OBJECT_PT_ParentByPositionRotationPanel)
    del bpy.types.WindowManager.parent_by_position_rotation_check_rotation
    del bpy.types.WindowManager.parent_by_position_rotation_check_scale
    del bpy.types.WindowManager.parent_by_position_rotation_suffix

if __name__ == "__main__":
    register()
