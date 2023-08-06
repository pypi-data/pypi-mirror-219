import json
from dataclasses import asdict
from typing import Any, List

import pandas as pd
import sqlalchemy
from dacite import from_dict
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector

load_dotenv()

from gandai.models import Actor, Checkpoint, Company, Event, EventType, Search


from gandai import helpers

from gandai.db import connect_with_connector

db = connect_with_connector()


### WRITES ###


def insert_company(company: Company):
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO company (domain, name, description) 
                VALUES(:domain, :name, :description)
                ON CONFLICT DO NOTHING
            """
        )
        con.execute(statement, asdict(company))
        con.commit()
    return company #todo this should return the id


def insert_event(event: Event) -> Event:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO event (search_uid, domain, actor_key, type, data) 
                VALUES(:search_uid, :domain, :actor_key, :type, :data)
                ON CONFLICT DO NOTHING
                RETURNING id
            """
        )
        obj = asdict(event)
        obj["data"] = json.dumps(obj["data"])
        result = con.execute(statement, obj)
        # print(result.first())
        _id = result.first()
        event.id = _id[0] if _id else None
        # con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW target"))
        con.commit()
    return event


def insert_actor(actor: Actor) -> Actor:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO actor (key, type, name) 
                VALUES(:key, :type, :name)
                ON CONFLICT DO NOTHING
            """
        )
        obj = asdict(actor)
        con.execute(statement, obj)
        con.commit()
    return actor


def insert_search(search: Search) -> Search:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO search (uid, client_domain, label, meta, inclusion, exclusion, sort) 
                VALUES(:uid, :client_domain, :label, :meta, :inclusion, :exclusion, :sort)
                ON CONFLICT DO NOTHING
            """
        )
        obj = asdict(search)
        obj["meta"] = json.dumps(obj["meta"])
        obj["inclusion"] = json.dumps(obj["inclusion"])
        obj["exclusion"] = json.dumps(obj["exclusion"])
        obj["sort"] = json.dumps(obj["sort"])
        con.execute(statement, obj)
        con.commit()
    return search


def insert_checkpoint(checkpoint: Checkpoint) -> Checkpoint:
    with db.connect() as con:
        statement = sqlalchemy.text(
            """
                INSERT INTO checkpoint (event_id) 
                VALUES(:event_id)
            """
        )
        con.execute(statement, asdict(checkpoint))
        con.commit()
    return checkpoint


def insert_targets_from_domains(
    domains: List[str], search_uid: int, actor_key: str, last_event_type: str
) -> None:
    """
    Takes in domains, inserts targets into a review stage, where they will
    try to be enriched on process event

    """
    existing_search_domains = unique_domains(search_uid=search_uid)[
        "domain"
    ].to_list()  # all I really want here is domains

    with db.connect() as con:
        for domain in domains:
            if "." not in domain:
                print(f"Skipping {domain} as not a valid domain")
                continue
            else:
                domain = helpers.clean_domain(domain) # removes http, https, www, etc
            
            if domain in existing_search_domains:
                print(f"Skipping {domain} as already a target")
                continue
            else:
                print(f"Adding {domain} as target")

            # should these be in same transaction?
            con.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO company (domain) 
                    VALUES(:domain)
                    ON CONFLICT DO NOTHING
                    """
                ),
                {"domain": domain},
            )

            con.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO event (search_uid, domain, actor_key, type) 
                    VALUES(:search_uid, :domain, :actor_key, :type)
                    """
                ),
                {
                    "search_uid": search_uid,
                    "actor_key": actor_key,
                    "domain": domain,
                    "type": last_event_type,
                },
            )
        # con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW target"))
        con.commit()


def insert_companies_as_targets(
    companies: List[Any], search_uid: int, actor_key: str
) -> None:
    """Takes Structured Companies (e.g. from source.find_similiar()) and inserts to Review phase"""
    existing_search_domains = unique_domains(search_uid=search_uid)["domain"].to_list()
    with db.connect() as con:
        for company in companies:
            if company.get("domain") is None:
                print(f"Missing domain: {company}. Skipping")
                continue

            # elif company["domain"] in targets["domain"]:
            elif company["domain"] in existing_search_domains:
                print(f"Skipping {company['domain']} as already a target")
                continue
            else:
                print(f"Adding {company['domain']} as target")

            con.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO company (domain, name, description) 
                    VALUES(:domain, :name, :description)
                    ON CONFLICT DO NOTHING
                    """
                ),
                {
                    "domain": company.get("domain"),
                    "name": company.get("name"),
                    "description": company.get("description"),
                },
            )

            con.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO event (search_uid, domain, actor_key, type) 
                    VALUES(:search_uid, :domain, :actor_key, :type)
                    """
                ),
                {
                    "search_uid": search_uid,
                    "actor_key": actor_key,
                    "domain": company.get("domain"),
                    "type": "create",
                },
            )

        # con.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW target"))
        con.commit()


### READS ###

