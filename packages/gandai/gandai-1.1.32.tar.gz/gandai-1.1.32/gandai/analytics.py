import pandas as pd
import plotly.express as px
from gandai.db import connect_with_connector
import sqlalchemy

db = connect_with_connector()


def draw_validation_per_day() -> pd.DataFrame:
    statement = """
    SELECT e.*, to_timestamp(e.created) as dt, a.name, s.label
    FROM event e
    JOIN actor a on e.actor_key = a.key
    JOIN search s on e.search_uid = s.uid
    WHERE to_timestamp(e.created) > now() - interval '14 day'
    and a.key not in ('grata','dealcloud')
    and e.type in ('validate')
    ORDER BY created
    """
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text(statement))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    df["date"] = df["dt"].dt.strftime("%Y-%m-%d")

    validations = df.groupby(["name", "date"]).size().reset_index(
        name="count"
    ).sort_values(by=["date"]).reset_index(drop=True)

    fig = px.bar(validations, x='date', y='count', color='name', barmode='group', title='Validations per day by actor')
    return fig