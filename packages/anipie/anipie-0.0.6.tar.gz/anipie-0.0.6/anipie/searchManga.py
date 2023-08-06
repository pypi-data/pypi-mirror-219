import requests
import re


class SearchManga:

    def __init__(self, title):
        self.title = title
        self.response = None
        self.mangaSearch()

    def mangaSearch(self):
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
                chapters
                volumes
                format
            }
        }
        '''
        self.variables = {
            'search': self.title,
            'type': 'MANGA',
        }
        self.url = 'https://graphql.anilist.co'
        self.response = requests.post(
            self.url, json={'query': self.query, 'variables': self.variables})
        self.response = self.response.json()
        self.Media = self.response.get('data').get('Media')

    def getMangaData(self):
        return self.response

    def getMangaRomajiName(self):
        return self.Media.get('title').get('romaji')

    def getMangaEnglishName(self):
        return self.Media.get('title').get('english')

    def getMangaStatus(self):
        return self.Media.get('status')

    def getMangaDescription(self):
        des = self.Media.get('description')
        return re.sub(re.compile('<.*?>'), '', des)

    def getMangaStartDate(self):
        esd = self.Media.get('startDate')
        return str(esd.get('month')) + '/' + str(esd.get('day')) + '/' + str(esd.get('year'))

    def getMangaEndDate(self):
        exp = self.Media.get('endDate')
        return str(exp.get('month')) + '/' + str(exp.get('day')) + '/' + str(exp.get('year'))

    def getMangaCoverImage(self):
        return self.Media.get('coverImage').get('large')

    def getMangaGenres(self):
        return ", ".join(self.Media.get('genres'))

    def getMangaSiteUrl(self):
        return self.Media.get('siteUrl')

    def getMangaVolumes(self):
        return self.Media.get('volumes')

    def getMangaChapters(self):
        return self.Media.get('chapters')

    def getMangaAverageScore(self):
        return int(self.Media.get('averageScore')) / 10

    def getMangaFormat(self):
        return self.Media.get('format')

    def getMangaID(self):
        return self.Media.get('id')
