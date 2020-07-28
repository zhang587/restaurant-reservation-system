import time
import datetime


class Restaurant:

    def __init__(self, num_tables, table_size):
        self.num_tables = num_tables
        self.table_size = table_size
        self.table_flags = ["reservable"] * self.num_tables
        self.ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.reservation_record = {}

    def reserve(self, num_customers) -> bool:
        count_table = 0

        # if there are reservable tables available
        for i in self.table_flags:
            if i == "reservable":
                count_table += 1

        if count_table == 0:
            return False
        elif count_table * self.table_size < num_customers:  # the number of people exceeded expected capacity
            return False
        else:
            num_reserved = int(num_customers / self.table_size) + 1 if num_customers % self.table_size != 0 \
                else num_customers / self.table_size
            count = 0
            for i in range(len(self.table_flags)):
                if self.table_flags[i] == 'reservable':
                    self.table_flags[i] = 'non-reservable'
                    count += 1
                if count == num_reserved:
                    self.reservation_record[self.ts] = ["non-reservable"]*count
                    break
            return True


if __name__ == "__main__":
    restaurant = Restaurant(3, 4)
    print(restaurant.reserve(4))
    print(restaurant.table_flags)
    print(restaurant.reservation_record)
    print(restaurant.reserve(4))
    print(restaurant.table_flags)
    print(restaurant.reservation_record)
    print(restaurant.reserve(4))
    print(restaurant.table_flags)
    print(restaurant.reservation_record)
