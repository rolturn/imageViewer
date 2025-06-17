from fastapi import APIRouter, HTTPException, Form, Depends
import os
import shutil
from pathlib import Path
import json
from api.auth import get_current_user


router = APIRouter()
TRASH_DIR = "trash"
PICKS_DIR = "picks"

def ensure_directory_exists(directory: str) -> None:
    """
    Ensure that the given directory exists. If it doesn't, create it.
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        directory_path.mkdir(parents=True)

def move_file(src: Path, dest_dir: Path, filename: str) -> Path:
    """
    Move a file from src to destination directory.

    Args:
        src (Path): Source path of the file
        dest_dir (Path): Destination directory path
        filename (str): Filename to be moved

    Returns:
        Path: The new path of the moved file
    """
    source_file = src / filename
    if not source_file.exists():
        raise HTTPException(status_code=404, detail=f"{filename} does not exist in {src}")

    destination_file = dest_dir / filename
    shutil.move(str(source_file), str(destination_file))
    return destination_file

def update_json_metadata(src: Path, dest: Path, filename: str, updates: dict) -> None:
    """
    Update the JSON metadata file and move it to a new location.

    Args:
        src (Path): Source directory path
        dest (Path): Destination directory path
        filename (str): Filename of the image (used for metadata)
        updates (dict): Dictionary with key-value pairs to update in the JSON
    """
    metadata_filename = Path(filename).stem + ".json"
    source_metadata_file = src / metadata_filename

    if not source_metadata_file.exists():
        raise HTTPException(status_code=404, detail=f"JSON metadata for {filename} not found")

    data = json.loads(source_metadata_file.read_text())
    data.update(updates)
    destination_metadata_file = dest / metadata_filename

    with open(destination_metadata_file, "w") as f:
        json.dump(data, f)

    source_metadata_file.unlink()

@router.post("/to-trash")
async def move_to_trash(
    current_user: dict = Depends(get_current_user),
    image_name: str = Form(...)
):
    """
    Move an image and its JSON metadata to the trash directory. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Args:
        image_name (str): The name of the image file

    Returns:
        dict: A success message
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR", "images"))
        ensure_directory_exists(base_dir)
        trash_dir = base_dir / TRASH_DIR
        ensure_directory_exists(trash_dir)

        # Move image to the trash directory
        move_file(base_dir, trash_dir, image_name)

        # Update JSON metadata for trashed image
        update_json_metadata(
            src=base_dir,
            dest=trash_dir,
            filename=image_name,
            updates={"trash": True}
        )

        return {"message": "Image and its JSON moved to trash"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/to-picks")
async def move_to_picks(
    current_user: dict = Depends(get_current_user),
    image_name: str = Form(...)
):
    """
    Move an image and its JSON metadata to the picks directory. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Args:
        image_name (str): The name of the image file

    Returns:
        dict: A success message
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR", "images"))
        ensure_directory_exists(base_dir)
        picks_dir = base_dir / PICKS_DIR
        ensure_directory_exists(picks_dir)

        # Move image to the picks directory
        move_file(base_dir, picks_dir, image_name)

        # Update JSON metadata for picked image
        update_json_metadata(
            src=base_dir,
            dest=picks_dir,
            filename=image_name,
            updates={"rating": 5, "pick": True}
        )

        return {"message": "Image and its JSON moved to picks"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete-all-trash")
async def delete_all_trash(current_user: dict = Depends(get_current_user)):
    """
    Delete all images from the trash directory. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Returns:
        dict: A success message
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR", "images"))
        ensure_directory_exists(base_dir)
        trash_dir = base_dir / TRASH_DIR

        if not trash_dir.exists() or not trash_dir.is_dir():
            raise HTTPException(status_code=404, detail="Trash directory does not exist")

        for item in trash_dir.iterdir():
            item.unlink()

        return {"message": "All images deleted from trash"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restore-from-trash")
async def restore_from_trash(
    current_user: dict = Depends(get_current_user),
    image_name: str = Form(...)
):
    """
    Restore an image and its JSON metadata from the trash directory. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Args:
        image_name (str): The name of the image file

    Returns:
        dict: A success message
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR", "images"))
        ensure_directory_exists(base_dir)
        trash_dir = base_dir / TRASH_DIR

        if not trash_dir.exists() or not trash_dir.is_dir():
            raise HTTPException(status_code=404, detail="Trash directory does not exist")

        # Move image from trash back to the base directory
        move_file(trash_dir, base_dir, image_name)

        # Update JSON metadata for restored image
        update_json_metadata(
            src=trash_dir,
            dest=base_dir,
            filename=image_name,
            updates={"trash": False}
        )

        return {"message": "Image and its JSON restored from trash"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demote-pick")
async def demote_pick(
    current_user: dict = Depends(get_current_user),
    image_name: str = Form(...)
):
    """
    Demote an image's pick status and move it back to the base directory. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Args:
        image_name (str): The name of the image file

    Returns:
        dict: A success message
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR", "images"))
        ensure_directory_exists(base_dir)
        picks_dir = base_dir / PICKS_DIR

        if not picks_dir.exists() or not picks_dir.is_dir():
            raise HTTPException(status_code=404, detail="Picks directory does not exist")

        # Update JSON metadata for demoted pick
        update_json_metadata(
            src=picks_dir,
            dest=base_dir,
            filename=image_name,
            updates={"pick": False, "rating": 4}
        )

        # Move image from picks back to the base directory
        move_file(picks_dir, base_dir, image_name)

        return {"message": "Pick status updated and image moved"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))