import datetime
from database import db, Attribute, Inference_Attributes, Inference_Association
from flask import Flask
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6WlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///simplify-web.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.app_context().push()



def existing_info(cat_value, category):
    for category in db.engine.execute(f'SELECT distinct category_id FROM inference_categories where value = "{cat_value}" and category = "{category}"'):
        category_id = category[0]
    existing_names = []
    for actor in db.engine.execute('SELECT distinct value FROM inference_attributes where attribute = "name";'):
        existing_names.append(actor[0])
    for record in db.engine.execute('SELECT count(distinct item_id) as item_count FROM inference_attributes;'):
        item_count = record[0]
    return {'category_id': category_id , 'existing names': existing_names,
            'item count': item_count}
def api_lookup(api_url,attribute,value):
    parameter = f"?{attribute}={value}"
    usr_inferred_response = requests.get(api_url + parameter, headers={'X-Api-Key': '2dtBpbUvz/bm0nU5wi+UaA==ymxNBBSwgxsTScx4'})
    api_dataset = usr_inferred_response.json()
    return api_dataset
# 'Entertainment', 'Celebrities'
def user_inferance(cat_value,category,dataset,lookup_attribute):
    current_dataset = existing_info(cat_value, category)
    category_id = current_dataset['category_id']
    existing_names = current_dataset['existing names']
    item_count = current_dataset['item count']
    for item in dataset:
        for attribute in item.keys():
            if type(item[attribute]) == type(""):
                if str.lower(item[lookup_attribute]) not in existing_names:
                    for new_attribute in item.keys():
                        if type(item[new_attribute]) == type(""):
                            record = Inference_Attributes(attribute=new_attribute,
                                                          value=str.lower(item[new_attribute]),
                                                          item_id = item_count + 1)
                            db.session.add(record)
                            db.session.commit()
                    association = Inference_Association(category_id = category_id,
                                                        item_id = item_count + 1)
                    db.session.add(association)
                    db.session.commit()
                    return True

def store_inference_as_attribute(cat_val,inference_attribute,matching_attribute):
    record_added = False
    existing_inferences = f"""select ic2.value as "Category",ia.value '{inference_attribute}' 
    from inference_association ic 
    inner join inference_attributes ia on ic.item_id = ia.item_id 
    inner join inference_categories ic2 on ic2.category_id = ic.category_id
    where lower(ia."attribute") = lower('{inference_attribute}');"""
    inference_list = []
    for inference in db.engine.execute(existing_inferences):
        item = {inference[0]: inference[1]}
        inference_list.append(item)
    # print(inference_list)
    matching_resultset = f"select item_id,value from attributes a where attribute = '{matching_attribute}';"
    test_list = []
    for record in db.engine.execute(matching_resultset):
        test = {record[0]:record[1]}
        test_list.append(test)

    for record in test_list:
        for item_id in record.keys():
            for inference in inference_list:
                if str.lower(inference[cat_val]) in str.lower(record[item_id]):
                    record_exists = False
                    existing_attributeqry = f"""select attribute,value
                         from attributes where item_id = {item_id} and attribute = '{cat_val}';"""
                    existing_attributes = []
                    for attribute_record in db.engine.execute(existing_attributeqry):
                        existing_attributes.append({attribute_record[0]:attribute_record[1]})
                    for attribute in existing_attributes:
                        for key in attribute.keys():
                            if str.lower(key) == str.lower(cat_val) and \
                                    str.lower(attribute[key]) == str.lower(inference[cat_val]):
                                record_exists = True
                            else:
                                record_exists = False
                    if record_exists == False:
                        add_inference = Attribute(
                            attribute=cat_val,
                            value=inference[cat_val],
                            item_id=item_id,
                            item_analyzed_on=datetime.date.today()
                        )
                        db.session.add(add_inference)
                        db.session.commit()

def teach_model(category,cat_value,inferring_attribute,value,target_attribute):
    store_inference_as_attribute(cat_value, inferring_attribute, target_attribute)
    api_url = f'https://api.api-ninjas.com/v1/celebrity'
    api_found = api_lookup(api_url, inferring_attribute, value)
    if len(api_found) > 0:
        user_inferance(cat_value, category, api_found, inferring_attribute)
    else:
        user_inferance(cat_value, category, [{inferring_attribute: value}], inferring_attribute)
    store_inference_as_attribute(cat_value, inferring_attribute, target_attribute)
def build_default_view():
    video_query = """with video_list as (select distinct item_id from "attributes" a where attribute = 'Item' and value = "Video"),
         video_title as (select distinct item_id,value from "attributes" a where attribute = 'Title'),
         video_date as (select distinct item_id,value from "attributes" a where attribute = 'Date'),
         video_views as (select distinct item_id,value from "attributes" a where attribute = 'Views'),
         video_impressions as (select distinct item_id,value from "attributes" a where attribute = 'Unique Impressions'),
         video_likes as (select distinct item_id,value from "attributes" a where attribute = 'Likes'),
         video_hearts as (select distinct item_id,value from "attributes" a where attribute = 'Hearts')
         select vl.item_id, vt.value "Title", vd.value "Date",vi.value "Impressions", vv.value "Views",vlk.value "Likes",vh.value "Hearts"
         from video_list vl 
         left join video_title vt on vl.item_id = vt.item_id
         left join video_date vd on vd.item_id = vl.item_id
         left join video_impressions vi on vi.item_id = vl.item_id
         left join video_views vv on vv.item_id = vl.item_id
         left join video_likes vlk on vlk.item_id = vl.item_id
         left join video_hearts vh on vh.item_id = vl.item_id;"""

    all_videos = []
    for video in db.session.execute(video_query):
        all_videos.append({'id': video[0],
                           'Title': video[1],
                           'Date': video[2],
                           'Impressions': video[3],
                           'Views':video[4],
                           'Likes':video[5],
                           'Hearts':video[6]})

    celebs = """select distinct item_id,value from attributes a 
    where attribute = 'Celebrities';"""
    all_celebs = []
    for celeb in db.session.execute(celebs):
        all_celebs.append({celeb[0]: celeb[1]})

    for record in all_videos:
        celebs_in_record = []
        for value in all_celebs:
            for key in value.keys():
                if key == record['id']:
                    celebs_in_record.append(value[key])
                    record['celebs']=celebs_in_record
    return all_videos