from pathlib import Path


def validate_path(file_path: Path) -> None:
	if not isinstance(file_path, Path):
		file_path = Path(file_path)

	if not file_path.is_file():
		raise FileNotFoundError(f"unable to locate file: {file_path}")
	
	elif file_path.is_dir():
		raise OSError("path must be a file not a directory")