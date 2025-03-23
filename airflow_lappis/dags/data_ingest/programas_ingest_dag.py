import logging
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from postgres_helpers import get_postgres_conn
from cliente_ted import ClienteTed
from cliente_postgres import ClientPostgresDB


@dag(
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "owner": "Davi",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["ted_api", "programas"],
)
def api_programas_dag() -> None:

    @task
    def fetch_and_update_programas() -> None:
        logging.info("Starting api_programas_dag - Update Programs")
        api = ClienteTed()
        postgres_conn_str = get_postgres_conn()
        db = ClientPostgresDB(postgres_conn_str)
        id_programas = db.get_id_programas()

        total_processed = 0
        for id_programa in id_programas:
            programas_data = api.get_programa_by_id_programa(id_programa)
            if programas_data and len(programas_data) > 0:
                programa = programas_data[0]

                # Alter table to add any new columns needed
                db.alter_table(programa, "programas", schema="transfere_gov")

                # Insert/update the program data
                db.insert_data(
                    programas_data,
                    "programas",
                    primary_key=["id_programa"],
                    conflict_fields=["id_programa"],
                    schema="transfere_gov",
                )

                total_processed += 1
                if total_processed % 10 == 0:
                    logging.info(f"Processed {total_processed} programs")
            else:
                logging.warning(f"No program data found for id_programa: {id_programa}")

        logging.info(f"Completed processing {total_processed} programs")

    fetch_and_update_programas()


dag_instance = api_programas_dag()
