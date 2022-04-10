"""
Various classes written for the purpose of loading configuration from different platforms
"""
import json

class VideoHistoryLocal:
    """
    Simple class for historical posting data. Stores in JSON local storage.
    """
    def __init__(self):
        self.history = []

    def __getitem__(self, videoid: str):
        return videoid in self.history

    def __setitem__(self, videoid: str):
        """
        Altered from typical setitem definitions. Using only one variable instead of two.
        """
        # pylint: disable=unexpected-special-method-signature
        # I am using this outside of standards, by only taking a video ID and appending it instead
        # of setting a value.
        self.history.append(videoid)
        self.save()

    def __len__(self):
        return len(self.history)

    def read(self, filename: str = 'history.json'):
        """
        Read a JSON file that should be a simple array of strings, representing video IDs
        """
        with open(filename, 'r', encoding='utf-8') as historydata:
            self.history = json.load(historydata)

    def save(self, filename: str = 'history.json'):
        """
        Save a JSON file that should be a simple array of strings, representing video IDs
        """
        with open(filename, 'w', encoding='utf-8') as historydata:
            json.dump(self.history, historydata)
