"""
用于导出和导入Python依赖包的脚本。

用法：
    python pip-in-local.py export-dependencies <output_directory> [--dry-run] [-v]
    python pip-in-local.py import-dependencies <input_directory> [--dry-run] [-v] [-s]

选项：
    -h, --help                显示此帮助文本。
    --dry-run                 输出将要执行的命令但不实际执行。
    -v, --verbose             启用详细日志记录。
    -s, --silent              不输出任何信息。

子命令：
    export-dependencies       将pip list得到的所有包导出到指定的目录。
    import-dependencies       安装指定目录的所有包。

示例：
    # 导出所有的Python依赖包到 /path/to/output 目录。
    python pip-in-local.py export-dependencies /path/to/output

    # 在 /path/to/input 目录中找到所有的Python依赖包并安装。
    python pip-in-local.py import-dependencies /path/to/input

    # 将所有的Python依赖包导出到 /path/to/output 目录，但只输出执行的命令。
    python pip-in-local.py export-dependencies /path/to/output --dry-run

    # 安装 /path/to/input 目录中的所有Python依赖包，但不输出任何信息。
    python pip-in-local.py import-dependencies /path/to/input -s
"""
import argparse
import os
import subprocess
import sys
import pip

def export_dependencies(output_directory, is_dry_run, is_silent, is_verbose):
    """
    导出所有依赖包到指定目录
    """
    command = ["pip", "list", "--format=freeze"] + (["-v"] if is_verbose else [])
    pip_list_output = subprocess.check_output(command)
    dependencies = pip_list_output.decode("utf-8").split("\n")
    dependencies = [dep.strip() for dep in dependencies if dep.strip()]

    for dependency in dependencies:
        filename = os.path.join(output_directory, dependency.split("=")[0] + ".txt")
        if not is_silent:
            print(f"Exporting {dependency} to {filename}")
        if not is_dry_run and not is_silent:
            print(f"  + {dependency}")
        if not is_dry_run:
            with open(filename, "w") as fp:
                fp.write(dependency)

def import_dependencies(input_directory, is_dry_run, is_silent, is_verbose):
    """
    安装指定目录中的所有依赖包
    """
    command = ["pip", "install", "--no-index", "--find-links=" + input_directory] + (["-v"] if is_verbose else [])
    if not is_verbose:
        command += ["-q"]

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            dependency = open(file_path).read().strip()
            if not is_silent:
                print(f"Installing {dependency}")
            if not is_dry_run and not is_silent:
                print(f"  + {dependency}")
            if not is_dry_run:
                try:
                    pip.main(command + [dependency])
                except SystemExit:
                    pass

def main():
    parser = argparse.ArgumentParser(description="Export or import Python dependencies.")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command")

    export_parser = subparsers.add_parser("export-dependencies")
    export_parser.add_argument("output_directory", help="Directory to export dependencies to")
    export_parser.add_argument("--dry-run", action="store_true", help="Output what will happen, but don't actually export")
    export_parser.add_argument("-v", "--verbose", action="store_true", help="List all actions")

    import_parser = subparsers.add_parser("import-dependencies")
    import_parser.add_argument("input_directory", help="Directory to import dependencies from")
    import_parser.add_argument("--dry-run", action="store_true", help="Output what will happen, but don't actually import")
    import_parser.add_argument("-v", "--verbose", action="store_true", help="List all actions")
    import_parser.add_argument("-s", "--silent", action="store_true", help="Don't output anything")

    args = parser.parse_args()

    if args.command == "export-dependencies":
        export_dependencies(args.output_directory, args.dry_run, args.silent or not args.verbose, args.verbose)
    elif args.command == "import-dependencies":
        import_dependencies(args.input_directory, args.dry_run, args.silent, args.verbose)
    else:
        parser.print_help()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
