import facebook

class Facebook:
    def __init__(self, user_access_token):
        self.token = user_access_token
    # user_access_token = "EABQUuk5VBgUBAIioYL4OfOIbFLo4EaRUPTe0SrJZ" \
    #                     "CPhLVNtso1gzJ4nsr8FEUd02UnW04vicKgFLf2PBmUDZBj6V" \
    #                     "IcTCenKLMjhAkPGBizmv8gCyGhC3fW15cSavqYPEBdtwtWTUrZAm" \
    #                     "YZAYmh2qzG0ntdhzGxanfHbMadKp9XqYPRHrjRI6ZCQVhVesYnd9" \
    #                     "LNu10wip4ZAwZDZD"
    def get_pages(self):
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        fb_page_api = graph.get_object("me/accounts")
        # TODO 1: Get userid and user access token:
        fb_page_list = []
        for page in fb_page_api['data']:
            insights = graph.get_object(f"{page['access_token']}/insights/page_impressions_unique")
            fb_page_list.append({'Name': page['name'],
                                 'AccessToken': page['access_token'],
                                 'Insights': insights})
        return {"data": fb_page_list}

test = Facebook("EABQUuk5VBgUBAK00JRQjkl9rkmTs09TjmzYrd9N1PIfeDs3dB4gLIZBQnKCs93OWpMKV042vooFTYAWsqUrko7cMc049uiggDCQBowlAf0JYaBpaqeMN7ulznAENQj4HoNMTaITZCQKRdLgoL5ylEizPszTC2j90OSeFPzx36eKa0FGIdAUWFMqFdbyMCFZB7ZAxAeZA1M8KmS3xLQcoZC97vZCnrrEFM4ZD")
page_list = test.get_pages()
