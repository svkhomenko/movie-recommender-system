import pandas as pd
from test_data.fill_db import get_path
from typing import cast, Dict


def check_person(persons, duplicates, id, name):
    found_name = persons.get(id)
    if found_name:
        if found_name != name and not duplicates.get(id):
            duplicates[id] = name
    else:
        persons[id] = name


def print_duplicates(duplicates):
    if not duplicates:
        print("No duplicates found")
    else:
        for id, name in duplicates.items():
            print(f"id: {id}, name: {name}")


def find_duplicates():
    movies_df = pd.read_json(
        get_path("movies.json"), orient="records", convert_dates=["release_date"]
    )

    persons = {}
    duplicates = {}

    for row in movies_df.itertuples():
        if isinstance(row.cast, list):
            for cast_member in row.cast:
                if isinstance(cast_member, dict):
                    check_person(
                        persons, duplicates, cast_member["id"], cast_member["name"]
                    )

        if isinstance(row.crew, dict):
            check_person(
                persons,
                duplicates,
                cast(Dict, row.crew)["id"],
                cast(Dict, row.crew)["name"],
            )

    print_duplicates(duplicates)


if __name__ == "__main__":
    find_duplicates()
