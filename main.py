from PIL import Image
from PIL.ExifTags import GPSTAGS
from termcolor import colored
import os

def getData(file_name: str) -> dict:
    path = file_name
    img = Image.open(path)
    data = {}

    if img.getexif():
        exif_data = img.getexif()

        model = exif_data.get(272, "Unknown Data")
        if model != "Unknown Data":
            data["Model"] = colored(model, color="green")
        else:
            data["Model"] = colored(model, color="red")

        datetime = exif_data.get(306, "Unknown Data")
        if model != "Unknown Data":
            data["Datetime"] = colored(datetime, color="green")
        else:
            data["Datetime"] = colored(datetime, color="red")

        gps_info = exif_data.get(34853)
        if gps_info:
            gps_data = {}
            for key, val in gps_info.items():
                name = GPSTAGS.get(key, key)
                gps_data[name] = val

            def convertToDegrees(value):
                d, m, s = value
                return d[0] / d[1] + (m[0] / m[1]) / 60 + (s[0] / s[1]) / 3600

            try:
                lat = convertToDegrees(gps_data["GPSLatitude"])
                lon = convertToDegrees(gps_data["GPSLongitude"])

                data["Latitude"] = colored(round(lat, 6), color="green")
                data["Longitude"] = colored(round(lon, 6), color="green")
                data["GoogleMaps"] = colored(f"https://www.google.com/maps?q={lat},{lon}", color="light_blue")
                
            except KeyError:
                data["Latitude"] = colored("Unknown Data", color="red")
                data["Longitude"] = colored("Unknown Data", color="red")
                data["GoogleMaps"] = colored("Unknown Data", color="red")
        else:
            data["Latitude"] = colored("Unknown Data", color="red")
            data["Longitude"] = colored("Unknown Data", color="red")
            data["GoogleMaps"] = colored("Unknown Data", color="red")
    else:
        data["Model"] = colored("No EXIF", color="red")
        data["Datetime"] = colored("No EXIF", color="red")
        data["Latitude"] = colored("No EXIF", color="red")
        data["Longitude"] = colored("No EXIF", color="red")
        data["GoogleMaps"] = colored("No EXIF", color="red")

    data["size_px"] = colored([str(i)+"px" for i in img.size], color="white")

    img_size = os.path.getsize(path)
    data["Size_KB"] = colored(str(round(img_size/ 1000 , 2)) + "KB", color="white")
    data["Size_MB"] = colored(str(round(img_size / (1000 * 1000), 2)) + "MB", color="white")

    return data

if __name__ == "__main__":
        file = "<---YOUR FILE PATH HERE--->"
        metadata = getData(file)
        print(colored(f"\n{file}", color="yellow"))
        for key, value in metadata.items():
            print(f"{key}: {value}")

#                   OR

# if __name__ == "__main__":
#     for file in os.listdir("<---YOUR FOLDER PATH HERE--->"):
#         metadata = getData(file)
#         print(colored(f"\n{file}", color="yellow"))
#         for key, value in metadata.items():

#             print(f"{key}: {value}")