def top_actor_per_search() -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
        SELECT 
            a.name,
            s.uid AS search_uid,
            COUNT(e.id) AS event_count
        FROM 
            event e
        INNER JOIN 
            actor a ON a.key = e.actor_key
        INNER JOIN 
            search s ON s.uid = e.search_uid
        WHERE
            a.type = 'research'
        GROUP BY 
            a.name, s.uid
        ORDER BY 
            event_count DESC;
        """
        result = conn.execute(
            sqlalchemy.text(statement))
        result = conn.execute(
            sqlalchemy.text(statement)
        )
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df


def search():
    with db.connect() as conn:
        statement = """
        SELECT 
            s.uid,
            s.label,
            (SELECT COUNT(*) 
            FROM event e
            WHERE 
            e.search_uid = s.uid AND e.created >= EXTRACT(EPOCH FROM (NOW() - INTERVAL '7 days')) and type = 'validate'
            ) AS validate_count
        FROM 
            search s;
        """
        result = conn.execute(
            sqlalchemy.text(statement)
        )
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        df['group'] = df['validate_count'].apply(lambda x: "Trending Searches" if x > 0 else "All Searches")
        df = df.sort_values(by=['group', 'validate_count','label'], ascending=[False, True, True])
        
        ## add top actor per search to the label
        ## do in the sql query instead sometime...
        df = df.merge(top_actor_per_search(),left_on='uid', right_on='search_uid', how='left')
        df = df.fillna("")
        # df['label'] = df['label'] + "      (" + df['name'] + ")"
    return df


def search_target_by_last_event_type(search_uid: int, last_event_type: str = None):
    statement = """
        SELECT 
            e.id, 
            e.search_uid, 
            e.domain, 
            e.data, 
            e.type AS last_event_type, 
            e.created AS updated,
            a.name AS updated_by,
            c.name as name,
            c.uid as dealcloud_id,
            c.description as description,
            c.meta as meta,
            (c.meta->>'employees') AS employees,
            (c.meta->>'ownership') AS ownership,
            (c.meta->>'linkedin') AS linkedin,
            (r.data->>'rating') AS rating
        FROM (
            SELECT 
                search_uid, 
                domain, 
                MAX(created) AS max_created
            FROM 
                event
            WHERE 
                type NOT IN ('comment','rating','generate','criteria')
                AND search_uid = :search_uid
            GROUP BY 
                domain, search_uid
        ) AS max_event
        JOIN event e ON e.domain = max_event.domain AND e.created = max_event.max_created AND e.search_uid = max_event.search_uid 
        JOIN company c ON c.domain = e.domain
        JOIN actor a ON a.key = e.actor_key
        LEFT JOIN (
            SELECT 
                search_uid,
                domain, 
                MAX(created) AS max_created
            FROM 
                event
            WHERE 
                type = 'rating'
            GROUP BY 
                domain, search_uid
        ) AS max_rating ON e.domain = max_rating.domain AND e.search_uid = max_rating.search_uid
        LEFT JOIN event r ON r.domain = max_rating.domain AND r.created = max_rating.max_created;
    """
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(statement),
            {"search_uid": search_uid, "last_event_type": last_event_type},
        )
        targets = pd.DataFrame(result.fetchall(), columns=result.keys())

    targets = targets[targets["last_event_type"] == last_event_type]
    comments = comment_by_domain(search_uid)
    targets = targets.merge(comments, on="domain", how="left")

    # handle sorting
    search = find_search_by_uid(search_uid)
    targets = targets.sort_values(
        by=search.sort.get("field", "domain"),
        ascending=search.sort.get("order") == "asc",
    )

    return targets


def search_target_export(search_uid: int) -> pd.DataFrame:
    """Returns all the targets not in rejected or created"""

    statement = """
        SELECT 
            e.id, 
            e.search_uid, 
            e.domain, 
            e.type AS last_event_type, 
            to_timestamp(e.created) AS updated,
            c.meta as meta,
            (r.data->>'rating') AS rating
        FROM (
            SELECT 
                search_uid, 
                domain, 
                MAX(created) AS max_created
            FROM 
                event
            WHERE 
                type NOT IN ('comment','rating','generate','criteria') 
                AND search_uid = :search_uid
            GROUP BY 
                domain, search_uid
        ) AS max_event
        JOIN event e ON e.domain = max_event.domain AND e.created = max_event.max_created AND e.search_uid = max_event.search_uid 
        JOIN company c ON c.domain = e.domain
        LEFT JOIN (
            SELECT 
                search_uid,
                domain, 
                MAX(created) AS max_created
            FROM 
                event
            WHERE 
                type = 'rating'
            GROUP BY 
                domain, search_uid
        ) AS max_rating ON e.domain = max_rating.domain AND e.search_uid = max_rating.search_uid
        LEFT JOIN event r ON r.domain = max_rating.domain AND r.created = max_rating.max_created;
    """
    with db.connect() as conn:
        result = conn.execute(
            sqlalchemy.text(statement),
            {"search_uid": search_uid},
        )
        targets = pd.DataFrame(result.fetchall(), columns=result.keys())
        if len(targets) > 0:
            targets = targets[~targets["last_event_type"].isin(["reject", "create"])]
            meta = pd.json_normalize(targets["meta"])
            targets = targets.merge(
                meta, left_on=["domain"], right_on=["domain"], how="left"
            )
            targets = targets.drop(columns=["meta"])
            targets = targets.sort_values(by=["last_event_type", "domain"])
    return targets


# def target(search_uid: int, last_event_type: str = None):
#     with db.connect() as conn:
#         if last_event_type is not None:
#             statement = "SELECT * FROM target WHERE search_uid = :search_uid AND last_event_type = :last_event_type"
#             result = conn.execute(
#                 sqlalchemy.text(statement),
#                 {"search_uid": search_uid, "last_event_type": last_event_type},
#             )

#         else:
#             statement = "SELECT * FROM target WHERE search_uid = :search_uid"
#             result = conn.execute(
#                 sqlalchemy.text(statement),
#                 {"search_uid": search_uid},
#             )

#         targets = pd.DataFrame(result.fetchall(), columns=result.keys())

#     comments = comment_by_domain(search_uid)
#     targets = targets.merge(comments, on="domain", how="left")

#     # handle sorting
#     search = find_search_by_uid(search_uid)
#     targets = targets.sort_values(
#         by=search.sort.get("field", "domain"),
#         ascending=search.sort.get("order") == "asc",
#     )

#     return targets


def target_count(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
            SELECT 
                e.type AS last_event_type,
                COUNT(e.type)
            FROM (
                SELECT 
                    search_uid, 
                    domain, 
                    MAX(created) AS max_created
                FROM 
                    event
                WHERE 
                    type NOT IN ('comment','rating','generate','criteria')
                    and search_uid = :search_uid
                GROUP BY 
                    domain, search_uid
            ) AS max_event
            JOIN event e ON e.domain = max_event.domain AND e.created = max_event.max_created AND e.search_uid = max_event.search_uid
            GROUP BY e.type;
        """
        result = conn.execute(
            sqlalchemy.text(statement),
            {"search_uid": search_uid},
        )
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def event(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM event
                WHERE search_uid = :search_uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"search_uid": search_uid})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def unique_domains(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT distinct(domain)
                FROM event
                WHERE search_uid = :search_uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"search_uid": search_uid})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def company() -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM company
            """
        result = conn.execute(sqlalchemy.text(statement))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def checkpoint(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM checkpoint
                JOIN event ON checkpoint.event_id = event.id
                WHERE search_uid = :search_uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"search_uid": search_uid})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def comment_by_domain(search_uid: int) -> pd.DataFrame:
    with db.connect() as conn:
        statement = """
                SELECT *, data->>'comment' AS comment
                FROM event e
                WHERE 
                    search_uid = :search_uid AND
                    type = 'comment'
            """
        result = conn.execute(
            sqlalchemy.text(statement),
            {"search_uid": search_uid},
        )
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df.groupby("domain").agg({"comment": lambda x: list(x)}).reset_index()


### FINDERS -> dataclass ###


def find_search_by_uid(search_uid: int) -> Search:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM search
                WHERE uid = :search_uid
            """
        result = conn.execute(sqlalchemy.text(statement), {"search_uid": search_uid})

    if result.rowcount == 0:
        return None
    else:
        obj = dict(zip(result.keys(), result.fetchone()))
        search =  from_dict(Search, obj)
        print(search.label)
        return search


