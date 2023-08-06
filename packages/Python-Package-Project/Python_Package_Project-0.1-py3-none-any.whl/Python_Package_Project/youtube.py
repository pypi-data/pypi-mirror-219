from IPython.display import HTML
from IPython.display import display
from ensure import ensure_annotations
from Python_Package_Project.custom_exception import InvalidURLException
from Python_Package_Project.logger import logger
from py_youtube import Data


@ensure_annotations
def get_time_info(URL: str) -> int:
    def _verify_video_id_len(video_id, __expected_len=11):
        len_of_video_id = len(video_id)
        if len_of_video_id != __expected_len:
            raise InvalidURLException(
                f"Invalid Video Id with Length : {len_of_video_id}, expected is : {__expected_len} "
            )

    try:
        split_value = URL.split("=")
        if len(split_value) > 3:
            raise InvalidURLException

        elif "=" in URL and "&ab_channel" in URL:  # edge_youtube_link
            video_id, time = split_value[-2].split("&")[0], 0
            _verify_video_id_len(video_id)
            logger.info(f"Video starts at: {time}")
            return time

        elif "watch" in URL:
            if "&t" in URL:
                video_id, time = split_value[-2][:-2], int(split_value[-1][:-1])
                _verify_video_id_len(video_id)
                logger.info(f"Video starts at: {time}")
                return time
            else:
                video_id, time = split_value[-1], 0
                _verify_video_id_len(video_id)
                logger.info(f"Video starts at: {time}")
                return time
        else:
            if "=" in URL and "?t" in URL:
                video_id, time = split_value[0].split("/")[-1][:-2], int(
                    split_value[1][:-1]
                )
                _verify_video_id_len(video_id)
                logger.info(f"Video starts at: {time}")
                return time
            else:
                video_id, time = split_value[0].split("/")[-1], 0
                _verify_video_id_len(video_id)
                logger.info(f"Video starts at: {time}")
                return time
    except Exception:
        raise InvalidURLException


@ensure_annotations
def render_youtube(URL: str, width: int = 800, height: int = 600) -> str:
    try:
        if URL is None:
            raise InvalidURLException("URL cannot be None")
        data = Data(URL).data()
        if data["publishdate"] is not None:
            time = get_time_info(URL)
            video_id = data["id"]
            embed_URL = f"https://www.youtube.com/embed/{video_id}?start={time}"
            logger.info(f"embed URL: {embed_URL}")
            iframe = f"""<iframe width="{width}" height="{height}" src="{embed_URL}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>"""
            display(HTML(iframe))
            return "sucess"
        else:
            raise InvalidURLException
    except Exception as e:
        raise e
