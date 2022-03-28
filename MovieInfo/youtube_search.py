# API client library
import googleapiclient.discovery

# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = 'AIzaSyAksptMU8oYDx518a9n-mKCO2RBoXz3ywY'
BASE_YOUTUBE_URL = "https://youtu.be/"

# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def __search_youtube(msg):
    fields = "items(id(videoId),snippet(publishedAt,title))"

    # Request body
    request = youtube.search().list(
        part="id,snippet",
        q=msg,
        maxResults=1,
        regionCode="IN",  # only indian vid
        type="video",
        # order="date",
        videoType="movie",  # This doesn't really work
        fields=fields  # only returns IDs title and date
    )
    # Request execution
    response = request.execute()
    return response


def __get_title_and_link_from_response(response):
    if len(response['items']) == 0:
        return -1, -1
    link = BASE_YOUTUBE_URL + response['items'][0]['id']['videoId']
    title = response['items'][0]['snippet']['title']
    return link, title


def __get_title_and_link(msg):
    response = __search_youtube(msg)
    return __get_title_and_link_from_response(response)


def get_msg_with_youtube_details(msg):
    link, title = __get_title_and_link(msg)
    return "YouTube Search: " + link  ## title comes in WA anyways
