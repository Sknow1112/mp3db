import wave
import struct
import os
import base64

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.entries = self.load_database()

    def load_database(self):
        try:
            with wave.open(self.filename, "rb") as wav_file:
                num_frames = wav_file.getnframes()
                frames = wav_file.readframes(num_frames)
                data = struct.unpack(f"<{num_frames}h", frames)
                entries = "".join(chr(freq // 100) for freq in data).split("\n")
                return entries
        except FileNotFoundError:
            return []

    def save_database(self):
        data = "\n".join(self.entries)
        frequencies = [ord(char) * 100 for char in data]
        frames = struct.pack(f"<{len(frequencies)}h", *frequencies)

        with wave.open(self.filename, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(44100)
            wav_file.writeframes(frames)

    def add_entry(self, entry):
        self.entries.append(entry)

    def add_file(self, file_path):
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(file_path)
                encoded_data = self.encode_file_data(file_data)
                entry = f"[{file_name}]{encoded_data}"
                self.entries.append(entry)
                print("File added successfully.")
        except FileNotFoundError:
            print("File not found.")

    def download_file(self, file_name):
        for entry in self.entries:
            if entry.startswith(f"[{file_name}]"):
                encoded_data = entry[len(file_name) + 2:]
                file_data = self.decode_file_data(encoded_data)
                with open(file_name, "wb") as file:
                    file.write(file_data)
                    print("File downloaded successfully.")
                return
        print("File not found in the database.")

    def encode_file_data(self, file_data):
        encoded_data = base64.b64encode(file_data).decode("utf-8")
        return encoded_data

    def decode_file_data(self, encoded_data):
        file_data = base64.b64decode(encoded_data)
        return file_data

    def search_entries(self, search_term):
        print("\nSearch Results:")
        found = False
        for i, entry in enumerate(self.entries, start=1):
            if search_term in entry:
                if entry.startswith("[") and entry.endswith("]"):
                    print(f"Line {i}: {entry[:entry.index(']') + 1]}")
                else:
                    print(f"Line {i}: {entry}")
                found = True
        if not found:
            print("No entries found.")

    def print_all_entries(self):
        print("\nAll Entries:")
        for entry in self.entries:
            if entry.startswith("[") and entry.endswith("]"):
                print(entry[:entry.index("]") + 1])
            else:
                print(entry)