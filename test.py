from config import SERVICES_ENABLED

for service in SERVICES_ENABLED:
    track = service.get_track_from_message("Hello, this is link: https://deezer.page.link/ry6x3Tf64HEhHnbT8")

    print(track.name)