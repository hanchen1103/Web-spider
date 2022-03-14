class status:
    def __init__(self, bid, comments_count, created_at, edit_at, raw_text, user, page_info, pics):
        self.bid = bid
        self.comments_count = comments_count
        self.created_at = created_at
        self.edit_at = edit_at
        self.raw_text = raw_text
        self.user = user
        self.page_info = page_info
        self.pics = pics


class page_info:
    def __init__(self, content1, content2, page_url, page_title, play_count, title, type, urls):
        self.content1 = content1
        self.content2 = content2
        self.page_url = page_url
        self.page_title = page_title
        self.play_count = play_count
        self.title = title
        self.type = type
        self.urls = urls


class user:
    def __init__(self, id, avatar_hd, description, follow_count, followers_count,
                 gender, profile_url, screen_name):
        self.id = id
        self.avatar_hd = avatar_hd
        self.description = description
        self.follow_count = followers_count
        self.gender = gender
        self.profile_url = profile_url
        self.screen_name = screen_name
