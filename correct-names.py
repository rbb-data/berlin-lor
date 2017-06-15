#!/usr/bin/env python3

"""
Unfortunately some of the area names are not converted
correctly in our toolchain of gdal | iconv (| topojson).
This script tries to straighten that out.
"""

import csv
import glob
import json
import re
from os.path import basename

csv_files = glob.glob('LOR-Schluesselsystematik/*.csv')

multiple_spaces = re.compile(r'\s+')
only_uppercase = re.compile(r'^[A-Z\s\d]+$')


def clean_name(name):
    """
    Clean names that have too much spacing, inconsistent whitespace
    around slashes or inconsistent capitalization
    """
    cleaned = multiple_spaces.sub(' ', name)
    # fix spacing around dashes and slashes:
    cleaned = '/'.join([w.strip() for w in cleaned.split('/')])
    cleaned = '-'.join([w.strip() for w in cleaned.split('-')])
    return cleaned if only_uppercase.match(cleaned) else cleaned.title()


# we build a dictionary where we can look up the correct names:
id_mappings = {}
for f in csv_files:
    prefix = basename(f)[:2]
    reader = csv.reader(open(f, 'r'), delimiter=';')

    # skip the first 4 columns
    for _ in range(4):
        next(reader)

    current_pgr = '00'
    current_bzr = '00'
    current_plr = '00'  # for the sake of readability

    for row in reader:
        pgr = row[4].strip()
        if pgr != '' and pgr != current_pgr:
            current_pgr = pgr.zfill(2)
            id_mappings[prefix + current_pgr] = clean_name(row[5])

        bzr = row[7].strip()
        if bzr != '' and bzr != current_bzr:
            current_bzr = bzr.zfill(2)
            name = clean_name(row[8])
            id_mappings[prefix + current_pgr + current_bzr] = name

        plr = row[10].strip()
        if plr != '':
            current_plr = plr.zfill(2)
            name = clean_name(row[11])
            id_mappings[prefix + current_pgr + current_bzr + current_plr] = name # noqa

# 🔧🔧🔧

json_files = glob.glob('berlin-lor*json')
for j in json_files:
    print('🚂 Processing {}'.format(j))

    data = json.load(open(j, 'r'))
    if '.geojson' in j:
        for i, feature in enumerate(data['features']):
            keys = feature['properties'].keys()
            name_key = [k for k in keys if '_NAME' in k][0]
            given_name = feature['properties'][name_key]

            # some shapes don't have a name (wtf?)
            if not given_name:
                print('🤔 Entry {} doesn\'t have a name, skipping it'.format(i)) # noqa
                continue

            try:
                correct_name = id_mappings[feature['properties']['SCHLUESSEL']]
            except:
                print('🤔 Unknown key ({}) for entry {}'.format(
                    feature['properties']['SCHLUESSEL'], i))

            if (given_name != correct_name):
                # print('🔧 Fixing {} to {}'.format(given_name, correct_name))
                data['features'][i]['properties'][name_key] = correct_name
    else:
        x = list(data['objects'].keys())[0]
        for i, geom in enumerate(data['objects'][x]['geometries']):
            keys = geom['properties'].keys()
            name_key = [k for k in keys if '_NAME' in k][0]
            given_name = geom['properties'][name_key]

            # some shapes don't have a name (wtf?)
            if not given_name:
                print('🤔 Entry {} doesn\'t have a name, skipping it'.format(i)) # noqa
                continue
            try:
                correct_name = id_mappings[geom['properties']['SCHLUESSEL']]
            except:
                print('🤔 Unknown key ({}) for entry {}'.format(
                    feature['properties']['SCHLUESSEL'], i))

            if (given_name != correct_name):
                # print('🔧 Fixing {} to {}'.format(given_name, correct_name))
                data['objects'][x]['geometries'][i]['properties'][name_key] = correct_name # noqa

    json.dump(data, open(j, 'w'))
    print('✏️ Wrote result to {}'.format(j))
    print()
