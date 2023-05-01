import facebook
import requests
user_access_token = "EABQUuk5VBgUBAIioYL4OfOIbFLo4EaRUPTe0SrJZ" \
                    "CPhLVNtso1gzJ4nsr8FEUd02UnW04vicKgFLf2PBmUDZBj6V" \
                    "IcTCenKLMjhAkPGBizmv8gCyGhC3fW15cSavqYPEBdtwtWTUrZAm" \
                    "YZAYmh2qzG0ntdhzGxanfHbMadKp9XqYPRHrjRI6ZCQVhVesYnd9" \
                    "LNu10wip4ZAwZDZD"

graph = facebook.GraphAPI(access_token=user_access_token, version="2.12")
app_id = "5652289944880645"
canvas_url = "http://amaira0218.pythonanywhere.com/"
# perms = ["manage_pages","publish_pages"]
fb_page_api = graph.get_object("me/accounts")

# TODO 1: Get userid and user access token:
fb_page_list = {}
for page in fb_page_api['data']:
    fb_page_list[page['name']] = page['access_token']

print(fb_page_list)
# TODO 2: Get Page list for associated account:
userid = "110550945301774"

fb_page_access_token = "EABQUuk5VBgUBAJI5kMhK4mawCJIgReWOT" \
                       "iQRbw0RrkVlfghFKluyoIsL97XLJRViycuxWG" \
                       "XuLOZBM5oAaB8vPzQaWwpP2JVxqAsWHgH5F" \
                       "mPJGpJcSLqgnmZBjERZBQ1ccCVT1tKxZ" \
                       "AQ2mTcGKfTl5rq72XOZCrRH0JBNbI8r" \
                       "JItFF9IcBh2rx"
# Access Token Needs to Update every 60 days
fb_page = "110550945301774"
copyright_rule_id = "<If using FB Rights Manager>"