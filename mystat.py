import requests
import sys
import re
import config
import logging
from bs4 import BeautifulSoup


# Logging configuration
# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_status():
    """This function will do the ff:
        1. Make a post request to the uscis url along with the required parameters
        2. Parse the html response to get the case status
    """
    header = {
        "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    url = (
        "https://egov.uscis.gov/casestatus/mycasestatus.do"
    )
    case_nbr = config.CASE_NBR
    payload = {
        "changeLocale": "",
        "appReceiptNum": case_nbr,
        "initCaseSearch": "CHECK STATUS",
    }
    r = requests.post(url, headers=header, data=payload)
    if r.status_code == 200:
        ok_msg = "Success! See case status below."
        logger.info(ok_msg)
        bs = BeautifulSoup(r.content, "html.parser")
        case_status = bs.find(
            "div", "current-status-sec"
        ).text.replace("Your Current Status:", "")
        case_status = re.sub(r"[\t\n\r+]", "", case_status)
        detail = bs.find("div", "rows text-center").text
        short_detail = detail.split(".")
        logger.info(short_detail[0])

    else:
        error_msg = "Error in getting status code"
        logger.info(error_msg)


if __name__ == "__main__":
    logger.info("Case Status Search Started...")
    get_status()
