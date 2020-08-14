import bpy
import math

def find_iso_collection(context, item):
    """
    Finds which collection the object is in.
    """
    collections = item.users_collection
    if len(collections) > 0:
        return collections[0]
    return context.scene.collection

def make_iso_collection(collection_name, parent_collection):
    """
    Checks if collection exists otherwise creates it.
    """
    if collection_name in bpy.data.collections: # Checks if collection exists
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection) # Add the new collection under a parent
        return new_collection

def move_iso_objects():
    """
    Moves objects into the Iso_Struct collection based on their names.
    """

    def move(coll_type, list_name):
        for _, x in enumerate(list_name):
            try:
                item = bpy.data.objects[x]
                old_collection = find_iso_collection(bpy.context, item)
                new_collection = make_iso_collection(coll_type, old_collection)
                new_collection.objects.link(item)  # put item in the new collection
                old_collection.objects.unlink(item)  # remove it from the old collection
            except:
                continue

    iso_obj_list =(
        "Iso Right Wall",
        "Iso Left Wall",
        "Iso Floor"
        )

    iso_cam_list = (
        "Isometric Camera",
        "Isometric Game Camera"
        )
    
    iso_hidden_list = (
        "Emission Right",
        "Emission Left",
        "Hidden Ceiling",
        "Hidden Right Wall",
        "Hidden Left Wall",
        "ISO Emission Left",
        "ISO Emission Right"
        )

    move_dict = {
        "Iso Camera": iso_cam_list,
        "Iso Hidden": iso_hidden_list,
        "Iso Structure": iso_obj_list
        }

    for coll_name, list_name in move_dict.items():
        move(coll_name, list_name)
    return

def isoq_light_hypotenuse(height):
    """
    edits length of 'light plane'
    """
    hypotenuse = math.sqrt(2*(height**2))
    return hypotenuse


def isoq_light_distance(scale, height, thickness):
    """
    moves plane to a perfect 45 degree angle to the wall
    """
    half_height = height/2
    half_hypotenuse = isoq_light_hypotenuse(height/2)
    base = half_hypotenuse**2 - half_height**2
    ans = math.sqrt(base)
    return scale/2+thickness+ans


def isoq_plane_emission():
    """
    Applies emission textures to both 'light planes'
    """
    obj_list = ["ISO Emission Left", "ISO Emission Right"]
    def assign_emission(obj):
        if emission_name not in bpy.data.materials:
            iso_emission = bpy.data.materials.new(emission_name)
            obj.active_material = iso_emission
            iso_emission.use_nodes = True
            nodes = iso_emission.node_tree.nodes
            nodes.clear()
            
            # Create needed Nodes
            nodeOut = nodes.new(type='ShaderNodeOutputMaterial')
            nodeEmission = nodes.new(type='ShaderNodeEmission')

            # Link them together
            links = iso_emission.node_tree.links
            linkOut = links.new(nodeEmission.outputs[0], nodeOut.inputs[0])
            bpy.data.materials[emission_name].node_tree.nodes["Emission"].inputs[1].default_value = 30
        else:
            obj.active_material = bpy.data.materials[emission_name]
            
    for _, name in enumerate(obj_list):
        try:
            obj = bpy.data.objects[name]
            emission_name = "ISOQ Emission"
            assign_emission(obj)
        except:
            continue
