# give_guids.py

## Description

This renames all files matching a sample name to a single guid

## Steps

0. Edit give_guids.py to adjust pattern, suffix and sample name terminating character

1. Get the sample name following {PATTERN}/{SAMPLE_NAME}{SUFFIX} pattern

2. Generate {GUID}

3. Rename all files matching {PATTERN}/{SAMPLE_NAME}* to {GUID}{SUFFIX}

4. Output json array to stdout that can be used by import.py

# import.py

## Description

Parses output of give_guids.py and inserts data into a table

Used mainly for mapping guids to names for arboreta

## Database

Create database:

    sqlite3 db2.sqlite
    CREATE TABLE samples (guid primary key, project, name, path, other_json);
