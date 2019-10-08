# coding=utf8

from geektime_dl.data_client.gk_apis import GkApiClient

course_keys_needed = {
    'id', 'column_title', 'had_sub', 'is_finish', 'update_frequency'
}
post_keys_needed = {
    'id', 'article_title', 'article_content', 'column_id'
}
comment_keys_needed = {
    'user_name', 'like_count', 'comment_content', 'comment_ctime'
}
daily_video_keys_needed = {
    'id', 'article_title', 'column_had_sub', 'video_media_map'
}

video_id = 2184
collection_id = 141
daily_id = 113850


def test_api_get_course_list(gk: GkApiClient):
    res = gk.get_course_list()

    assert isinstance(res, dict)
    assert {'1', '2', '3', '4'} & set(res.keys())
    for type_ in {'1', '2', '3', '4'}:
        course_list = res[type_]['list']
        course = course_list[0]
        assert isinstance(course, dict)
        for key in course_keys_needed:
            assert course.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_course_intro(gk: GkApiClient, column_id):
    course = gk.get_course_intro(column_id)
    assert isinstance(course, dict)
    for key in course_keys_needed:
        assert course.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_course_post_list(gk: GkApiClient, column_id):
    course = gk.get_post_list_of(column_id)
    assert course and isinstance(course, list)
    article = course[0]
    for key in {'id'}:
        assert article.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_post_content(gk: GkApiClient, article_id):
    article = gk.get_post_content(article_id)
    assert article and isinstance(article, dict)
    for key in post_keys_needed:
        assert article.get(key) is not None, '{} 不存在'.format(key)

    # mp3
    assert article.get('audio_download_url')
    # mp4
    article = gk.get_post_content(video_id)
    vm = article.get('video_media_map')
    assert vm, 'video_media_map 不存在'
    assert vm['sd']['url']
    assert vm['hd']['url']


def test_api_get_post_comments(gk: GkApiClient, article_id):
    res = gk.get_post_comments(article_id)
    assert res and isinstance(res, list)
    comment = res[0]
    for key in comment_keys_needed:
        assert comment.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_video_collection_intro(gk: GkApiClient):
    course = gk.get_video_collection_intro(collection_id)
    assert isinstance(course, dict)
    for key in {'cid', 'title'}:
        assert course.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_video_collection_list(gk: GkApiClient):
    col_list = gk.get_video_collection_list()
    assert col_list and isinstance(col_list, list)
    col = col_list[0]
    for key in {'collection_id'}:
        assert col.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_collection_video_list(gk: GkApiClient):
    v_list = gk.get_video_list_of(collection_id)
    assert v_list and isinstance(v_list, list)
    video = v_list[0]
    for key in {'article_id', 'is_sub'}:
        assert video.get(key) is not None, '{} 不存在'.format(key)


def test_api_get_vedio_content(gk: GkApiClient):
    video = gk.get_post_content(daily_id)
    assert video and isinstance(video, dict)
    for key in daily_video_keys_needed:
        assert video.get(key) is not None, '{} 不存在'.format(key)

    # video_url
    assert 'video_media_map' in video
    # assert vm['sd']['url']
    # assert vm['hd']['url']
