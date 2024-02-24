from goprocam import GoProCamera, constants

go_pro = GoProCamera.GoPro()
# List all Media
# go_pro.listMedia(True)

def take_photo():
    go_pro.take_photo(timer=5)
    go_pro.downloadLastMedia(custom_filename="Test.JPG")
    go_pro.delete("last")

take_photo()
go_pro.listMedia(True)