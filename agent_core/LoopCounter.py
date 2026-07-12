class LoopCounter:
    def __init__(self, max_loops=15):
        self.count = 0
        self.max_loops = max_loops

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count

    def reset(self):
        self.count = 0
    
    def has_exceeded_limit(self):
        return self.count > self.max_loops

