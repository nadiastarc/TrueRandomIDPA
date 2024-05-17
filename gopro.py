from goprocam import GoProCamera
import hashlib

go_pro = GoProCamera.GoPro()


def take_photo_and_generate_hash():
    # Take photo
    go_pro.take_photo(timer=5)

    # Download last taken photo
    go_pro.downloadLastMedia(custom_filename="Test.JPG")

    # Generate hash based on pixels
    hash_code = generate_hash_from_image("Test.JPG")
    print("Hash code:", hash_code)

    # Delete the last taken photo
    go_pro.delete("last")


def generate_hash_from_image(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        # Generate MD5 hash based on image data
        hash_md5 = hashlib.md5(image_data)
        return hash_md5.hexdigest()


take_photo_and_generate_hash()
