class Status:
    def __init__(self, bid, id, mid, attitudes_count, reposts_count, comments_count, created_at, edit_at, raw_text, user, page_info, pics):
        self.bid = bid
        self.attitudes_count = attitudes_count
        self.reposts_count = reposts_count
        self.comments_count = comments_count
        self.created_at = created_at
        self.edit_at = edit_at
        self.raw_text = raw_text if raw_text is not None else ' '
        self.user = user
        self.page_info = page_info if page_info is not None else ' '
        self.pics = pics if pics is not None else ' '
        self.id = id
        self.mid = mid


class Page_info:
    def __init__(self, mid, content1, content2, page_url, page_title, play_count, title, type, urls):
        self.mid = mid
        self.content1 = content1 if content1 is not None else ' '
        self.content2 = content2 if content2 is not None else ' '
        self.page_url = page_url if page_url is not None else ' '
        self.page_title = page_title if page_title is not None else ' '
        self.play_count = play_count
        self.title = title if title is not None else ' '
        self.type = type if type is not None else ' '
        self.urls = urls


class User:
    def __init__(self, id, avatar_hd, description, follow_count, followers_count,
                 gender, profile_url, screen_name):
        self.id = id
        self.avatar_hd = avatar_hd if avatar_hd is not None else ' '
        self.description = description if description is not None else ' '
        self.follow_count = follow_count
        self.followers_count = followers_count
        self.gender = gender
        self.profile_url = profile_url
        self.screen_name = screen_name if screen_name is not None else ' '


class Comments:
    def __init__(self, id, bid, created_at, like_count, text, source, user):
        self.id = id
        self.bid = bid
        self.created_at = created_at
        self.like_count = like_count
        self.text = text if text is not None else ' '
        self.source = source
        self.user = user
