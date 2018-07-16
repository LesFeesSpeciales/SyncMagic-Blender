# Copyright (C) 2018 Les Fees Speciales
# voeu@les-fees-speciales.coop
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


"""Apply lipsync to character armature"""

import bpy
import csv
import re

bl_info = {
    "name": "Apply SyncMagic Lipsync",
    "description": "Application du fichier de lipsync SyncMagic au rig sélectionné",
    "author": "Les Fées Spéciales",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > SyncMagic",
    "wiki_url": "https://github.com/LesFeesSpeciales/SyncMagic-Blender/",
    "tracker_url": "https://github.com/LesFeesSpeciales/SyncMagic-Blender/issues",
    "category": "Animation"}


def parse_dialog_file(dialog_file, in_point, out_point):
    dialog_file = dialog_file.split('\n')
    frames = {}
    for f in range(in_point+1, out_point+2):

        line = dialog_file[f]
        position = re.findall(r"\(([0-9]+)\)", line)
        # print(position)
        position = int(position[0])
        frames[f] = position
    return frames


class ApplySyncMagicLipsync(bpy.types.Operator):
    bl_idname = "lfs.apply_lipsync"
    bl_label = "Apply Lipsync"
    bl_description = ""
    bl_options = {"REGISTER"}

    current_shot = bpy.props.IntProperty(
        name="Current shot", description='Shot number'
    )
    scene_list_file = bpy.props.StringProperty(
        name="Scene list file", description='File containing the frame ranges'
    )
    dialog_file = bpy.props.StringProperty(
        name="Dialog file", description='File containing the dialog'
    )
    sound_file = bpy.props.StringProperty(
        name="Sound file", description='Audio dialog file'
    )
    object_data_path = bpy.props.StringProperty(
        name="Object data path",
        description='Blender object data path', default=''
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Absolute paths
        scene_list_file = bpy.path.abspath(self.scene_list_file)
        dialog_file = bpy.path.abspath(self.dialog_file)
        sound_file = bpy.path.abspath(self.sound_file)

        obj = context.object
        scene = context.scene

        # Get shot first frame from scene list
        in_point = -1
        with open(scene_list_file) as scene_list:
            shots = csv.reader(scene_list)
            for s in shots:
                try:
                    shot_number = int(s[0])
                except:
                    continue
                if shot_number == self.current_shot:
                    in_point, out_point = int(s[2]), int(s[3])
                    break

        if in_point == -1:
            self.report(
                {'ERROR'},
                'Shot %i not found in Scene list file' % self.current_shot
            )
            return {'CANCELLED'}
        # Get mouth positions for frame range
        with open(dialog_file) as dialog:
            dialog = dialog.read()
        lines = parse_dialog_file(dialog, in_point, out_point)
        previous_position = -1
        for f, position in lines.items():
            if position != previous_position:
                obj[self.object_data_path] = position
                obj.keyframe_insert(
                    '["{}"]'.format(self.object_data_path),
                    frame=(f - in_point + context.scene.frame_start - 1)
                )
            previous_position = position

        curve = obj.animation_data.action.fcurves.find(
            '["{}"]'.format(self.object_data_path)
        )
        for point in curve.keyframe_points:
            point.interpolation = 'CONSTANT'

        # Add sound to sequence editor
        if self.sound_file:
            if scene.sequence_editor is None:
                scene.sequence_editor_create()
            if "DIALOGUE" in scene.sequence_editor.sequences:
                scene.sequence_editor.sequences.remove(
                    scene.sequence_editor.sequences['DIALOGUE'])
            scene.sequence_editor.sequences.new_sound(
                'DIALOGUE', sound_file, 1,
                context.scene.frame_start - in_point,
            )

            scene.use_audio_scrub = True
            scene.sync_mode = 'AUDIO_SYNC'

        return {"FINISHED"}


class ApplySyncMagicLipsyncPanel(bpy.types.Panel):
    bl_idname = "apply_lipsync_panel"
    bl_label = "SyncMagic"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Animation"

    def draw(self, context):
        scene = context.scene
        settings = scene.lipsync_settings

        layout = self.layout
        box = layout.box()
        row = box.row(align=True)
        icon = 'TRIA_DOWN' if settings.instructions_expand else 'TRIA_RIGHT'
        row.context_pointer_set('settings', settings)
        op = row.operator('wm.context_toggle', text='', icon=icon,
                          emboss=False)
        op.data_path = 'settings.instructions_expand'
        row.label(text='Instructions', icon='INFO')
        if settings.instructions_expand:
            col = box.column(align=True)
            col.label(text='- Convertir le fichier SceneList en CSV')
            col.label(text='- Choisir les fichiers SceneList et de dialogue')
            col.label(text='- Choisir le fichier son (facultatif)')
            col.label(text='- Renseigner le champ « Current shot »')
            col.label(text='  Il correspond à l\'instruction \\beginScene')
            col.label(text='  dans le fichier dialogue')
            col.label(text='- Choisir la propriété (Object data path)')
            col.label(text='  où seront enregistrées les clefs.')
            col.label(text='- Le début de la scène correspond au')
            col.label(text='  réglage Start Frame dans Blender.')

        col = layout.column(align=True)
        col.prop(settings, "scene_list_file", icon="LINENUMBERS_ON")
        col.prop(settings, "dialog_file", icon="MOD_MASK")
        col.prop(settings, "sound_file", icon="FILE_SOUND")
        col.prop(settings, "object_data_path")
        layout.prop(settings, "current_shot")

        layout.separator()
        op = layout.operator("lfs.apply_lipsync")
        op.scene_list_file = settings.scene_list_file
        op.dialog_file = settings.dialog_file
        op.sound_file = settings.sound_file
        op.current_shot = settings.current_shot
        op.object_data_path = settings.object_data_path


class LipsyncSettings(bpy.types.PropertyGroup):
    current_shot = bpy.props.IntProperty(
        name="Current shot", description='Shot number'
    )
    scene_list_file = bpy.props.StringProperty(
        name="Scene list file",
        description='File containing the frame ranges',
        subtype='FILE_PATH', default=''
    )
    dialog_file = bpy.props.StringProperty(
        name="Dialog file",
        description='File containing the dialog',
        subtype='FILE_PATH'
    )
    sound_file = bpy.props.StringProperty(
        name="Sound file",
        description='Audio dialog file',
        subtype='FILE_PATH', default=''
    )
    object_data_path = bpy.props.StringProperty(
        name="Object data path",
        description='Blender object data path',
        default='variation_mouth'
    )
    instructions_expand = bpy.props.BoolProperty(
        name="Ouvrir instructions",
        description='Ouvrir instructions dans le panneau',
        default=False
    )


def register():
    bpy.utils.register_class(LipsyncSettings)
    bpy.types.Scene.lipsync_settings = bpy.props.PointerProperty(
        type=LipsyncSettings
    )
    bpy.utils.register_class(ApplySyncMagicLipsync)
    bpy.utils.register_class(ApplySyncMagicLipsyncPanel)


def unregister():
    del bpy.types.Scene.lipsync_settings
    bpy.utils.unregister_class(LipsyncSettings)
    bpy.utils.unregister_class(ApplySyncMagicLipsyncPanel)
    bpy.utils.unregister_class(ApplySyncMagicLipsync)


if __name__ == "__main__":
    register()
