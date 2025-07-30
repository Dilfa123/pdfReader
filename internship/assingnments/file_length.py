import os
import math

def process_directory(path):
    try:
        all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        print("Files in directory:")
        for file in all_files:
            print(file)
        
        total_files = len(all_files)
        
        longest_file = max(all_files, key=len) if all_files else "No files found"
        
        square_root = round(math.sqrt(total_files), 2)
        
        rounded_value = math.ceil(total_files / 10) * 10
        
        print("\nLongest filename:", longest_file)
        print("Total files:", total_files)
        print("Square root of file count:", square_root)
        print("Rounded up to nearest multiple of 10:", rounded_value)

    except FileNotFoundError:
        print("Error: The path does not exist.")
    except Exception as e:
        print("An error occurred:", str(e))

directory_path = input("Enter the directory path: ")
process_directory(directory_path)