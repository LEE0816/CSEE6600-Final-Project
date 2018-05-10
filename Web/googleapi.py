from google_images_download import google_images_download
import shutil, os

# download images
response = google_images_download.googleimagesdownload()
arguments = {"keywords": "apple", "limit":20, "print_urls":True}
response.download(arguments)
# delete original folder
shutil.rmtree("static/img/downloads")
# move folder
shutil.move("downloads", "static/img/downloads")
L = []
for root, dirs, files in os.walk("static/img/downloads"):
    for file in files:
       L.append(os.path.join(root, file))


