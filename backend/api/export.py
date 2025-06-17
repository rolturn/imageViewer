import os
from pathlib import Path
import json
import shutil
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from api.auth import get_current_user

router = APIRouter()

def ensure_directory_exists(directory: Path):
    """
    Ensure a directory exists. If it does exist, delete and recreate it.

    Args:
        directory (Path): The path to the directory.
    """
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()


def process_directory_for_prompts(directory: Path) -> list:
    """
    Process a given directory for JSON files with valid prompts.

    Args:
        directory (Path): The path to the directory containing JSON files.

    Returns:
        list: A list of tuples containing (json_file, source_dir, prompt_value).
    """
    json_files = []
    try:
        for json_file in directory.glob("*.json"):
            with open(json_file, 'r') as f:
                metadata = json.load(f)
                prompt_value = metadata.get('prompt', '')
                if prompt_value:  # Only add files with non-empty prompts
                    json_files.append((json_file, directory, prompt_value))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing JSON file {directory}: {str(e)}")
    return json_files


def create_export_archive(source_dir: Path, zip_filename: str) -> Path:
    """
    Create a ZIP archive of the given directory.

    Args:
        source_dir (Path): The path to the directory to be archived.
        zip_filename (str): The name of the ZIP file.

    Returns:
        Path: The path to the created ZIP file.
    """
    base_dir = source_dir.parent
    zip_path = base_dir / f"{zip_filename}.zip"
    shutil.make_archive(str(zip_path.with_suffix('')), 'zip', source_dir)
    return zip_path


@router.get("/prompts", response_class=FileResponse)
def export_prompts(current_user: dict = Depends(get_current_user)):
    """
    Export JSON files with valid prompts to a ZIP archive. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    This endpoint will:
    - Create a directory named "exported_prompts" in the base directory.
    - Process both base and picks directories for JSON files with non-empty prompts.
    - Copy images related to these JSON files into the "exported_prompts" directory.
    - Create .txt files containing the prompt values next to their respective images.
    - ZIP the entire contents of the "exported_prompts" directory.

    Returns:
        FileResponse: A ZIP file containing the exported prompts and corresponding images.
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR"))
        if not base_dir.exists() or not base_dir.is_dir():
            raise HTTPException(status_code=404, detail="Base directory does not exist")

        # Directory to store exported prompts
        export_dir = base_dir / "exported_prompts"
        ensure_directory_exists(export_dir)

        # Process both base and picks directories for JSON files with non-empty prompts
        json_files_from_base = process_directory_for_prompts(base_dir)
        picks_dir = base_dir / "picks"
        json_files_from_picks = []

        if picks_dir.exists() and picks_dir.is_dir():
            json_files_from_picks = process_directory_for_prompts(picks_dir)

        # Combine JSON files from both directories
        all_json_files = json_files_from_base + json_files_from_picks

        if not all_json_files:
            raise HTTPException(status_code=500, detail="No JSON files found with valid prompts")

        # Copy images and create corresponding .txt files with prompt values
        for json_file, source_dir, prompt_value in all_json_files:
            img_file = source_dir / (json_file.stem + '.png')
            if not img_file.exists():
                continue

            shutil.copy2(img_file, export_dir / img_file.name)  # Copy image to exported_prompts
            txt_filename = export_dir / (json_file.stem + ".txt")
            with open(txt_filename, 'w') as f:
                f.write(prompt_value)

        zip_path = create_export_archive(export_dir, "exported_prompts")

        return FileResponse(
            path=zip_path,
            filename="exported_prompts.zip",
            media_type='application/zip'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/picks", response_class=FileResponse)
def export_picks(current_user: dict = Depends(get_current_user)):
    """
    Export the "picks" directory to a ZIP archive. Requires user authentication.

    This endpoint is protected and requires the caller to be authenticated before access is granted.
    The current user information is retrieved using dependency injection with `get_current_user`.

    This endpoint will create a ZIP file containing all contents of the "picks" directory.

    Returns:
        FileResponse: A ZIP file containing the exported picks.
    """
    try:
        base_dir = Path(os.getenv("BASE_DIR"))
        picks_dir = base_dir / "picks"

        if not picks_dir.exists() or not picks_dir.is_dir():
            raise HTTPException(status_code=404, detail="Picks directory does not exist")

        zip_path = create_export_archive(picks_dir, "exported_picks")

        return FileResponse(
            path=zip_path,
            filename="exported_picks.zip",
            media_type='application/zip'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))