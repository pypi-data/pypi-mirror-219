import jsonpickle
import json

from py_astrolab.types import KerykeionPoint, KerykeionException
from pathlib import Path
from typing import Union, Literal


def get_number_from_name(name: str) -> int:
    """Utility function, gets planet id from the name."""
    name = name.lower()

    if name == "sun":
        return 0
    elif name == "moon":
        return 1
    elif name == "mercury":
        return 2
    elif name == "venus":
        return 3
    elif name == "mars":
        return 4
    elif name == "jupiter":
        return 5
    elif name == "saturn":
        return 6
    elif name == "uranus":
        return 7
    elif name == "neptune":
        return 8
    elif name == "pluto":
        return 9
    elif name == "mean_node":
        return 10  # change!
    elif name == "true_node":
        return 11
    else:
        return int(name)


def calculate_position(degree: Union[int, float], number_name: str, point_type: Literal["Planet", "House", "Axis"]) -> KerykeionPoint:
    """Utility function to create a dictionary deviding
    the houses or the planets list."""

    if degree < 30:
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Fire", "signs": ["Ari"], "sign_num": 0, "position": degree, "abs_pos": degree,
                      "emoji": "♈️", "point_type": point_type}
        if point_type == 'House' and degree > 0:
            dictionary['signs'].append('Tau')

    elif degree < 60:
        result = degree - 30
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Earth", "signs": ["Tau"], "sign_num": 1, "position": result, "abs_pos": degree,
                      "emoji": "♉️", "point_type": point_type}
        if point_type == 'House' and degree > 30:
            dictionary['signs'].append('Gem')
    elif degree < 90:
        result = degree - 60
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Air", "signs": ["Gem"], "sign_num": 2, "position": result, "abs_pos": degree,
                      "emoji": "♊️", "point_type": point_type}
        if point_type == 'House' and degree > 60:
            dictionary['signs'].append('Can')
    elif degree < 120:
        result = degree - 90
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Water", "signs": ["Can"], "sign_num": 3, "position": result, "abs_pos": degree,
                      "emoji": "♋️", "point_type": point_type}
        if point_type == 'House' and degree > 90:
            dictionary['signs'].append('Leo')
    elif degree < 150:
        result = degree - 120
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Fire", "signs": ["Leo"], "sign_num": 4, "position": result, "abs_pos": degree,
                      "emoji": "♌️", "point_type": point_type}
        if point_type == 'House' and degree > 120:
            dictionary['signs'].append('Vir')
    elif degree < 180:
        result = degree - 150
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Earth", "signs": ["Vir"], "sign_num": 5, "position": result, "abs_pos": degree,
                      "emoji": "♍️", "point_type": point_type}
        if point_type == 'House' and degree > 150:
            dictionary['signs'].append('Lib')
    elif degree < 210:
        result = degree - 180
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Air", "signs": ["Lib"], "sign_num": 6, "position": result, "abs_pos": degree,
                      "emoji": "♎️", "point_type": point_type}
        if point_type == 'House' and degree > 180:
            dictionary['signs'].append('Sco')
    elif degree < 240:
        result = degree - 210
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Water", "signs": ["Sco"], "sign_num": 7, "position": result, "abs_pos": degree,
                      "emoji": "♏️", "point_type": point_type}
        if point_type == 'House' and degree > 210:
            dictionary['signs'].append('Sag')
    elif degree < 270:
        result = degree - 240
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Fire", "signs": ["Sag"], "sign_num": 8, "position": result, "abs_pos": degree,
                      "emoji": "♐️", "point_type": point_type}
        if point_type == 'House' and degree > 240:
            dictionary['signs'].append('Cap')
    elif degree < 300:
        result = degree - 270
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Earth", "signs": ["Cap"], "sign_num": 9, "position": result, "abs_pos": degree,
                      "emoji": "♑️", "point_type": point_type}
        if point_type == 'House' and degree > 270:
            dictionary['signs'].append('Aqu')
    elif degree < 330:
        result = degree - 300
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Air", "signs": ["Aqu"], "sign_num": 10, "position": result, "abs_pos": degree,
                      "emoji": "♒️", "point_type": point_type}
        if point_type == 'House' and degree > 300:
            dictionary['signs'].append('Pis')
    elif degree < 360:
        result = degree - 330
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Water", "signs": ["Pis"], "sign_num": 11, "position": result, "abs_pos": degree,
                      "emoji": "♓️", "point_type": point_type}
        if point_type == 'House' and degree > 330:
            dictionary['signs'].append('Ari')
    else:
        raise KerykeionException(
            f'Error in calculating positions! Degrees: {degree}')

    return KerykeionPoint(**dictionary)

def dangerous_json_dump(subject, dump=True, new_output_directory=None):
    """
        Dumps the Kerykeion object to a json file located in the home folder.
        This json file allows the object to be recreated with jsonpickle.
        It's dangerous since it contains local system information.
        """

    OUTPUT_DIR = Path.home()

    try:
        subject.sun
    except:
        subject.__get_all()

    if new_output_directory:
        output_directory_path = Path(new_output_directory)
        json_dir = new_output_directory / \
            f"{subject.name}_kerykeion.json"
    else:
        json_dir = f"{subject.name}_kerykeion.json"

    json_string = jsonpickle.encode(subject)

    if dump:
        json_string = json.loads(json_string.replace(
            "'", '"'))  # type: ignore TODO: Fix this

        with open(json_dir, "w", encoding="utf-8") as file:
            json.dump(json_string, file,  indent=4, sort_keys=True)
            subject.__logger.info(f"JSON file dumped in {json_dir}.")
    else:
        pass
    return json_string