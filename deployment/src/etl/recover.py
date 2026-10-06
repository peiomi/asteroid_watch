import logging

from src.etl.recovery_service import RecoveryService


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    recovery = RecoveryService()
    recovery.replay_failed_batches()


if __name__ == "__main__":
    main()
