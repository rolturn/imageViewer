from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
import os
from typing import List, Dict, Any
from pathlib import Path
import json
from api.auth import get_current_user


load_dotenv()  # Load .env file
router = APIRouter()


def ensure_json_exists(file: Path):
    """
    Ensure each image has its own .json metadata file.

    Args:
        file (Path): The path to the image file.
    """
    if not file.with_suffix('.json').exists():
        default_metadata = {
            "filename": file.name,
            "trash": False,
            "pick": False,
            "rating": None,
            "notes": "",
            "prompt": ""
        }
        with open(file.with_suffix('.json'), 'w') as json_file:
            json.dump(default_metadata, json_file)


def update_json_if_needed(file: Path):
    """
    Update the JSON metadata if necessary.

    Args:
        file (Path): The path to the image file.
    """
    json_path = file.with_suffix('.json')
    # Load existing JSON data
    with open(json_path, 'r') as json_file:
        metadata = json.load(json_file)

    # Ensure all fields are present and have default values if missing
    for key in ["trash", "pick", "rating", "notes", "prompt"]:
        if key not in metadata or metadata[key] is None:
            metadata[key] = ""

    # Write back the updated JSON data
    with open(json_path, 'w') as json_file:
        json.dump(metadata, json_file)


def collect_json_files(directory: Path) -> List[Path]:
    """
    Collect all .json metadata files from a directory.

    Args:
        directory (Path): The path to the directory containing JSON metadata files.

    Returns:
        List[Path]: A list of paths to JSON metadata files.
    """
    json_files = []
    if directory.exists() and directory.is_dir():
        for file in directory.iterdir():
            # Only collect .json metadata files
            if file.is_file() and file.suffix == '.json':
                json_files.append(file)
    return json_files


def process_json_metadata(json_files: List[Path], filter_func=None) -> List[Dict[str, Any]]:
    """
    Process the collected JSON metadata to create response objects.

    Args:
        json_files (List[Path]): A list of paths to JSON metadata files.
        filter_func (function, optional): A function to filter JSON metadata. Defaults to None.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing image metadata.
    """
    image_objects = []
    for json_file in json_files:
        with open(json_file, 'r') as f:
            metadata = json.load(f)
            if filter_func is not None and not filter_func(metadata):
                continue
            image_objects.append(metadata)
    return image_objects


def check_directories():
    """
    Ensure all images have their .json metadata files.
    """
    base_dir = Path(os.getenv("BASE_DIR"))
    if not base_dir.exists() or not base_dir.is_dir():
        return

    for directory in [base_dir, base_dir / "picks", base_dir / "trash"]:
        if directory.exists() and directory.is_dir():
            for file in directory.iterdir():
                if file.is_file() and not file.name.startswith('.') and file.suffix != '.json':
                    ensure_json_exists(file)


@router.get("/", response_model=List[Dict[str, Any]])
def get_images(current_user: dict = Depends(get_current_user)):
    """
    Retrieve a list of all image metadata. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing image metadata.
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR"))
        if not base_dir.exists() or not base_dir.is_dir():
            raise HTTPException(status_code=404, detail="Base directory does not exist")

        # Initialize list to collect JSON metadata files
        json_files = []

        print("Checking and updating JSON metadata...")

        # Check and update each image's JSON file
        for directory in [base_dir, base_dir / "picks", base_dir / "trash"]:
            if not directory.exists() or not directory.is_dir():
                continue

            for file in directory.iterdir():
                # Only process image files (not .json metadata files)
                if file.is_file() and not file.name.startswith('.') and file.suffix != '.json':
                    ensure_json_exists(file)  # Create JSON file if it doesn't exist
                    update_json_if_needed(file)  # Update JSON file with missing fields

        # Collect all the JSON metadata files from various directories
        for directory in [base_dir, base_dir / "picks", base_dir / "trash"]:
            json_files.extend(collect_json_files(directory))

        return process_json_metadata(json_files)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/trash", response_model=List[Dict[str, Any]])
def get_trash_images(current_user: dict = Depends(get_current_user)):
    """
    Retrieve a list of trash image metadata. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing trash image metadata.

    Raises:
        HTTPException: If the base directory does not exist or if there's an error processing files.
    """

    try:
        base_dir = Path(os.getenv("BASE_DIR"))
        if not base_dir.exists() or not base_dir.is_dir():
            raise HTTPException(status_code=404, detail="Base directory does not exist")

        json_files = collect_json_files(base_dir / "trash")
        return process_json_metadata(json_files, lambda metadata: "trash" in metadata and metadata["trash"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/picks", response_model=List[Dict[str, Any]])
def get_pick_images(current_user: dict = Depends(get_current_user)):
    """
    Retrieve a list of pick image metadata. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing pick image metadata.
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR"))
        if not base_dir.exists() or not base_dir.is_dir():
            raise HTTPException(status_code=404, detail="Base directory does not exist")

        json_files = collect_json_files(base_dir / "picks")
        return process_json_metadata(json_files, lambda metadata: "pick" in metadata and metadata["pick"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

