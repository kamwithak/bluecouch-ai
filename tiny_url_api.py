import requests
import urllib

"""
URL shortener class using TinyURL API
"""
class UrlShortenTinyurl:

    def __init__(self):
        self.API = "http://tinyurl.com/api-create.php"

    def shorten(self, url_long):
        try:
            url = self.API + "?" \
                + urllib.parse.urlencode({"url": url_long})
            return requests.get(url).text
        except Exception as e:
            raise