# thread_scenarios.py

# -----------------------------
# THREAD SECTION 1: Define Thread
# -----------------------------
def thread_section_1_define_thread(scenario_number=1):
    import threading
    import time
    import random

    print("===== SECTION 1: Define Thread =====")

    # ---------- Scenario 1 ----------

    def scenario_1():
        print("\n--- Scenario 1: Basic threading ---")
        def my_func(index):
            print(f"my_func called by thread N°{index}")

        threads = []
        for i in range(10):
            t = threading.Thread(target=my_func, args=(i,))
            threads.append(t)
            t.start()
            t.join()


    # ---------- Scenario 2 ----------

    def scenario_2():
        print("\n--- Scenario 2:Grouped execution (Threads 1-2, then 5-6-7, then 3-4 and rest)  ---")

        def my_func(index):
            time.sleep(random.uniform(0.1, 0.3))  # تأخیر تصادفی برای شبیه‌سازی کار واقعی
            print(f"my_func called by thread N°{index}")

        threads = [threading.Thread(target=my_func, args=(i,)) for i in range(10)]

        # گروه‌بندی نخ‌ها
        group_1 = [threads[0], threads[1]]  # نخ‌های ۱ و ۲
        group_2 = [threads[4], threads[5], threads[6]]  # نخ‌های ۵، ۶ و ۷
        group_3 = [threads[2], threads[3]] + threads[7:]  # نخ‌های ۳، ۴ و بقیه (۸، ۹)

        # اجرای گروه ۱
        print("Starting Group 1 (Threads 1, 2)")
        for t in group_1:
            t.start()
        for t in group_1:
            t.join()

        # اجرای گروه ۲
        print("Starting Group 2 (Threads 5, 6, 7)")
        for t in group_2:
            t.start()
        for t in group_2:
            t.join()

        # اجرای گروه ۳
        print("Starting Group 3 (Threads 3, 4, 8, 9, 10)")
        for t in group_3:
            t.start()
        for t in group_3:
            t.join()


    # ---------- Scenario 3 ----------

    def scenario_3():
        print("\n--- Scenario 3: Random delay to change order ---")

        def my_func(index):
            time.sleep(random.uniform(0.1, 0.5))
            print(f"my_func called by thread N°{index}")

        threads = []
        for i in range(10):
            t = threading.Thread(target=my_func, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")

# -----------------------------
# THREAD SECTION 2: Current Thread
# -----------------------------
def thread_section_2_current_thread(scenario_number=1):
    import threading
    import time
    import random

    print("===== SECTION 2: current_thread =====")

    def scenario_1():
        print("\n--- Scenario 1: استفاده ساده از چند تابع همزمان با threading ---")

        def function_A():
            thread_name = threading.current_thread().name
            print(f"function_A--> starting in {thread_name}")
            time.sleep(0.5)
            print(f"function_A--> exiting in {thread_name}")

        def function_B():
            thread_name = threading.current_thread().name
            print(f"function_B--> starting in {thread_name}")
            time.sleep(0.5)
            print(f"function_B--> exiting in {thread_name}")

        def function_C():
            thread_name = threading.current_thread().name
            print(f"function_C--> starting in {thread_name}")
            time.sleep(0.5)
            print(f"function_C--> exiting in {thread_name}")

        threads = []
        for func in [function_A, function_B, function_C]:
            t = threading.Thread(target=func)
            threads.append(t)
            t.start()
            t.join()


    def scenario_2():
        print("\n--- Scenario 2:  ---")

        def log_function(name):
            thread_name = threading.current_thread().name
            print(f"{name}--> starting in {thread_name}")
            time.sleep(0.3)
            print(f"{name}--> exiting in {thread_name}")

        threads = []
        for name in ['function_A', 'function_B', 'function_C']:
            t = threading.Thread(target=log_function, args=(name,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


    def scenario_3():
        print("\n--- Scenario 3:  ---")

        def function(name):
            thread_name = threading.current_thread().name
            time.sleep(random.uniform(0, 0.3))
            print(f"{name}--> starting in {thread_name}")
            time.sleep(random.uniform(0.1, 0.5))
            print(f"{name}--> exiting in {thread_name}")

        threads = []
        for name in ['function_A', 'function_B', 'function_C']:
            t = threading.Thread(target=function, args=(name,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")

# -----------------------------
# THREAD SECTION 3: Subclassing Thread
# -----------------------------
def thread_section_3_subclass_thread(scenario_number=1):
    import threading
    import os
    import time
    import random
    print("===== SECTION 3: Defining a thread subclass =====")

    # ---------- Scenario 1 ----------
    def scenario_1():
        print("\n--- Scenario 1:  ---")

        class MyThread(threading.Thread):
            def __init__(self, number):
                threading.Thread.__init__(self)
                self.number = number

            def run(self):
                print(f"---> Thread#{self.number} running, belonging to process ID {os.getpid()}")
                time.sleep(random.uniform(0.5, 2.0))
                print(f"---> Thread#{self.number} over")

        start_time = time.time()

        for i in range(1, 10):
            t = MyThread(i)
            t.start()
            t.join()

        print("End ---", time.time() - start_time, "seconds ---")

    # ---------- Scenario 2 ----------
    def scenario_2():
        print("\n--- Scenario 2:  ---")

        class MyThread(threading.Thread):
            def __init__(self, number):
                threading.Thread.__init__(self)
                self.number = number

            def run(self):
                print(f"---> Thread#{self.number} running, belonging to process ID {os.getpid()}")
                time.sleep(random.uniform(0.5, 2.0))
                print(f"---> Thread#{self.number} over")

        start_time = time.time()

        threads = []
        for i in range(1, 10):
            t = MyThread(i)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print("End ---", time.time() - start_time, "seconds ---")
    # ---------- Scenario 3 ----------
    def scenario_3():
        print("\n--- Scenario 3:  ---")

        class MyThread(threading.Thread):
            def __init__(self, number):
                threading.Thread.__init__(self)
                self.number = number

            def run(self):
                if self.number % 2 == 0:
                    print(f"Thread#{self.number} is about to start...")

                    time.sleep(1)  # نخ‌های زوج با تأخیر
                print(f"---> Thread#{self.number} running, belonging to process ID {os.getpid()}")
                time.sleep(0.5)
                print(f"---> Thread#{self.number} over")

        start_time = time.time()
        threads = []

        for i in range(10):
            t = MyThread(i)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print("All threads completed.")
        print("End ---", time.time() - start_time, "seconds ---")



    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")


# -----------------------------
# THREAD SECTION 4: Lock Synchronization
# -----------------------------
def thread_section_4_lock_sync(scenario_number=1):
    import threading
    import time
    import os

    print("===== SECTION 4: Thread synchronization with a lock =====")

    # ---------- Scenario 1 ----------
    def scenario_1():
        print("\n--- Scenario 1:  ---")

        lock = threading.Lock()

        def print_thread(number):
            # گرفتن قفل قبل از ورود به بخش حساس
            lock.acquire()
            print(f"Thread#{number} running, belonging to process ID {os.getpid()}")
            time.sleep(1)  # شبیه‌سازی انجام کار
            print(f"Thread#{number} over")
            # آزاد کردن قفل
            lock.release()

        # ایجاد و شروع نخ‌ها
        threads = []
        for i in range(1, 10):
            t = threading.Thread(target=print_thread, args=(i,))
            threads.append(t)
            t.start()

        # منتظر ماندن برای پایان همه نخ‌ها
        for t in threads:
            t.join()

        print("End")



    # ---------- Scenario 2 ----------
    def scenario_2():
        print("\n--- Scenario 2:  ---")

        def print_thread(number):
            print(f"Thread#{number} running, belonging to process ID {os.getpid()}")
            time.sleep(1)  # شبیه‌سازی انجام کار
            print(f"Thread#{number} over")

        # ایجاد و شروع نخ‌ها
        threads = []
        for i in range(1, 10):
            t = threading.Thread(target=print_thread, args=(i,))
            threads.append(t)
            t.start()

        # منتظر ماندن برای پایان همه نخ‌ها
        for t in threads:
            t.join()

        print("End")

        pass

    # ---------- Scenario 3 ----------
    def scenario_3():
        print("\n--- Scenario 3:  ---")

        lock = threading.Lock()

        def print_thread(number):
            # گرفتن قفل فقط برای بخش شروع
            lock.acquire()
            print(f"Thread#{number} running, belonging to process ID {os.getpid()}")
            lock.release()
            time.sleep(1)  # شبیه‌سازی انجام کار
            print(f"Thread#{number} over")


        # ایجاد و شروع نخ‌ها
        threads = []
        for i in range(1, 10):
            t = threading.Thread(target=print_thread, args=(i,))
            threads.append(t)
            t.start()

        # منتظر ماندن برای پایان همه نخ‌ها
        for t in threads:
            t.join()

        print("End")



    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")

# -----------------------------
# THREAD SECTION 5: RLock Synchronization
# -----------------------------
def thread_section_5_rlock_sync(scenario_number=1):
    import threading
    import time

    print("===== SECTION 5: Thread synchronization with RLock =====")

    # ---------- Scenario 1 ----------
    def scenario_1():
        print("\n--- Scenario 1: Using shared_data and RLock ---")

        rlock = threading.RLock()

        # دیکشنری اشتراکی برای نگه‌داری داده‌ها
        shared_data = {
            "items_to_add": 16,
            "items_to_remove": 1
        }

        def modify_items(thread_id):
            with rlock:
                print(f"[Thread-{thread_id}] N° {shared_data['items_to_add']} items to ADD")
                time.sleep(0.5)
                if shared_data["items_to_add"] > 0:
                    shared_data["items_to_add"] -= 1
                    print(f"[Thread-{thread_id}] ADDED one item --> {shared_data['items_to_add']} left to ADD")

                time.sleep(0.5)
                print(f"[Thread-{thread_id}] N° {shared_data['items_to_remove']} items to REMOVE")
                if shared_data["items_to_remove"] > 0:
                    shared_data["items_to_remove"] -= 1
                    print(f"[Thread-{thread_id}] REMOVED one item --> {shared_data['items_to_remove']} left to REMOVE")

        # ایجاد و اجرای نخ‌ها
        threads = []
        for i in range(5):
            t = threading.Thread(target=modify_items, args=(i + 1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("End")


    # ---------- Scenario 2 ----------
    def scenario_2():
        print("\n--- Scenario 2: Nested RLock ---")

        rlock = threading.RLock()

        # shared_data به جای global
        shared_data = {
            "items_to_add": 16,
            "items_to_remove": 1
        }

        def modify_items(thread_id):
            with rlock:
                print(f"[Thread-{thread_id}] N° {shared_data['items_to_add']} items to ADD")
                time.sleep(0.5)
                if shared_data["items_to_add"] > 0:
                    shared_data["items_to_add"] -= 1
                    print(f"[Thread-{thread_id}] ADDED one item --> {shared_data['items_to_add']} left to ADD")

                # Re-entering lock (همون نخ دوباره قفل رو می‌گیره)
                with rlock:
                    time.sleep(0.5)
                    print(f"[Thread-{thread_id}] N° {shared_data['items_to_remove']} items to REMOVE")
                    if shared_data["items_to_remove"] > 0:
                        shared_data["items_to_remove"] -= 1
                        print(
                            f"[Thread-{thread_id}] REMOVED one item --> {shared_data['items_to_remove']} left to REMOVE")

        threads = []
        for i in range(5):
            t = threading.Thread(target=modify_items, args=(i + 1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("End")


    # ---------- Scenario 3 ----------
    def scenario_3():
        print("\n--- Scenario 3: Nested functions using RLock ---")

        rlock = threading.RLock()

        shared_data = {
            "items_to_add": 16,
            "items_to_remove": 1
        }

        def modify_items(thread_id):
            def add_item():
                with rlock:
                    print(f"[Thread {thread_id}] N° {shared_data['items_to_add']} items to ADD")
                    time.sleep(0.5)
                    if shared_data["items_to_add"] > 0:
                        shared_data["items_to_add"] -= 1
                        print(
                            f"[Thread {thread_id}] ADDED one item --> {shared_data['items_to_add']} items left to ADD")

            def remove_item():
                with rlock:
                    print(f"[Thread {thread_id}] N° {shared_data['items_to_remove']} items to REMOVE")
                    time.sleep(0.5)
                    if shared_data["items_to_remove"] > 0:
                        shared_data["items_to_remove"] -= 1
                        print(
                            f"[Thread {thread_id}] REMOVED one item --> {shared_data['items_to_remove']} items left to REMOVE")

            with rlock:
                add_item()
                remove_item()

        threads = []
        for i in range(5):
            t = threading.Thread(target=modify_items, args=(i + 1,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("End")

    # اجرای سناریوی انتخاب‌شده
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")

# -----------------------------
# THREAD SECTION 6: Semaphore Synchronization
# -----------------------------
def thread_section_6_semaphore_sync(scenario_number=1):
    import threading
    import time
    #import logging
    print("===== SECTION 6: Thread synchronization with semaphores =====")

    # ---------- Scenario 1 ----------
    def scenario_1():
        print("\n--- Scenario 1:  ---")
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

        semaphore = threading.Semaphore(0)
        items = []

        def producer(item_number):
            time.sleep(1)  # تولید آیتم با کمی تأخیر
            items.append(item_number)
            print(f'Producer notify: item number {item_number}')     #logging.info(...) رو برداشتم بجاش  print گذاشتم تا در مرورگر خروجی نمایش داده بشه
            semaphore.release()

        def consumer():
            time.sleep(3)  # مصرف‌کننده‌ها با تأخیر وارد می‌شن
            print('Consumer is waiting')
            time.sleep(1.5)  # اضافه‌شده برای اطمینان از رسیدن producer
            semaphore.acquire()
            item = items.pop(0)
            print(f'Consumer notify: item number {item}')

        # تعریف نخ‌ها
        t1 = threading.Thread(target=producer, args=(101,), name="Thread-1")
        t2 = threading.Thread(target=producer, args=(202,), name="Thread-2")
        t3 = threading.Thread(target=consumer, name="Thread-3")
        t4 = threading.Thread(target=consumer, name="Thread-4")

        # شروع نخ‌ها
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # منتظر ماندن برای پایان همه نخ‌ها
        t1.join()
        t2.join()
        t3.join()
        t4.join()


    # ---------- Scenario 2 ----------
    def scenario_2():
        print("\n--- Scenario 2:  ---")
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

        items = []
        items_count = 5
        semaphore = threading.Semaphore(0)

        def producer(item_number):
            time.sleep(1)
            items.append(item_number)
            print(f'Producer notify: item number {item_number}')
            semaphore.release()

        def consumer():
            for _ in range(items_count):
                print('Consumer is waiting')
                time.sleep(1.5)  # اضافه‌شده برای اطمینان از رسیدن producer
                semaphore.acquire()
                item = items.pop(0)
                print(f'Consumer notify: item number {item}')

        # ساخت نخ‌های تولیدکننده
        producer_threads = []
        for i in range(items_count):
            t = threading.Thread(target=producer, args=(i + 1,), name=f"Producer-{i + 1}")
            producer_threads.append(t)
            t.start()

        consumer_thread = threading.Thread(target=consumer, name="Consumer-Thread")
        consumer_thread.start()

        for t in producer_threads:
            t.join()

        consumer_thread.join()



    # ---------- Scenario 3 ----------
    def scenario_3():
        print("\n--- Scenario 3:  ---")
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

        semaphore = threading.Semaphore(0)
        items = []

        def producer(item_number):
            time.sleep(1)
            items.append(item_number)
            print(f'Producer notify: item number {item_number}')
            semaphore.release()

        def consumer():
            print('Consumer is waiting')
            time.sleep(1.5)  # اضافه‌شده برای اطمینان از رسیدن producer
            semaphore.acquire()
            item = items.pop(0)
            print(f'Consumer notify: item number {item}')

        t1 = threading.Thread(target=consumer, name="Thread-1")
        t2 = threading.Thread(target=consumer, name="Thread-2")
        t3 = threading.Thread(target=producer, args=(999,), name="Thread-3")
        t4 = threading.Thread(target=producer, args=(999,), name="Thread-4")

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")

# -----------------------------
# THREAD SECTION 7: Barrier Synchronization
# -----------------------------
def thread_section_7_barrier_sync(scenario_number=1):
    import threading
    import time

    print("===== SECTION 7: Thread synchronization with a barrier =====")

    # ---------- Scenario 1 ----------
    def scenario_1():
        print("\n--- Scenario 1:  ---")

        def reach_barrier(name, barrier):
            print(f"{name} reached the barrier at: {time.ctime()}")
            barrier.wait()

        def race():
            barrier = threading.Barrier(3)
            threads = []

            names = ["Dewey", "Huey", "Louie"]

            for name in names:
                thread = threading.Thread(target=reach_barrier, args=(name, barrier))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print("Race over!")

        print("START RACE!!!!")
        race()


    def scenario_2():
        print("\n--- Scenario 2:  ---")

        def reach_barrier(name, barrier, delay=0):
            time.sleep(delay)
            print(f"{name} reached the barrier at: {time.ctime()}")
            barrier.wait()

        def race():
            barrier = threading.Barrier(3)
            threads = []

            names = ["Dewey", "Huey", "Louie"]

            # Louie will be delayed
            threads.append(threading.Thread(target=reach_barrier, args=("Dewey", barrier)))
            threads.append(threading.Thread(target=reach_barrier, args=("Huey", barrier)))
            threads.append(threading.Thread(target=reach_barrier, args=("Louie", barrier, 2)))  # با 2 ثانیه تاخیر

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            print("Race over!")

        race()

    # ---------- Scenario 3 ----------
    #(با دو مرحله Barrier)
    def scenario_3():
        import threading
        import time
        import random

        print("\n--- Scenario 3: Multi-step race with multiple barriers ---")

        def runner(name, barrier1, barrier2):
            print(f"{name} started step 1")
            time.sleep(random.uniform(0.5, 1.0))
            print(f"{name} reached barrier 1 at: {time.ctime()}")
            barrier1.wait()

            print(f"{name} started step 2")
            time.sleep(random.uniform(0.5, 1.0))
            print(f"{name} reached barrier 2 at: {time.ctime()}")
            barrier2.wait()

            print(f"{name} finished the race!")

        # هر مرحله یه Barrier خودش داره
        barrier1 = threading.Barrier(3)
        barrier2 = threading.Barrier(3)

        names = ["Dewey", "Huey", "Louie"]
        threads = []

        for name in names:
            t = threading.Thread(target=runner, args=(name, barrier1, barrier2))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("Multi-step race over!")

    # اجرای سناریوها
    if scenario_number == 1:
        scenario_1()
    elif scenario_number == 2:
        scenario_2()
    elif scenario_number == 3:
        scenario_3()
    else:
        print("Invalid scenario number!")
