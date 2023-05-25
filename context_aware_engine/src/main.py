import time

import schedule

from repository import execute_context_aware_rules

if __name__ == "__main__":
    print("Starting up code...")

    execute_context_aware_rules()
    schedule.every(1).minute.do(execute_context_aware_rules)

    while True:
        schedule.run_pending()
        time.sleep(1)