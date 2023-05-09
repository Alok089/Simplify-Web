import facebook
import requests
import time
import datetime
from datetime import timedelta

class Facebook:
    def __init__(self, user_access_token):
        self.token = user_access_token
        self.all_posts = []
    def get_pages(self):
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        fb_page_api = graph.get_object("me/accounts")

        # TODO 1: Get userid and user access token:
        fb_page_list = []
        for page in fb_page_api['data']:
            if 'access_token' in page:
                page_graph = facebook.GraphAPI(access_token=page['access_token'], version="2.12")
                page_insights = page_graph.get_object(f"{page['id']}/insights?metric=page_impressions")
                listed_metrics = {}
                for metric in page_insights['data']:
                    if f'{metric["name"]}_{metric["period"]}' == 'page_impressions_day':
                        metric_title = "Page Impressions Yesterday"
                    elif f'{metric["name"]}_{metric["period"]}' == 'page_impressions_week':
                        metric_title = "Page Impressions Last Week"
                    elif f'{metric["name"]}_{metric["period"]}' == 'page_impressions_days_28':
                        metric_title = "Page Impressions Last 28 Days"
                    else:
                        metric_title = "New Metric"
                    listed_metrics[metric_title] = metric["values"][1]['value']
                fb_page_list.append({'Name': page['name'],
                                     'id': page['id'],
                                     'AccessToken': page['access_token'],
                                     'Insights': listed_metrics
                                     })
        return {"data": fb_page_list}
    def get_posts(self, page_name, lookback):
        # TODO 1: Get page Credentials from provided page name
        # page_name = "Action Reeplayy"
        fb = Facebook(self.token)
        page_details = fb.get_pages()
        for page in page_details['data']:
            if page['Name'] == page_name:
                access_token = page['AccessToken']
                page_id = page['id']
        graph = facebook.GraphAPI(access_token=access_token, version="2.12")
        fb_post_api = graph.get_object(f"/{page_id}/published_posts")

        # TODO 2: Define logic to get post metrics:
        def get_post_info(next_page_posts):
            def video_view_review(period):
                for provided_period in post_video_views['data']:
                    if period in provided_period['period']:
                        video_views = provided_period['values'][0]['value']
                return video_views

            # print(post_video_views['data'])
            def reaction_review(reaction):
                if reaction in post_reactions['data'][0]['values'][0]['value']:
                    reaction_value = post_reactions['data'][0]['values'][0]['value'][f'{reaction}']
                else:
                    reaction_value = 0
                return reaction_value

            for post in next_page_posts['data']:
                post_impressions = graph.get_object(f"/{post['id']}/insights/post_impressions")
                post_engaged_users = graph.get_object(f"/{post['id']}/insights/post_engaged_users")
                post_video_views = graph.get_object(f"/{post['id']}/insights/post_video_views")
                post_reactions = graph.get_object(f"/{post['id']}/insights/post_reactions_by_type_total")
                self.all_posts.append({'message': post['message'], 'id': post['id'],
                                  'Impressions': post_impressions['data'][0]['values'][0]['value'],
                                  'Engaged Users': post_engaged_users['data'][0]['values'][0]['value'],
                                  'Views': video_view_review('lifetime'),
                                  'Likes': reaction_review('like'),
                                  'Laughs': reaction_review('haha'),
                                  'Hearts': reaction_review('love'),
                                  'Wows': reaction_review('wow'),
                                  'Sorry': reaction_review('sorry'),
                                  'Anger': reaction_review('anger')
                                  })
        # TODO 3: Read posts across pages
        def paginate(next_page_posts):
            reached_last_page = False
            while not reached_last_page:
                try:
                    next_page_posts = requests.get(next_page_posts['paging']['next']).json()
                    get_post_info(next_page_posts)
                except KeyError:
                    break

        # TODO 3: Get post IDs:
        until_dt = datetime.datetime.now()
        until = time.mktime(until_dt.timetuple())
        since_dt = until_dt - timedelta(lookback)
        since = time.mktime(since_dt.timetuple())
        next_page_posts = requests.get(f"{fb_post_api['paging']['next']}&since={since}&until={until}").json()
        get_post_info(next_page_posts)
        paginate(next_page_posts)
        return self.all_posts