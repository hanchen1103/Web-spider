class Status:
    def __init__(self, bid, id, mid, attitudes_count, reposts_count, comments_count, created_at, edit_at, raw_text, user, page_info, pics):
        self.bid = bid
        self.attitudes_count = attitudes_count
        self.reposts_count = reposts_count
        self.comments_count = comments_count
        self.created_at = created_at
        self.edit_at = edit_at
        self.raw_text = raw_text
        self.user = user
        self.page_info = page_info
        self.pics = pics
        self.id = id
        self.mid = mid


class Page_info:
    def __init__(self, content1, content2, page_url, page_title, play_count, title, type, urls):
        self.content1 = content1
        self.content2 = content2
        self.page_url = page_url
        self.page_title = page_title
        self.play_count = play_count
        self.title = title
        self.type = type
        self.urls = urls


class User:
    def __init__(self, id, avatar_hd, description, follow_count, followers_count,
                 gender, profile_url, screen_name):
        self.id = id
        self.avatar_hd = avatar_hd
        self.description = description
        self.follow_count = follow_count
        self.followers_count = followers_count
        self.gender = gender
        self.profile_url = profile_url
        self.screen_name = screen_name


class Comments:
    def __init__(self, id, bid, created_at, like_count, text, source, user):
        self.id = id
        self.bid = bid
        self.created_at = created_at
        self.like_count = like_count
        self.text = text
        self.source = source
        self.user = user
