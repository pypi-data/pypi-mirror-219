#!/usr/bin/env python3
"""
Information about the righty dataset.

To see descriptions of all the types of information available here, run:

  import righty
  righty.info.descriptions

To be sure to print the descriptions formatted nicely, run:

  import righty
  import json
  print(json.dumps(righty.info.descriptions, indent=2))
"""

import numpy as np


# A dictionary to hold descriptions of each object provided in this info file
descriptions = {}

descriptions['github_url'] = 'The URL for the GitHub repo where you can find information and code related to this dataset.'
github_url = 'https://github.com/jasper-tms/righty'

descriptions['dataset_description'] = 'A few sentences describing what this dataset is.'
dataset_description = (
'GridTape-TEM (transmission electron microscopy) dataset of the entire '
'central nervous system (brain and ventral nerve cord) of an adult '
'female fly (Drosophila melanogaster). This electron microscopy '
f'dataset is nicknamed "righty". See {github_url} for more information.'
)

descriptions['sample_info'] = (
    'A dictionary containing some information about the specific fly whose'
    ' nervous system was used to create this dataset'
)
sample_info = {
    'species': 'Drosophila melanogaster',
    'genotype': 'Canton-S x w1118',
    'sex': 'female',
    'age_days': '5-6 days post eclosion',
    'age_hours': '117-146 hours post eclosion'
}

descriptions['contributors'] = 'Who contributed to the generation of this dataset'
contributors = (
    ('Jasper Phelps', 'jasper.s.phelps@gmail.com', 'https://linktr.ee/jasperphelps'),
    ('Minsu Kim', 'minsu_kim@hms.harvard.edu', 'https://twitter.com/mindyisminsu'),
    ('Ryan Maloney', 'TODO', 'TODO'),
    ('Ben de Bivort', 'TODO', 'TODO'),
    ('Wei-Chung Lee', 'wei-chung_lee@hms.harvard.edu', 'https://lee.hms.harvard.edu')
)

descriptions['voxel_size'] = 'The size (in nanometers) of each voxel in the EM dataset. In xyz order'
voxel_size = (4, 4, 45) 

descriptions['shape'] = 'The size (in number of voxels) of the bounding box of the aligned EM dataset. In xyz order'
shape = (249000, 287864, 7010)

descriptions['size'] = 'The size (in nanometers) of the bounding box of the aligned EM dataset. In xyx order'
size = (996000, 1151456, 315450)


descriptions['hms_o2_path'] = "Path to data on Harvard Medical School's O2 cluster filesystem"
hms_o2_path = '/n/groups/htem/temcagt/datasets/righty_r1062'

descriptions['gridtape_reel_number'] = (
    'The unique identifier number of the GridTape reel (see'
    ' https://luxel.com/gridtape/) onto which the sections comprising this'
    ' dataset were collected.'
)
gridtape_reel_number = 1062

descriptions['max_slot_number'] = (
    'The largest slot number onto which a collected section was imaged and'
    ' included in the dataset'
)
max_slot_number = 7070

descriptions['skipped_slots'] = (
    "Slot numbers on the GridTape reel where the microtome didn't cut any"
    ' tissue, meaning there is no image data for these slot numbers, but no'
    ' data was lost. These slots were just skipped over.'
)
skipped_slots = np.array([
    3365, 3501, 3508, 3509, 3510, 3513, 3519, 3523, 3763, 3764, 3765, 3766,
    3767, 3768, 3769, 3770, 3771, 3772, 3773, 3774, 3775, 3776, 3777, 3778,
    3779, 3780, 3781, 3782, 3783, 3784, 3785, 3786, 3787, 3788, 3789, 3790,
    3791, 3792, 3793, 3794, 3795, 3796, 3797, 3798, 3799, 3800, 3801, 3802,
    3803, 3804, 3805, 3806, 3807, 3808, 3809, 3810, 4926, 5040, 5042, 6461,
    6480
])


def slot_to_z(num: int) -> int:
    """ 
    Given a GridTape slot number, return the z slice index where the image data
    from that slot has ended up in the aligned dataset.

    The difference in numbering between the GridTape slots and the aligned
    dataset's z indices accounts for slots that were skipped over during
    section collection because the microtome didn't cut any tissue. This
    includes the 48 skipped slots during the microtome reset and 13 sections of
    spontaneous "empty swings". The renumbering makes it so that there are not
    gaps in the dataset due to the skipped slots.
    """
    if num in skipped_slots:
        raise ValueError(f'{num} is a skipped slot')
    return num - sum(skipped_slots < num)

_z_to_slot = []
def z_to_slot(num: int) -> int:
    """ 
    Given a z slice index in the aligned dataset, return the GridTape slot
    number where the image data for that z slice came from.

    The difference in numbering between the GridTape slots and the aligned
    dataset's z indices accounts for slots that were skipped over during
    section collection because the microtome didn't cut any tissue. This
    includes the 48 skipped slots during the microtome reset and 13 sections of
    spontaneous "empty swings". The renumbering makes it so that there are not
    gaps in the dataset due to the skipped slots.
    """
    if num in skipped_slots:
        raise ValueError(f'{num} is a skipped slot')

    # Only build this mapping when this function is run for the first time
    if len(_z_to_slot) == 0:
        _z_to_slot.extend(list(range(max_slot_number + 1)))
        [_z_to_slot.remove(i) for i in skipped_slots]

    return _z_to_slot[num]


def run_tests():
    # Test that voxel_size * shape == size
    assert all([a * b == c for a, b, c in zip(voxel_size, shape, size)])

    # Test that slot_to_z and z_to_slot are inverses
    for i in range(0, shape[2]):
        try: assert slot_to_z(z_to_slot(i)) == i, i
        except ValueError: pass
    for i in range(0, max_slot_number + 1):
        try: assert z_to_slot(slot_to_z(i)) == i, i
        except ValueError: pass

    # Test that shape.z is correct
    assert shape[2] == slot_to_z(max_slot_number) + 1
    assert z_to_slot(shape[2] - 1) == max_slot_number

    print('Success')
    return True
