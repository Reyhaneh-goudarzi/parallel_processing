# test_runner.py

from multiprocessing import Queue as mpQueue , Manager
from thread_scenarios import (
    thread_section_1_define_thread,
    thread_section_2_current_thread,
    thread_section_3_subclass_thread,
    thread_section_4_lock_sync,
    thread_section_5_rlock_sync,
    thread_section_6_semaphore_sync,
    thread_section_7_barrier_sync,
)

from process_scenarios import (
    process_section_1_spawn_process,
    process_section_2_name_process,
    process_section_3_background_process,
    process_section_4_kill_process,
    process_section_5_subclass_process,
    process_section_6_queue_exchange,
    process_section_7_sync_processes,
    process_section_8_process_pool,
)

def run_test(section_number: int, scenario_number: int, mode: str = "thread", log_queue=None):
    if mode == "thread":
        if section_number == 1:
            thread_section_1_define_thread(scenario_number)
        elif section_number == 2:
            thread_section_2_current_thread(scenario_number)
        elif section_number == 3:
            thread_section_3_subclass_thread(scenario_number)
        elif section_number == 4:
            thread_section_4_lock_sync(scenario_number)
        elif section_number == 5:
            thread_section_5_rlock_sync(scenario_number)
        elif section_number == 6:
            thread_section_6_semaphore_sync(scenario_number)
        elif section_number == 7:
            thread_section_7_barrier_sync(scenario_number)
        else:
            print("Invalid section number!")

    elif mode == "process":
        # تغییر: استفاده شرطی از Manager().Queue() فقط برای بخش ۸
        if section_number == 8:
            log_queue = log_queue or Manager().Queue()  # برای Pool در بخش ۸
        else:
            log_queue = log_queue or mpQueue()  # برای Process در بخش‌های ۱ تا ۷
        if section_number == 1:
            process_section_1_spawn_process(scenario_number, log_queue=log_queue)
        elif section_number == 2:
            process_section_2_name_process(scenario_number, log_queue=log_queue)
        elif section_number == 3:
            process_section_3_background_process(scenario_number, log_queue=log_queue)
        elif section_number == 4:
            process_section_4_kill_process(scenario_number, log_queue=log_queue)
        elif section_number == 5:
            process_section_5_subclass_process(scenario_number, log_queue=log_queue)
        elif section_number == 6:
            process_section_6_queue_exchange(scenario_number, log_queue=log_queue)
        elif section_number == 7:
            process_section_7_sync_processes(scenario_number, log_queue=log_queue)
        elif section_number == 8:
            process_section_8_process_pool(scenario_number, log_queue=log_queue)
        else:
            print("Invalid process section number!")

            # برای دیباگ: چاپ لاگ‌ها از log_queue
        while not log_queue.empty():
            print(log_queue.get())

    else:
        print("Invalid mode! Use 'thread' or 'process'.")


#  تست هر بخش
if __name__ == "__main__":

    section = 7
    scenario = 3
    mode = "thread" # "thread" / "process"

    run_test(section, scenario, mode)