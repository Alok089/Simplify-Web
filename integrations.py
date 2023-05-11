import facebook
import requests
import time
import datetime
from datetime import timedelta
from threading import Thread

class Facebook:
    def __init__(self, user_access_token):
        self.token = user_access_token
        self.all_posts = []
        self.all_reels = []
        self.all_videos = []

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
    def get_posts(self, page_name):
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
        def get_post_info(page_posts):
            def video_view_review(period):
                for provided_period in post_video_views['data']:
                    if period in provided_period['period']:
                        video_views = provided_period['values'][0]['value']
                return video_views

            def reaction_review(reaction):
                if reaction in post_reactions['data'][0]['values'][0]['value']:
                    reaction_value = post_reactions['data'][0]['values'][0]['value'][f'{reaction}']
                else:
                    reaction_value = 0
                return reaction_value

            def message_review(post):
                if 'message' in post:
                    title = post['message'].split('\n')[0]
                    date = post['created_time'].split('T')[0]
                else:
                    title = "<No Post Title>"
                    date = post['created_time'].split('T')[0]
                return {'title': title , 'date': date}

            video_insights = []
            def add_insights(post, metric, tag):
                json = graph.get_object(f"/{post['id']}/insights/{metric}")
                video_insights.append({f"{tag}": json})

            for post in page_posts['data']:
                impressions = Thread(target = add_insights(post,'post_impressions_unique', 'Unique Impressions'))
                post_video_views = graph.get_object(f"/{post['id']}/insights/post_video_views")
                post_reactions = graph.get_object(f"/{post['id']}/insights/post_reactions_by_type_total")
                video_summary = {'Title': message_review(post)['title'],
                                 'Date': message_review(post)['date'],
                                 'Views': video_view_review('lifetime'),
                                 'Likes': reaction_review('like'),
                                 'Laughs': reaction_review('haha'),
                                 'Hearts': reaction_review('love'),
                                 'Wows': reaction_review('wow'),
                                 'Sorry': reaction_review('sorry'),
                                 'Anger': reaction_review('anger')
                                       }
                for insight in video_insights:
                    if insight['id'] == post['id']:
                        video_summary.update(
                            {'Unique Impressions by function': insight['Unique Impressions by function']})
                self.all_posts.append(video_summary)



        # TODO 3: Get post IDs:
        single_page_posts = fb_post_api
        get_post_info(single_page_posts)
    def get_videos(self, page_name):
        fb = Facebook(self.token)
        page_details = fb.get_pages()
        for page in page_details['data']:
            if page['Name'] == page_name:
                access_token = page['AccessToken']
                page_id = page['id']
        graph = facebook.GraphAPI(access_token=access_token, version="2.12")
        fb_page_videos_api = graph.get_object(f"/{page_id}/videos")
        def get_video_info(page):
            def reaction_review(api, reaction):
                if reaction in api['values'][0]['value']:
                    reaction_value = api['values'][0]['value'][f'{reaction}']
                else:
                    reaction_value = 0
                return reaction_value
            for video in page['data']:
                unique_impressions = graph.get_object(f"{video['id']}/video_insights/total_video_impressions_unique")['data']
                views = graph.get_object(f"{video['id']}/video_insights/total_video_views")['data']
                reactions = graph.get_object(f"{video['id']}/video_insights/total_video_reactions_by_type_total")
                for reaction in reactions['data']:
                    if reaction['period'] == 'lifetime':
                        self.all_videos.append({
                            'Title': video['description'],
                            'Date': video['updated_time'].split('T')[0],
                            'Unique Impressions': unique_impressions[0]['values'][0]['value'],
                            'Views': views[0]['values'][0]['value'],
                            'Likes': reaction_review(reaction, 'like'),
                            'Laughs': reaction_review(reaction, 'haha'),
                            'Hearts': reaction_review(reaction, 'love'),
                            'Wows': reaction_review(reaction, 'wow'),
                            'Sorry': reaction_review(reaction, 'sorry'),
                            'Anger': reaction_review(reaction, 'anger')})

        get_video_info(fb_page_videos_api)
    def get_reels(self, page_name):
        fb = Facebook(self.token)
        page_details = fb.get_pages()
        for page in page_details['data']:
            if page['Name'] == page_name:
                access_token = page['AccessToken']
                page_id = page['id']
        graph = facebook.GraphAPI(access_token=access_token, version="2.12")
        fb_page_reels_api = graph.get_object(f"/{page_id}/video_reels")
        def get_reel_info(api):
            for reel in api['data']:
                # reel_impressions = graph.get_object(f"/{reel['id']}/video_insights/post_impressions_unique")
                views = graph.get_object(f"/{reel['id']}/video_insights/blue_reels_play_count")['data'][0]['values'][0]['value']
                unique_impressions = graph.get_object(f"/{reel['id']}/video_insights/post_impressions_unique")['data'][0]['values'][0]['value']
                reactions = graph.get_object(f"/{reel['id']}/video_insights/post_video_likes_by_reaction_type")['data'][0]
                def reaction_reivew(json,reaction):
                    if reaction in json['values'][0]['value']:
                        counts = json['values'][0]['value'][reaction]
                    else:
                        counts = 0
                    return counts

                self.all_reels.append({
                    'Title': reel['description'],
                    'Date': reel['updated_time'].split('T')[0],
                    'Unique Impressions': unique_impressions,
                    'Views': views,
                    'Likes': reaction_reivew(reactions, 'REACTION_LIKE'),
                    'Laughs': reaction_reivew(reactions, 'REACTION_HAHA'),
                    'Hearts': reaction_reivew(reactions, 'REACTION_LOVE'),
                    'Wows': reaction_reivew(reactions, 'REACTION_WOW'),
                    'Sorry': reaction_reivew(reactions, 'REACTION_SORRY'),
                    'Anger': reaction_reivew(reactions, 'REACTION_ANGER')})
        get_reel_info(fb_page_reels_api)

fb = Facebook("EABQUuk5VBgUBAJBydI679ZBAfB5T30LefG56YCGoVid63H7SJJf1wowHiTohsYokH2ZBcITAWYq0mRzR6e0tCPbtlpNa7etbpsMNUO5yjZCc7ExIha8JaxWKEZAZAukFAZCxainPs5eyNktO00xgopLjim8NLOkcMEDG8m54HLb5frek6gUCUZC6fmcqBbxVzkEnmOVjfmNrwZDZD")

fb.get_posts("Action Reeplayy")
# Thread(target = fb.get_posts("Action Reeplayy")).start()
# Thread(target = fb.get_videos("Action Reeplayy")).start()
# Thread(target = fb.get_reels("Action Reeplayy")).start()
#
print(fb.all_posts)
# print(fb.all_videos)
# print(fb.all_reels)
