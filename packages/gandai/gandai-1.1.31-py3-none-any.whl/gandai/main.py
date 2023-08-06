from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from time import time

import pandas as pd
from dacite import from_dict

from gandai import query
from gandai.models import Checkpoint, Company, Event
from gandai.sources import GrataWrapper as grata


def process_event(event_id: int) -> None:
    """
    May trigger additional targets adding to inbox, or something else
    (e.g. a notification)
    """

    e: Event = query.find_event_by_id(event_id)
    search_uid = e.search_uid

    if e.type == "create":
        pass
    elif e.type == "advance":
        # enrich the company
        company = query.find_company_by_domain(e.domain)

        if "company_uid" not in company.meta.keys():
            # adding this check to mitigate API usage
            # revisit this number
            resp = grata.enrich(company.domain)
            if resp.get("status") == 404:
                print(f"{company} not found")  # are we charged for "not found"?
            else:
                print(resp)
                company.name = resp.get("name")
                company.description = resp.get("description")
                company.meta = {**company.meta, **resp}  # merge 3.5+
                query.update_company(company)
        else:
            print(f"{company} already enriched.")

    elif e.type == "validate":
        search = query.find_search_by_uid(search_uid)
        grata_companies = grata.find_similar(domain=e.domain, search=search)
        query.insert_companies_as_targets(
            companies=grata_companies, search_uid=search_uid, actor_key="grata"
        )
        # subscribers (which could be a virtual) could get a notification here
    elif e.type == "send":
        pass
    elif e.type == "accept":
        pass
    elif e.type == "reject":
        pass
    elif e.type == "conflict":
        pass
    elif e.type == "criteria":
        print(f"criteria search for {search_uid}")
        search = query.find_search_by_uid(search_uid)
        grata_companies = grata.find_by_criteria(search)
        query.insert_companies_as_targets(
            companies=grata_companies, search_uid=search_uid, actor_key="grata"
        )

    # finally, record we processed the event
    # could make these async
    query.insert_checkpoint(Checkpoint(event_id=e.id))
    print(f"processed: {e}")


def process_events(search_uid: int) -> int:
    """
    Process all events for a given search
    """

    events = query.event(search_uid=search_uid)
    checkpoints = query.checkpoint(search_uid=search_uid)

    q = list(set(events["id"].tolist()) - set(checkpoints["event_id"].tolist()))

    # for event_id in q:
    #     print(event_id)
    #     process_event(event_id)

    # F2 instance_class defaults to 4 workers
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_event, q)

    return len(q)
