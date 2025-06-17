from fastapi import APIRouter, HTTPException, Body, Depends
from dotenv import load_dotenv
import os
from typing import Optional
from pathlib import Path
import json
from api.auth import get_current_user


load_dotenv()  # Load .env file
router = APIRouter()


def get_target_directory(base_dir: Path, directory: Optional[str]) -> Path:
    """
    Determine the target directory based on the specified type.

    Args:
        base_dir (Path): The base directory.
        directory (Optional[str]): Can be 'trash', 'picks', or None for regular.

    Returns:
        Path: The path to the target directory.
    """
    if directory == 'trash':
        return base_dir / "trash"
    elif directory == 'picks':
        return base_dir / "picks"
    else:
        return base_dir

def load_metadata(json_file_path: Path) -> dict:
    """
    Load metadata from a JSON file.

    Args:
        json_file_path (Path): The path to the JSON file.

    Returns:
        dict: The loaded metadata.
    """
    with open(json_file_path, 'r') as f:
        return json.load(f)

def save_metadata(json_file_path: Path, metadata: dict):
    """
    Save metadata to a JSON file.

    Args:
        json_file_path (Path): The path to the JSON file.
        metadata (dict): The metadata to be saved.
    """
    with open(json_file_path, 'w') as f:
        json.dump(metadata, f)

@router.put("/update-metadata", response_model=dict)
def update_metadata(
    current_user: dict = Depends(get_current_user),
    filename: str = Body(...),
    directory: Optional[str] = Body(None),  # Can be 'trash', 'picks', or None for regular
    notes: Optional[str] = Body(None),
    prompt: Optional[str] = Body(None),
):
    """
    Update metadata for a specified file. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    Args:
        filename (str): The name of the file.
        directory (Optional[str]): Can be 'trash', 'picks', or None for regular.
        notes (Optional[str]): Notes to add/change in metadata.
        prompt (Optional[str]): Prompt to add/change in metadata.

    Returns:
        dict: A message indicating success or failure.

    Raises:
        HTTPException: If the base directory does not exist, if the file is not found,
                       or if there's an error processing files.
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR"))
        if not base_dir.exists() or not base_dir.is_dir():
            raise HTTPException(status_code=404, detail="Base directory does not exist")

        # Determine the target directory
        target_dir = get_target_directory(base_dir, directory)

        # Remove the file extension from filename before adding .json
        json_filename = Path(filename).stem + ".json"
        json_file_path = target_dir / json_filename

        # Check if the JSON file exists
        if not json_file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Load existing metadata
        metadata = load_metadata(json_file_path)

        # Update fields if provided
        if notes is not None:
            metadata['notes'] = notes
        if prompt is not None:
            metadata['prompt'] = prompt

        # Write updated metadata back to file
        save_metadata(json_file_path, metadata)

        return {"message": "Metadata updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))