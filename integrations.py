import facebook
import requests
user_access_token = "EABQUuk5VBgUBALCon6ifROLirpaZCE60iBMJgOm2wj3Vup5vIcDXS" \
                    "uUVQoYFBctQ4Cpt7MGXWFRg40QKQo6ZCpbQj7jgUagABTqhVhKq4is9p" \
                    "fohjxmOckkM8FbAGlnwX9QKFmnMZBZCZBnE3X7mljMM7cVuRECqnbxZC" \
                    "vToU5AGzOoOBdB6KBZBVx5kYxrby4meZBYIjZCu3DAZDZD"

graph = facebook.GraphAPI(access_token="your_token", version="2.12")
app_id = "5652289944880645"
canvas_url = "http://amaira0218.pythonanywhere.com/"
# perms = ["manage_pages","publish_pages"]
fb_login_url = graph.get_auth_url(app_id, canvas_url)
response = requests.post(fb_login_url)
# TODO 1: Get userid and user access token:

# TODO 2: Get Page list for associated account:
userid = "110550945301774"
user_access_token = "EABQUuk5VBgUBALCon6ifROLirpaZCE60iBMJgOm2wj3Vup5vIcDXS" \
                    "uUVQoYFBctQ4Cpt7MGXWFRg40QKQo6ZCpbQj7jgUagABTqhVhKq4is9p" \
                    "fohjxmOckkM8FbAGlnwX9QKFmnMZBZCZBnE3X7mljMM7cVuRECqnbxZC" \
                    "vToU5AGzOoOBdB6KBZBVx5kYxrby4meZBYIjZCu3DAZDZD"

fb_page_access_token = "EABQUuk5VBgUBAJI5kMhK4mawCJIgReWOT" \
                       "iQRbw0RrkVlfghFKluyoIsL97XLJRViycuxWG" \
                       "XuLOZBM5oAaB8vPzQaWwpP2JVxqAsWHgH5F" \
                       "mPJGpJcSLqgnmZBjERZBQ1ccCVT1tKxZ" \
                       "AQ2mTcGKfTl5rq72XOZCrRH0JBNbI8r" \
                       "JItFF9IcBh2rx"
# Access Token Needs to Update every 60 days
fb_page = "110550945301774"
copyright_rule_id = "<If using FB Rights Manager>"