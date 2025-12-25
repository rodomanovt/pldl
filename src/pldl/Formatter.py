class Formatter:

    @staticmethod
    def remove_special_chars(filename: str) -> str:
        return filename.replace('.', '').replace('"', '').replace('/', '').replace('|', '')
    
    
    @staticmethod
    def smart_song_name(song_name: str) -> str:
        # TODO: implement
        pass