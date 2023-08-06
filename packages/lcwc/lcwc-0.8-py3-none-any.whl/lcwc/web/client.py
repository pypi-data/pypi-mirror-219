import datetime
import aiohttp
import pytz
from bs4 import BeautifulSoup
from lcwc import Client
from lcwc.category import IncidentCategory
from lcwc.unit import Unit
from lcwc.web.incident import WebIncident as Incident

DATE_FORMAT = "%a, %b %d, %Y %H:%M"
""" The date format used on the LCWC website """


class WebClient(Client):
    """Client for scraping the live incident page"""

    URL = "https://www.lcwc911.us/live-incident-list"
    """ The URL of the live incident page """

    @property
    def name(self) -> str:
        """Returns the name of the client"""
        return "WebClient"

    async def get_incidents(
        self, session: aiohttp.ClientSession, timeout: int = 10
    ) -> list[Incident]:
        """Fetches the live incident page and returns a list of incidents

        :param session: The aiohttp session to use
        :param timeout: The timeout in seconds
        :return: A list of incidents
        :rtype: list[Incident]
        """
        html = None
        async with session.get(self.URL, timeout=timeout) as resp:
            if resp.status == 200:
                html = await resp.read()
            else:
                raise Exception(f"Unable to fetch live incident page: {resp.status}")

        active_incidents = self.__parse(html)
        return active_incidents

    def __parse(self, page_html: bytes) -> list[Incident]:
        """Parses the live incident page and returns a list of incidents

        :param page_html: The html of the live incident page
        :return: A list of incidents
        :rtype: list[Incident]
        """

        incidents = []

        soup = BeautifulSoup(page_html, "html.parser")
        containers = soup.find_all("div", class_="live-incident-container")

        for container in containers:
            header = container.find("h2").text
            category = IncidentCategory[header.split()[1].upper()]

            table = container.find("table", class_="live-incidents")

            rows = table.find_all("tr")

            for row in rows:
                date_row = row.find("td", class_="date-row")
                incident_row = row.find("td", class_="incident-row")
                location_row = row.find("td", class_="location-row")
                units_row = row.find("td", class_="units-row")

                if (
                    not date_row
                    or not incident_row
                    or not location_row
                    or not units_row
                ):
                    continue

                # convert date to UTC
                local_tz = pytz.timezone("America/New_York")
                raw_date = datetime.datetime.strptime(
                    date_row.text.strip(), DATE_FORMAT
                )
                local_dt = local_tz.localize(raw_date, is_dst=None)
                date = local_dt.astimezone(pytz.utc)

                description = incident_row.text.strip().strip()

                # split location by street(s) and municipality (if applicable)
                location = [l.strip() for l in location_row.text.strip().split("\n")]

                if len(location) == 1:
                    intersection = None
                    municipality = location[0]
                else:
                    intersection = location[0]
                    municipality = location[1]

                # we have to decode manually because of internal <br/> tags
                unit_names = [
                    u.strip()
                    for u in units_row.decode_contents().strip().split("<br/>")
                ]

                units = [Unit(u) for u in unit_names if u != ""]

                incident = Incident(
                    category, date, description, municipality, intersection, units
                )
                incidents.append(incident)

        return incidents
