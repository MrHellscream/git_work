import os
import re

def getSoundNames(directory):
    """
    Collects sound file names and their full paths from a given directory, including subdirectories,
    while filtering out names where the base name (without extension) is written in all uppercase letters.

    Args:
        directory (str): Path to the directory containing sound files.

    Returns:
        dict: A dictionary with sound file names (without extensions) as keys
              and their full paths as values.
    """
    sounds = {}

    if not os.path.exists(directory):
        print(f"Error: Unable to open directory '{directory}'.")
        return sounds

    # Walk through directory and subdirectories
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                # Extract the base name (without extension)
                base_name = os.path.splitext(file_name)[0]

                # Skip files if the base name is all uppercase
                if base_name.isupper():
                    continue

                # Add base name as key and full path as value
                sounds[base_name] = file_path

    return sounds


def walk(file_scripts, sounds):
    """
    Checks a list of script files for references to sound names and returns
    the sounds that were not found in any of the scripts.

    Args:
        file_scripts (list): List of file paths to script files.
        sounds (dict): Dictionary of sound names and their file paths.

    Returns:
        dict: A dictionary of sounds that were not found in the script files.
    """
    # Create a copy of sounds to track unused sounds
    unused_sounds = sounds.copy()

    for file_script in file_scripts:
        try:
            with open(file_script, 'r') as script_file:
                script_content = script_file.read()

                # Check for each sound name in the script file's content
                for sound_name in list(unused_sounds.keys()):
                    if sound_name in script_content:
                        unused_sounds.pop(sound_name)

        except OSError as e:
            print(f"Error opening file '{file_script}': {e}")

    return unused_sounds