def find_company_by_domain(domain: str) -> Company:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM company
                WHERE domain = :domain
            """
        result = conn.execute(sqlalchemy.text(statement), {"domain": domain})
        # obj = dict(zip(result.keys(), result.fetchone()))
    if result.rowcount == 0:
        return None
    else:
        obj = dict(zip(result.keys(), result.fetchone()))
        return from_dict(Company, obj)


def find_event_by_id(event_id: int) -> Event:
    with db.connect() as conn:
        statement = """
                SELECT *
                FROM event
                WHERE id = :event_id
            """
        result = conn.execute(sqlalchemy.text(statement), {"event_id": event_id})
        # obj = dict(zip(result.keys(), result.fetchone()))
    if result.rowcount == 0:
        return None
    else:
        obj = dict(zip(result.keys(), result.fetchone()))
        return from_dict(Event, obj)


### UPDATE ###


def update_company(company: Company) -> None:
    with db.connect() as conn:
        statement = """
            UPDATE company
            SET
                name = :name,
                description = :description,
                meta = :meta,
                updated = FLOOR(EXTRACT(EPOCH FROM NOW()))
            WHERE domain = :domain
            """

        conn.execute(
            sqlalchemy.text(statement),
            {
                "name": company.name,
                "description": company.description,
                "domain": company.domain,
                "meta": json.dumps(company.meta),
            },
        )
        # conn.execute(sqlalchemy.text("REFRESH MATERIALIZED VIEW target"))
        conn.commit()


def update_search(search: Search) -> None:
    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                UPDATE search
                SET
                    sort = :sort,
                    inclusion = :inclusion,
                    exclusion = :exclusion
                WHERE uid = :uid
                """
            ),
            {
                "sort": json.dumps(search.sort),
                "inclusion": json.dumps(search.inclusion),
                "exclusion": json.dumps(search.exclusion),
                "uid": search.uid,
            },
        )
        conn.commit()
