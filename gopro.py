from flask import Flask, request, jsonify, send_from_directory, session
from goprocam import GoProCamera
import hashlib
import json
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session

go_pro = GoProCamera.GoPro()


@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'lotto.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    print(f"Received data: {data}")  # Debug print

    numbers_to_pick = data.get('numbers_to_pick')
    max_numbers = data.get('max_numbers')

    if numbers_to_pick is None or max_numbers is None:
        return jsonify({"error": "Missing 'numbers_to_pick' or 'max_numbers'"}), 400

    numbers_to_pick = int(numbers_to_pick)
    max_numbers = int(max_numbers)

    # Debug: Print received values
    print(f"Received numbers_to_pick: {numbers_to_pick}, max_numbers: {max_numbers}")

    # Check if this session has already processed the request
    if 'processed' in session:
        return jsonify({"error": "Already processed request"}), 400

    # Mark session as processed
    session['processed'] = True

    # Take multiple photos and generate unique decimal values and hash codes
    results = take_multiple_photos_and_generate_results(numbers_to_pick, max_numbers)

    # Extract decimal values and hash codes from results
    decimal_values = [result['decimal_value'] for result in results]
    hash_codes = [result['hash_code'] for result in results]

    # Debug: Print decimal values and hash codes
    print(f"Generated decimal values: {decimal_values}")
    print(f"Generated hash codes: {hash_codes}")

    # Return the decimal values and hash codes as a JSON response
    return jsonify({'decimal_values': decimal_values, 'hash_codes': hash_codes})


def take_multiple_photos_and_generate_results(count, max_value):
    results = []
    chosen_values = set()  # To store chosen decimal values

    while len(results) < count:
        # Take photo
        go_pro.take_photo(timer=1)

        # Download last taken photo with a unique name
        filename = f"Test_{len(results)}.JPG"
        go_pro.downloadLastMedia(custom_filename=filename)

        # Generate hash and convert to decimal
        decimal_value = generate_decimal_from_image(filename, max_value)

        # Check if decimal_value is unique and within range
        if decimal_value not in chosen_values and decimal_value <= max_value:
            # Add decimal_value to chosen_values
            chosen_values.add(decimal_value)

            # Calculate MD5 hash code
            hash_code = generate_hash_from_image(filename)

            # Save the decimal value and hash code to results
            results.append({'decimal_value': decimal_value, 'hash_code': hash_code})
            print(f"Decimal value for {filename}: {decimal_value}, MD5 hash code: {hash_code}")
        else:
            # If not unique, delete the last taken photo and retry
            go_pro.delete("last")

    # Save all decimal values and hash codes in a single JSON file (optional)
    save_results_to_json(results)

    # Clear session flag after processing
    session.pop('processed', None)

    return results


def generate_decimal_from_image(image_path, max_value):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        # Generate MD5 hash based on image data
        hash_md5 = hashlib.md5(image_data).hexdigest()
        # Convert hash to an integer
        hash_int = int(hash_md5, 16)
        # Scale the integer to the range 1 to max_value
        scaled_value = (hash_int % max_value) + 1
        return scaled_value


def generate_hash_from_image(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        # Generate MD5 hash based on image data
        hash_md5 = hashlib.md5(image_data)
        return hash_md5.hexdigest()


def save_results_to_json(results):
    data = {"results": results}
    with open("results.json", "w") as json_file:
        json.dump(data, json_file)


if __name__ == '__main__':
    app.run(debug=True)
