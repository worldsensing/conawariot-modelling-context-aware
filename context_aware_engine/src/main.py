import time

import schedule

from repository import get_context_aware_rules

if __name__ == "__main__":
    print("Starting up code...")

    get_context_aware_rules()

    schedule.every(15).seconds.do(get_context_aware_rules)

    while True:
        schedule.run_pending()
        time.sleep(1)
