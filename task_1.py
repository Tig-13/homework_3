import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys

def copy_file_to_target(file_path, target_dir):
    target_folder = target_dir / file_path.suffix[1:]
    target_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(file_path, target_folder / file_path.name)

def process_directory(source_dir, target_dir):
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                futures.append(executor.submit(copy_file_to_target, file_path, target_dir))
        
        for future in as_completed(futures):
            future.result()

def main():
    if len(sys.argv) < 2:
        print("Використання: python script.py <source_dir> [<target_dir>]")
        return

    source_dir = Path(sys.argv[1]).resolve()
    target_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("dist").resolve()

    if not source_dir.is_dir():
        print(f"Джерельна директорія {source_dir} не існує або не є директорією.")
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    process_directory(source_dir, target_dir)
    print(f"Файли успішно скопійовані в {target_dir}")

if __name__ == "__main__":
    main()
