#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil
import sys
from typing import Dict
import zipfile

from downgrade_to_godot_3 import downgrade_file

def main():
	parser = argparse.ArgumentParser(prog='Build Release', description='Builds a release of a Godot project.')
	parser.add_argument('-p', '--project_base_folder', type=Path, default="../", help="Path to project base folder. Default: ../")
	parser.add_argument('-a', '--addons_folder', type=Path, default="../addons", help="Path to addons folder. Default: ../addons")
	parser.add_argument('-o', '--output_folder', type=Path, default="../output", help="Path to output folder. Default: ../output")
	parser.add_argument('-l', '--license_file', type=Path, default="../LICENSE", help="Path to license file. Default: ../LICENSE")
	parser.add_argument('-r', '--readme_file', type=Path, default="../README.md", help="Path to README file. Default: ../README.md")
	parser.add_argument('-d', '--downgrade', action=argparse.BooleanOptionalAction, default=False, help="Whether to output downgraded GDScript files or not. Default: False")

	args = parser.parse_args()

	# Resolve all argument file paths.
	project_base_folder_path = Path(args.project_base_folder).expanduser().resolve()
	addons_folder_path = Path(args.addons_folder).expanduser().resolve()
	output_folder_path = Path(args.output_folder).expanduser().resolve()

	license_file_path : Path | None = Path(args.license_file).expanduser().resolve()
	if not license_file_path.exists():
		license_file_path = None

	readme_file_path : Path | None = Path(args.readme_file).expanduser().resolve()
	if not readme_file_path.exists():
		readme_file_path = None

	# If we need to downgrade, iterate all files in addons and downgrade files with the '.gd' extension. Then, keep track of the input file path and the downgrade output file path.
	input_file_path_to_downgraded_file_path_dictionary : Dict[Path, Path] = {}
	if args.downgrade:
		downgrade_folder_path = Path(output_folder_path, "downgraded")

		for file_path in addons_folder_path.rglob('*'):
			if file_path.is_file():
				if file_path.suffix == '.gd':
					input_file_path_to_downgraded_file_path_dictionary[file_path] = Path(downgrade_file(file_path, downgrade_folder_path))

	# For every directory in the addon folder, use the last directory as the name for the output zip. Also, copy the license and readme files into each folder.
	output_project_name : str | None = None
	for file_path in addons_folder_path.iterdir():
		if file_path.is_dir():
			output_project_name = file_path.name

			if license_file_path != None:
				shutil.copy2(license_file_path, Path(file_path, license_file_path.name))

			if readme_file_path != None:
				shutil.copy2(readme_file_path, Path(file_path, readme_file_path.name))

	# Map the output zip file path to whether we need to downgrade or not.
	output_zip_file_path_to_use_downgrade_dictionary : Dict[Path, bool] = {}

	output_zip_file_path_to_use_downgrade_dictionary[Path(output_folder_path, output_project_name + "_godot_4.zip")] = False

	if args.downgrade:
		output_zip_file_path_to_use_downgrade_dictionary[Path(output_folder_path, output_project_name + "_godot_3.zip")] = True

	# For every zip file path, write every file in the addons folder to the zip file relative to the project base directory's parent. If we need to downgrade, attempt to write the associated downgraded file if it exists.
	for output_zip_file_path, use_downgrade in output_zip_file_path_to_use_downgrade_dictionary.items():
		with zipfile.ZipFile(output_zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
			for file_path in addons_folder_path.rglob('*'):
				source_file_path = file_path
				if use_downgrade:
					source_file_path = input_file_path_to_downgraded_file_path_dictionary.get(source_file_path, source_file_path)

				zip_file.write(source_file_path, file_path.relative_to(project_base_folder_path.parent))

	return 0

if __name__ == '__main__':
	sys.exit(main())