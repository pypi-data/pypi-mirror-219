import re
import requests


class SearchAnime:

    def __init__(self, title):
        self.title = title
        self.animeSearch()

    def animeSearch(self):
        self.query = '''
        query ($search: String! $type: MediaType!) { 
            Media (search: $search type: $type) { 
                id
                title {
                    romaji
                    english
                }
                status
                description
                averageScore
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                coverImage {
                    large  
                }
                genres
                siteUrl
                episodes
                season
                format
            }
        }
        '''
        self.variables = {
            'search': self.title,
            'type': 'ANIME',
        }
        self.url = 'https://graphql.anilist.co'
        self.response = requests.post(
            self.url, json={'query': self.query, 'variables': self.variables})
        self.response = self.response.json()
        self.Media = self.response.get('data').get('Media')

    def getAnimeData(self):
        return self.response

    def getAnimeRomajiName(self):
        return self.Media.get('title').get('romaji')

    def getAnimeEnglishName(self):
        return self.Media.get('title').get('english')

    def getAnimeStatus(self):
        return self.Media.get('status')

    def getAnimeDescription(self):
        des = self.Media.get('description')
        return re.sub(re.compile('<.*?>'), '', des)

    def getAnimeEpisodes(self):
        return self.Media.get('episodes')

    def getAnimeCoverImage(self):
        return self.Media.get('coverImage').get('large')

    def getAnimeGenres(self):
        return ", ".join(self.Media.get('genres'))

    def getAnimeSiteUrl(self):
        return self.Media.get('siteUrl')

    def getAnimeStartDate(self):
        esd = self.Media.get('startDate')
        return str(esd.get('month')) + '/' + str(esd.get('day')) + '/' + str(esd.get('year'))

    def getAnimeEndDate(self):
        exp = self.Media.get('endDate')
        return str(exp.get('month')) + '/' + str(exp.get('day')) + '/' + str(exp.get('year'))

    def getAnimeAverageScore(self):
        return int(self.Media.get('averageScore'))/10

    def getAnimeSeason(self):
        return self.Media.get('season')

    def getAnimeFormat(self):
        return self.Media.get('format')

    def getAnimeID(self):
        return self.Media.get('id')
