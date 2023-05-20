import os
import subprocess
import shlex
import multiprocessing

# Function to process a file
def process_file(file_path):
    command = shlex.split(f'mediainfo --Output="Audio;%CodecID%" "{file_path}"')
    process = subprocess.run(command, capture_output=True, text=True)
    audio_codec = process.stdout.strip().lower()
    if "eac3" in audio_codec or "dts" in audio_codec:
        return file_path, audio_codec
    else:
        return None

# Ask user for folder path
folder = input("Enter the folder path: ")

# Validate folder path
while not os.path.isdir(folder):
    print("Invalid folder path. Please try again.")
    folder = input("Enter the folder path: ")

# List files in the folder
file_list = []
for root, dirs, files in os.walk(folder):
    for file in files:
        file_path = os.path.join(root, file)
        file_list.append(file_path)

# Number of parallel processes
num_processes = multiprocessing.cpu_count()

# Process files in parallel
with multiprocessing.Pool(processes=num_processes) as pool:
    results = pool.map(process_file, file_list)

# Filter and print the results
hits = 0
output_file = "output.txt"

with open(output_file, "w") as f:
    for result in results:
        if result is not None:
            file_path, audio_codec = result
            output_line = f"{file_path} [{audio_codec}]"
            f.write(f"{output_line}\n")
            hits += 1
            print(output_line)

print(f"Total hits: {hits}")
print(f"Output saved to {output_file}")

