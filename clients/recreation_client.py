import logging

import requests
import user_agent 

from utils import formatter

LOG = logging.getLogger(__name__)


class RecreationClient:

    BASE_URL = "https://www.recreation.gov"
    AVAILABILITY_ENDPOINT = (
        BASE_URL + "/api/camps/availability/campground/{park_id}/month"
    )
    AVAILABILITY_URL = (
        BASE_URL + "/camping/campgrounds/{park_id}/availability"
    )
    MAIN_PAGE_ENDPOINT = BASE_URL + "/api/camps/campgrounds/{park_id}"

    headers = {"User-Agent": user_agent.generate_user_agent() }
    
    @classmethod
    def get_availability(cls, park_id, month_date):
        params = {"start_date": formatter.format_date(month_date)}
        LOG.debug(
            "Querying for {} with these params: {}".format(park_id, params)
        )
        url = cls.AVAILABILITY_ENDPOINT.format(park_id=park_id)
        resp = cls._send_request(url, params)
        return resp

    @classmethod
    def get_park_name(cls, park_id):
        resp = cls._send_request(
            cls.MAIN_PAGE_ENDPOINT.format(park_id=park_id), {}
        )
        return resp["campground"]["facility_name"]

    @classmethod
    def get_booking_url(cls, park_id):
        return cls.AVAILABILITY_URL.format(park_id=park_id)

    @classmethod
    def _send_request(cls, url, params):
        resp = requests.get(url, params=params, headers=cls.headers)
        if resp.status_code != 200:
            raise RuntimeError(
                "failedRequest",
                "ERROR, {status_code} code received from {url}: {resp_text}".format(
                    status_code=resp.status_code, url=url, resp_text=resp.text
                ),
            )
        return resp.json()
