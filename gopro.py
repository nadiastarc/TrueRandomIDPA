from flask import Flask, request, jsonify, send_from_directory
from goprocam import GoProCamera
import hashlib
import json
import os

app = Flask(__name__)
go_pro = GoProCamera.GoPro()


@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'lotto.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    numbers_to_pick = int(data.get('numbers_to_pick'))

    # Debug: Print received data
    print(f"Received numbers_to_pick: {numbers_to_pick}")

    # Take multiple photos and generate hash values
    hash_codes = take_multiple_photos_and_generate_hashes(numbers_to_pick)

    # Debug: Print hash codes
    print(f"Generated hash codes: {hash_codes}")

    # Return the hash codes as a JSON response
    return jsonify({'hash_codes': hash_codes})


def take_multiple_photos_and_generate_hashes(count):
    hash_codes = []

    for i in range(count):
        # Take photo
        go_pro.take_photo(timer=5)

        # Download last taken photo with a unique name
        filename = f"Test_{i}.JPG"
        go_pro.downloadLastMedia(custom_filename=filename)

        # Generate hash based on pixels
        hash_code = generate_hash_from_image(filename)
        print(f"Hash code for {filename}: {hash_code}")

        # Save the hash code to the list
        hash_codes.append(hash_code)

        # Delete the last taken photo
        go_pro.delete("last")

    # Save all hash codes in a single JSON file
    save_hashes_to_json(hash_codes)

    return hash_codes


def generate_hash_from_image(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        # Generate MD5 hash based on image data
        hash_md5 = hashlib.md5(image_data)
        return hash_md5.hexdigest()


def save_hashes_to_json(hash_codes):
    hash_data = {"hash_codes": hash_codes}
    with open("hash_codes.json", "w") as json_file:
        json.dump(hash_data, json_file)


if __name__ == '__main__':
    app.run(debug=True)
