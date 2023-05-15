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
            def video_view_review(post_video_views, period):
                for provided_period in post_video_views['data']:
                    if period in provided_period['period']:
                        video_views = provided_period['values'][0]['value']
                return video_views

            def reaction_review(post_reactions,reaction):
                if reaction in post_reactions['data'][0]['values'][0]['value']:
                    reaction_value = post_reactions['data'][0]['values'][0]['value'][f'{reaction}']
                else:
                    reaction_value = 0
                return reaction_value

            def message_review(post):
                if 'message' in post:
                    title = post['message'].split('\n')[0]
                    date = post['created_time'].split('T')[0]
                    id = post['id']
                else:
                    title = "<No Post Title>"
                    date = post['created_time'].split('T')[0]
                    id = post['id']
                return {'title': title , 'date': date, "id": id}

            video_insights = {}
            def add_insights(post, metric, tag):
                json = graph.get_object(f"/{post['id']}/insights/{metric}")
                video_insights.update({f"{tag}": json})

            for post in page_posts['data']:
                video_insights = {}
                impression_tread = Thread(target = add_insights(post,'post_impressions_unique', 'Unique Impressions'))
                view_thread = Thread(target = add_insights(post,'post_video_views','Views'))
                reaction_thread = Thread(target= add_insights(post,'post_reactions_by_type_total','Reactions'))
                video_summary = {'Title': message_review(post)['title'],
                                 'Date': message_review(post)['date'],
                                 'id': message_review(post)['id']}
                impression_tread.start()
                view_thread.start()
                reaction_thread.start()
                view_thread.join()
                impression_tread.join()
                reaction_thread.join()
                video_summary.update({'Unique Impressions': video_insights['Unique Impressions']['data'][0]['values'][0]['value']})
                video_summary.update({'Views': video_view_review(video_insights['Views'], 'lifetime')})
                video_summary.update({'Likes': reaction_review(video_insights['Reactions'], 'like')})
                video_summary.update({'Hearts': reaction_review(video_insights['Reactions'], 'love')})
                video_summary.update({'Laughs': reaction_review(video_insights['Reactions'], 'haha')})
                video_summary.update({'Wow': reaction_review(video_insights['Reactions'], 'wow')})
                video_summary.update({'Anger': reaction_review(video_insights['Reactions'], 'anger')})
                video_summary.update({'Sorry': reaction_review(video_insights['Reactions'], 'sorry')})
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

            video_insights={}
            def add_insights(video, metric, tag):
                json = graph.get_object(f"/{video['id']}/video_insights/{metric}")
                video_insights.update({f"{tag}": json})

            for video in page['data']:
                video_insights = {}
                impression_thread = Thread(target=add_insights(video,'total_video_impressions_unique','Unique Impressions'))
                view_thread = Thread(target=add_insights(video,'total_video_views','Views'))
                reaction_thread = Thread(target=add_insights(video,'total_video_reactions_by_type_total','Reactions'))
                video_summary = {
                            'Title': video['description'],
                            'Date': video['updated_time'].split('T')[0]
                }
                impression_thread.start()
                view_thread.start()
                reaction_thread.start()

                impression_thread.join()
                view_thread.join()
                reaction_thread.join()

                for item in video_insights['Unique Impressions']['data']:
                    video_summary.update({'Unique Impressions': item['values'][0]['value']})
                for item in video_insights['Views']['data']:
                    video_summary.update({'Views': item['values'][0]['value']})
                for reaction in video_insights['Reactions']['data']:
                    video_summary.update({'Likes': reaction_review(reaction, 'like')})
                    video_summary.update({'Hearts': reaction_review(reaction, 'love')})
                    video_summary.update({'Laughs': reaction_review(reaction, 'haha')})
                    video_summary.update({'Wow': reaction_review(reaction, 'wow')})
                    video_summary.update({'Sorry': reaction_review(reaction, 'sorry')})
                    video_summary.update({'Anger': reaction_review(reaction, 'anger')})
                self.all_videos.append(video_summary)
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

        reel_insights = {}
        def add_insights(reel, metric, tag):
            json = graph.get_object(f"/{reel['id']}/video_insights/{metric}")
            reel_insights.update({f"{tag}": json})
        def get_reel_info(api):
            for reel in api['data']:
                threaded_views = Thread(target=add_insights(reel, 'blue_reels_play_count', 'Views'))
                threaded_impressions = Thread(target=add_insights(reel, 'post_impressions_unique', 'Unique Impressions'))
                threaded_reactions = Thread(target=add_insights(reel, 'post_video_likes_by_reaction_type', 'Reactions'))
                # ['data'][0]
                def reaction_reivew(json,reaction):
                    if reaction in json['values'][0]['value']:
                        counts = json['values'][0]['value'][reaction]
                    else:
                        counts = 0
                    return counts

                reel_summary = {
                    'Title': reel['description'],
                    'Date': reel['updated_time'].split('T')[0]
                }
                    # 'Likes': reaction_reivew(reactions, 'REACTION_LIKE'),
                    # 'Laughs': reaction_reivew(reactions, 'REACTION_HAHA'),
                    # 'Hearts': reaction_reivew(reactions, 'REACTION_LOVE'),
                    # 'Wows': reaction_reivew(reactions, 'REACTION_WOW'),
                    # 'Sorry': reaction_reivew(reactions, 'REACTION_SORRY'),
                    # 'Anger': reaction_reivew(reactions, 'REACTION_ANGER')
                threaded_impressions.start()
                threaded_views.start()
                threaded_reactions.start()

                threaded_impressions.join()
                threaded_views.join()
                threaded_reactions.join()

                for item in reel_insights['Views']['data']:
                    reel_summary.update({'Views': item['values'][0]['value']})
                for item in reel_insights['Unique Impressions']['data']:
                    reel_summary.update({'Unique Impressions': item['values'][0]['value']})
                for item in reel_insights['Reactions']['data']:
                    reel_summary.update({'Likes': reaction_reivew(item,'REACTION_LIKE')})
                    reel_summary.update({'Laughs': reaction_reivew(item, 'REACTION_HAHA')})
                    reel_summary.update({'Hearts': reaction_reivew(item, 'REACTION_LOVE')})
                    reel_summary.update({'Wow': reaction_reivew(item, 'REACTION_WOW')})
                    reel_summary.update({'Sorry': reaction_reivew(item, 'REACTION_SORRY')})
                    reel_summary.update({'Anger': reaction_reivew(item, 'REACTION_ANGER')})


                self.all_reels.append(reel_summary)
        get_reel_info(fb_page_reels_api)