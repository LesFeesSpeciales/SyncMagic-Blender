# SyncMagic Blender

Cet addon permet l'import de fichiers de dialogues créés par l'entreprise
[SyncMagic](http://syncmagic.com/). Il est adapté au
[workflow 2D](http://syncmagic.com/content/2d/Lipsync2D.pdf), où le
fichier comprend une forme de bouche par image.

### Usage

* Convertir le fichier SceneList au format CSV.
* Dans la boîte à outils de la Vue 3D (Toolbox, panneau `T`),
  onglet *Animation* :
  * Choisir les fichiers SceneList et de dialogue.
  * Choisir le fichier son (facultatif).
  * Renseigner le champ « *Current shot* ». Il correspond à l'instruction
    `\beginScene` dans le fichier dialogue.
  * Choisir la propriété (*Object data path*) où seront enregistrées les clefs
    dans l'objet actif.
  * Cliquer sur *Apply Lipsync*.
  * Une propriété animée est créée dans l'objet actif. Elle est accessible
    depuis le panneau *Custom Properties* des propriétés d'objet,
    et dans le panneau N de la vue 3D. Elle peut être utilisée comme cible
    pour contrôler (*driver*) n'importe quelle propriété.
  * Le début de la scène correspond au réglage *Start Frame* dans Blender.

### Avertissement
Cet addon n'est prévu que pour les cas simples où une seule propriété est animée,
et pas pour les personnages en 3D ayant des rigs faciaux complexes.

## Licence

Les scripts pour Blender publiés par **Les Fées Spéciales** le sont, sauf
mention contraire, sous licence GPLv2.

-----

## EN

This addon allows importing dialog files created by the
[SyncMagic](http://syncmagic.com/) company. It is well suited for their
[2D workflow](http://syncmagic.com/content/2d/Lipsync2D.pdf),
wherein the file contains one mouthshape per frame.

### Usage

* Convert the SceneList file to CSV format.
* In the 3D View's Toolbox (`T` panel), *Animation* category:
  * Choose the SceneList and dialog files.
  * Optionally, choose the sound file.
  * Fill in the *Current shot* field. It corresponds to the `\beginScene`
    instruction in the dialog file.
  * Choose the property (*Object data path*) to store the keys in.
  * Click the *Apply Lipsync* button.
  * An animated property is created for the active object. It is displayed in
    the *Custom Properties* panel under the Object Properties, as well as in
    the 3D View's N Panel. It can be used as a driver target for any
    property.
  * The scene will start at Blender's *Start Frame*.

### Warning
This script currently only works for simple animated properties, not for 3D
characters including complex rigs.

## License

Blender scripts shared by **Les Fées Spéciales** are, except where otherwise
noted, licensed under the GPLv2 license.
