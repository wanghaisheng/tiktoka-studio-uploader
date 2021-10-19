from opplast import Upload


if __name__ == "__main__":
    upload = Upload(
        # use r"" for paths, this will not give formatting errors e.g. "\n"
        r"C:/Users/USERNAME/AppData/Roaming/Mozilla/Firefox/Profiles/r4Nd0m.selenium",
    )

    was_uploaded, video_id = upload.upload(
        r"C:/path/to/video.mp4",
        title="My YouTube Title",
        description="My YouTube Description",
        thumbnail=r"C:/path/to/thumbnail.jpg",
        tags=["these", "are", "my", "tags"],
    )

    if was_uploaded:
        print(f"{video_id} has been uploaded to YouTube")

    upload.close()
