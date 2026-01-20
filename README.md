# Godot Plugin Tools
A collection of tools to make managing Godot plugin repositories easier.

## Features
- Creating zip releases.
- Downgrading Godot 4 scripts to Godot 3.

## Installation
### Method One: Git Submodule (Recommended)
- Add the GodotPluginTools git repository as a Git submodule via this command: `git submodule add https://github.com/Mycodeko/GodotPluginTools.git`

### Method Two: Manual Download
- Download the repository via `Code - Download ZIP` and extract the `GodotPluginTools-main` folder into your addon project.

## Usage
### `build_release.py`
```
usage: Build Release [-h] [-p PROJECT_BASE_FOLDER] [-a ADDONS_FOLDER] [-o OUTPUT_FOLDER] [-l LICENSE_FILE]
                     [-r README_FILE] [-d | --downgrade | --no-downgrade]

Builds a release of a Godot project.

options:
  -h, --help            show this help message and exit
  -p, --project_base_folder PROJECT_BASE_FOLDER
                        Path to project base folder. Default: ../
  -a, --addons_folder ADDONS_FOLDER
                        Path to addons folder. Default: ../addons
  -o, --output_folder OUTPUT_FOLDER
                        Path to output folder. Default: ../output
  -l, --license_file LICENSE_FILE
                        Path to license file. Default: ../LICENSE
  -r, --readme_file README_FILE
                        Path to README file. Default: ../README.md
  -d, --downgrade, --no-downgrade
                        Whether to output downgraded GDScript files or not. Default: False
```

## License
`GodotPluginTools` is licensed under the [Zero Clause BSD license](https://landley.net/toybox/license.html), meaning you may use it however you like with/without attribution **as long as you agree to waive any liability of the original authors for any damage the software may cause**.