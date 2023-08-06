import requests
import googlemaps
import time

from gandai.models import Search
from gandai import secrets, models

gmaps = googlemaps.Client(key=secrets.access_secret_version("GOOLE_MAPS_KEY"))

class GoogleMapsWrapper:
    @staticmethod
    def find_by_criteria(phrase: str, location: str, miles=50):
        def get_loc(text: str = "San Diego, CA") -> tuple:
            resp = gmaps.geocode(text)
            return tuple(resp[0]["geometry"]["location"].values())

        METERS_PER_MILE = 1609.34
        loc = get_loc(location)
        results = []
        next_page_token = None

        response = gmaps.places(
            query=phrase,
            location=loc,
            radius=(miles * METERS_PER_MILE),
        )
        results.extend(response["results"])
        next_page_token = response.get("next_page_token", None)
        while next_page_token:
            time.sleep(1)
            # print(next_page_token)
            response = gmaps.places(
                query=phrase,
                location=loc,
                radius=(miles * METERS_PER_MILE),
                page_token=next_page_token,
            )
            results.extend(response["results"])
            next_page_token = response.get("next_page_token", None)
        print(len(results))
        return results

    @staticmethod
    def enrich(place_id: str) -> dict:
        resp = gmaps.place(place_id=place_id)
        return resp["result"]


class GrataWrapper:
    HEADERS = {
        "Authorization": secrets.access_secret_version("GRATA_API_TOKEN"),
        "Content-Type": "application/json",
    }
    
    def find_similar(domain: str, search: models.Search) -> list:
        api_filters = GrataWrapper._get_api_filter(search)
        response = requests.post(
            "https://search.grata.com/api/v1.2/search-similar/",
            headers=GrataWrapper.HEADERS,
            json={
                "domain": domain,
                "grata_employees_estimates_range": api_filters["grata_employees_estimates_range"],
                "headquarters": api_filters["headquarters"],
            },
        )
        data = response.json()
        print("find_similar:", data)
        data["companies"] = data.get("results", [])  # asking grata about this

        return data["companies"]

    def find_by_criteria(search: models.Search) -> dict:
        api_filters = GrataWrapper._get_api_filter(search)
        response = requests.post(
            "https://search.grata.com/api/v1.2/search/",
            headers=GrataWrapper.HEADERS,
            json=api_filters,
        )
        data = response.json()
        print("find_by_criteria: ", data)
        return data["companies"]

    def enrich(domain: str) -> dict:
        response = requests.post(
            "https://search.grata.com/api/v1.2/enrich/",
            headers=GrataWrapper.HEADERS,
            json={"domain": domain},
        )
        data = response.json()
        data["linkedin"] = data.get("social_linkedin")
        data["ownership"] = data.get("ownership_status")
        return data

    def _get_api_filter(search: models.Search) -> dict:
        STATES = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
        }

        COUNTRIES = {
            "USA": "United States",
            "CAN": "Canada",
            "MEX": "Mexico",
            "GBR": "United Kingdom",
        }

        def _hq_include() -> list:
            include = []
            cities = search.inclusion.get("city", [])
            states = search.inclusion.get("state", [])
            countries = search.inclusion.get("country", [])

            # GRATA BUG - in progress with them
            if len(cities) > 0:
                # front-end validates only one state when city selected
                state = STATES[states[0]]
                for city in cities:
                    include.append(
                        {"city": city, "state": state, "country": "United States"}
                    )
                return include
            
            if len(states) > 0:
                for state in states:
                    # NB: API wants full state name, but product wants state code
                    include.append({"state": STATES[state]})

            if len(countries) > 0:
                for country in countries:
                    include.append({"country": COUNTRIES[country]})
            return include

        def _hq_exclude() -> list:
            exclude = []
            for state in search.exclusion.get("state", []):
                exclude.append({"state": STATES[state]})
            return exclude

        return {
            "op": "any",
            "include": search.inclusion.get("keywords", []),
            "exclude": search.exclusion.get("keywords", []),
            "grata_employees_estimates_range": search.inclusion.get("employees_range", []),
            "ownership": search.inclusion.get("ownership", ""),
            "headquarters": {
                "include": _hq_include(),
                "exclude": _hq_exclude(),
            },
        }

class SourceScrubWrapper:
    def find_similar(domain: str, search: Search) -> dict:
        pass

    def find_by_criteria(search: Search) -> dict:
        pass

    def enrich(domain: str) -> dict:
        pass
