import traceback
import sys
import threading
import time
from test_jasper import run_report

def trace():
    time.sleep(5)
    print("--- TRACE AFTER 5 SECONDS ---")
    for threadId, stack in sys._current_frames().items():
        print("Thread:", threadId)
        traceback.print_stack(stack)
    print("-----------------------------")
    sys.exit()

t = threading.Thread(target=trace)
t.daemon = True
t.start()

run_report()
