from datetime import datetime

from lib.pg import PgConnect


class StgRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def order_events_insert(self,
                            object_id: int,
                            object_type: str,
                            sent_dttm: datetime,
                            payload: str
                            ) -> None:
        print("IN 1")
        with self._db.connection() as conn:
            print("IN 2")
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO stg.order_events (object_id, object_type, sent_dttm, payload) VALUES (%s, %s, %s, %s) ON CONFLICT (object_id) DO UPDATE SET object_type=EXCLUDED.object_type, sent_dttm=EXCLUDED.sent_dttm, payload=EXCLUDED.payload;",
                    (object_id, object_type, sent_dttm, payload)
                )
