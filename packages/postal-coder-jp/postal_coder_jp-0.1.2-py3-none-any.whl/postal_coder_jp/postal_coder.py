import pickle

with open('../data/post_code_master.pkl', 'rb') as file:
    df_post = pickle.load(file)

def postal_coder(postal_code):
    df_post_extracted = df_post.loc[df_post["post_code"] == postal_code]
    return df_post_extracted.loc[:, ['prefectures', 'city', 'town', 'latitude', 'longitude']].to_dict(orient='records')