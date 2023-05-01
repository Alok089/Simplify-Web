import facebook

class Facebook:
    def __init__(self, user_access_token):
        self.token = user_access_token
    # user_access_token = "EABQUuk5VBgUBAIioYL4OfOIbFLo4EaRUPTe0SrJZ" \
    #                     "CPhLVNtso1gzJ4nsr8FEUd02UnW04vicKgFLf2PBmUDZBj6V" \
    #                     "IcTCenKLMjhAkPGBizmv8gCyGhC3fW15cSavqYPEBdtwtWTUrZAm" \
    #                     "YZAYmh2qzG0ntdhzGxanfHbMadKp9XqYPRHrjRI6ZCQVhVesYnd9" \
    #                     "LNu10wip4ZAwZDZD"
    def get_pages(self, token):
        graph = facebook.GraphAPI(access_token=token, version="2.12")
        fb_page_api = graph.get_object("me/accounts")
        # TODO 1: Get userid and user access token:
        fb_page_list = []
        for page in fb_page_api['data']:
            fb_page_list.append({'Name': page['name'],'AccessToken': page['access_token']})
        return {"data": fb_page_list}