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
            page_token = page['access_token']
            page_graph = facebook.GraphAPI(access_token=page_token, version="2.12")
            insights = page_graph.get_object(f"{page['id']}/insights/page_impressions")
            listed_metrics = {}
            for metric in insights['data']:
                if f'{metric["name"]}_{metric["period"]}' == 'page_impressions_day':
                    metric_title = "Page Impressions Per Day"
                elif f'{metric["name"]}_{metric["period"]}' == 'page_impressions_week':
                    metric_title = "Page Impressions Per Week"
                elif f'{metric["name"]}_{metric["period"]}' == 'page_impressions_days_28':
                    metric_title = "Page Impressions Every 28 Days"
                else:
                    metric_title = "New Metric"
                listed_metrics[metric_title] = metric["values"][1]['value']
            fb_page_list.append({'Name': page['name'],
                                 'AccessToken': page['access_token'],
                                 'Insights': listed_metrics
                                 })
        return {"data": fb_page_list}

fb = Facebook("EABQUuk5VBgUBAAFKuSvaipDlsN4xZARuI69bPrLwZANa2Pye08XnZCZBHCdORvJAzPNcMApVESoU1UAmwWmy2Iom92kWaTuatUwxaqJMHXgkUrh7ArDPFLz09LoMiZBj26pJZCllSxnfJ1Xd6nZBlj7P75JislkK5bh8IlTWnXqbyV1402DGFOjlPJ6mBCxeZAB3NIrCmVXjGvulLUwyouWhrfLOJfcEosMZD")
print(fb.get_pages())