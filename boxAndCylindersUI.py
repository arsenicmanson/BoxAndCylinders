bl_info = {
        "name":"Boxes and Cylinders",
        "author": "ArsenicManson",
        "version":(1,0,0),
        "blender":(5,0,0)}

import bpy
import random
import math

class box_and_cylinders_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Box and Cylinders"
    bl_category = "Box and Cylinder"
    
    bpy.types.Object.box_num = bpy.props.IntProperty(
        name="Number of Boxes",
        description="How many boxes to create",
        default=0,
        min=0,
        max=10
        )
    
    bpy.types.Object.cyl_num = bpy.props.IntProperty(
        name="Number of cylinders",
        description="How many cylinders to create",
        default=0,
        min=0,
        max=10)
    
    def draw(self, context):
        
        layout = self.layout

        layout.label(text="Number of Boxes")
        layout.prop(context.object, "box_num", slider=True)
        
        layout.label(text="Number of Cylinders")
        layout.prop(context.object, "cyl_num", slider=True)

        layout.operator("object.create_exercise", text="Create Boxes")
        
        

class create_Exercise(bpy.types.Operator):
    bl_idname = "object.create_exercise"
    bl_label = "Create Exercise"
    bl_description = "Create Boxes and Cylinders"

    def execute(self, context):
        boxes = context.object.box_num
        cyls = context.object.cyl_num
        
        if(boxes == 0 and cyls == 0):
            return {'CANCELLED'}

        exe = Exercise_Creator(boxes, cyls)
        exe.init_creation()

        return {'FINISHED'}


class Exercise_Creator:
    
    def __init__(self, num_boxes, cyl_num):
        self.num_boxes = num_boxes
        self.cyl_num = cyl_num

    def init_creation(self):
        self.delete_objs()
        cam = bpy.data.objects.get("Camera")
        cam.location = (0, -10, 3)
        cam.rotation_euler = (math.pi / 2, 0, 0)
        
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                print(area.spaces)
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
        
        number_of_cubes = 1
        number_of_cylinders = 1
        
        for rep in range(0, self.num_boxes):
            self.create_cubes()
        
        for rep in range(0, self.cyl_num ):
            self.create_cylinders()


    def delete_objs(self):
        obj_delete = []
        for obj in bpy.context.scene.objects:
            if obj.name.find("Cube") != -1 or obj.name.find("Cylinder") != -1:
                obj_delete.append(obj.name)

        for name in obj_delete:
            delete_obj = bpy.data.objects.get(name)
            bpy.data.objects.remove(delete_obj, do_unlink=True)
            
    def create_cubes(self):
        bpy.ops.mesh.primitive_cube_add(
            size=1.5,
            location=self.define_location(),
            rotation=self.define_rotation()
        )
        
    def create_cylinders(self):
        bpy.ops.mesh.primitive_cylinder_add(
            depth =1.5,
            radius=0.5,
            vertices=64,
            location = self.define_location(),
            rotation = self.define_rotation()
            )
            
        
        
    def define_location(self):
        #minimum,maximum Z = 1,5
        location = (random.uniform(-3,3),random.uniform(-4,4),random.uniform(1,4))
        return location

    def define_rotation(self):
        rotation = (random.random() * 360,random.random() * 360,random.random() * 360)
        return rotation



def register():
    bpy.utils.register_class(box_and_cylinders_panel)
    bpy.utils.register_class(create_Exercise)
    
        
def unregister():
    bpy.utils.unregister_class(box_and_cylinders_panel)
    bpy.utils.unregister_class(create_Exercise)
        
if __name__ == "__main__":
    register()