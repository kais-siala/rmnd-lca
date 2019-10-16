# content of test_activity_maps.py
import pytest
from rmnd_lca.inventory_imports import BaseInventoryImport
from pathlib import Path


def get_db():
    db = [{
            'name':'fake activity',
            'reference product': 'fake product',
            'location':'IAI Area, Africa',
            'unit':'kilogram',
            'exchanges': [
                {'name' : 'fake activity',
                 'product': 'fake product',
                 'amount': 1,
                 'type': 'production',
                 'unit':'kilogram',
                 'input':('dummy_db', '6543541'),},
                {'name' : '1,4-Butanediol',
                 'categories': ('air', 'urban air close to ground'),
                 'amount': 1,
                 'type': 'biosphere',
                 'unit':'kilogram',
                 'input':('dummy_bio', '123'),
                },
            ]
        }]
    version = 3.5
    return db, version


def test_biosphere_dict():
    db, version = get_db()
    testpath = Path("testfile")
    open(testpath, "w")
    dbc = BaseInventoryImport(db, version, testpath)
    assert dbc.biosphere_dict[
               (
                   '1,4-Butanediol',
                   'air',
                   'urban air close to ground',
                   'kilogram'
               )] == '38a622c6-f086-4763-a952-7c6b3b1c42ba'

    testpath.unlink()

def test_biosphere_dict_2():
    db, version = get_db()
    testpath = Path("testfile")
    open(testpath, "w")
    dbc = BaseInventoryImport(db, version, testpath)

    for act in dbc.db:
        for exc in act['exchanges']:
            if exc['type'] == 'biosphere':
                assert dbc.biosphere_dict[(
                    exc['name'],
                    exc['categories'][0],
                    exc['categories'][1],
                    exc['unit']
                )] == '38a622c6-f086-4763-a952-7c6b3b1c42ba'

    testpath.unlink()
