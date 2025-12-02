import os

SRC_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ROOT_DIR = os.path.dirname(
    SRC_DIR
)


def upsert_dir(relative_path: str):
    path = os.path.join(ROOT_DIR, relative_path)

    if not os.path.exists(path):
        os.makedirs(path)
