import os


class Test:

    def __init__(self):
        self.age = 0
    def get_age(self):
        self.calculate_age()
        return self.age

    def calculate_age(self):
        pass

if __name__ == '__main__':
    class Test2(Test):
        def __init__(self):
            super(Test2, self).__init__()
        # override
        def calculate_age(self):
            self.age = 18

