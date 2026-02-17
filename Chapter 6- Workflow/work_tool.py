import os 

def write_to_file(final_text, base_name="final_output"):
    # Base filename
     
    ext = ".md"
    file_name = f"{base_name}{ext}"
    counter = 1

    # Increment filename if it already exists
    while os.path.exists(file_name):
        counter += 1
        file_name = f"{base_name}{counter:02d}{ext}"  # e.g., final_output02.md

    # Write to the file
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"Output saved to {file_name}")