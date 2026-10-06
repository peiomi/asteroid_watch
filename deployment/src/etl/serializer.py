from dataclasses import asdict, is_dataclass


# i really do just be throwing everything in a class bc i can
class Serializer:

    @staticmethod
    def serialize_records(records):
        rows = []

        for record in records:

            # normal etl path
            if is_dataclass(record):
                row = asdict(record)
            # recovery path
            elif isinstance(record, dict):
                row = record.copy()
            else:
                raise TypeError(f"Unsupported record type: {type(record)}")

            if "processed_at" in row and hasattr(row["processed_at"], "isoformat"):
                row["processed_at"] = row["processed_at"].isoformat()

            rows.append(row)

        return rows
