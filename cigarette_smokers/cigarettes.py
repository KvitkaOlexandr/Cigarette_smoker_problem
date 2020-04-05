import threading
import random
import time


def generate_random_items():
    item1 = random.randint(1, 100)
    item2 = random.randint(1, 100)
    item1 %= 3
    item2 %= 3
    if item1 == item2:
        item2 += 1
        item2 %= 3
    item_list = [item1, item2]
    return item_list


class CigaretteSmoker:
    def __init__(self, rounds):
        self.condMutex = threading.Condition()
        self.barmanSleep = threading.Semaphore(0)
        self.rounds = rounds
        self.ingredients = ['TOBACCO', 'PAPER', 'MATCHES']
        self.availableItems = [False, False, False]
        self.smokerThreads = []
        self.terminate = False
        self.smokerThreads.append(threading.Thread(target=self.smoker_routine, name='Dude_with_tobacco', args=(1, 2)))
        self.smokerThreads.append(threading.Thread(target=self.smoker_routine, name='Dude_with_paper', args=(0, 2)))
        self.smokerThreads.append(threading.Thread(target=self.smoker_routine, name='Dude_with_matches', args=(0, 1)))
        for smokers in self.smokerThreads:
            smokers.start()
        self.barmanThread = threading.Thread(target=self.barman_routine)
        self.barmanThread.start()

    def barman_routine(self):
        for i in range(self.rounds):
            random_items = generate_random_items()
            self.condMutex.acquire()
            print('Barman produced: {0} and {1}'.format(self.ingredients[random_items[0]], self.ingredients[random_items[1]]))
            self.availableItems[random_items[0]] = True
            self.availableItems[random_items[1]] = True
            self.condMutex.notify_all()
            self.condMutex.release()
            self.barmanSleep.acquire()

    def smoker_routine(self, needed_item1, needed_item2):
        name = threading.currentThread().getName()
        while True:
            self.condMutex.acquire()
            while not self.availableItems[needed_item1] or not self.availableItems[needed_item2]:
                self.condMutex.wait()
            self.condMutex.release()
            if self.terminate:
                break
            self.availableItems[needed_item1] = False
            self.availableItems[needed_item2] = False
            print('{0} started smoking.'.format(name))
            self.start_smoking()
            print('{0} ended smoking.'.format(name))
            self.barmanSleep.release()

    def start_smoking(self):
        random_time = random.randint(1, 100)
        random_time %= 5
        time.sleep(random_time + 1)

    def wait_for_completion(self):
        self.barmanThread.join()
        self.condMutex.acquire()
        self.terminate = True
        self.availableItems = [True, True, True]
        self.condMutex.notify_all()
        self.condMutex.release()


if __name__ == "__main__":
    obj = CigaretteSmoker(3)
    obj.wait_for_completion()
