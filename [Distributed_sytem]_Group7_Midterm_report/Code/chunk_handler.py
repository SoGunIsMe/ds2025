import os

# Function to split a file into chunks
def split_file(file_path, chunk_size=1024):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, "rb") as f:
        chunks = []
        index = 0
        while chunk := f.read(chunk_size):
            chunk_file = f"{file_path}.chunk{index}"
            with open(chunk_file, "wb") as chunk_f:
                chunk_f.write(chunk)
            chunks.append(chunk_file)
            index += 1
    return chunks

# Function to merge chunks into the original file
def merge_chunks(chunks, output_file):
    with open(output_file, "wb") as f:
        for chunk in chunks:
            if not os.path.exists(chunk):
                raise FileNotFoundError(f"The chunk {chunk} does not exist.")
            with open(chunk, "rb") as chunk_f:
                f.write(chunk_f.read())
