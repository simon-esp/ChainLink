import interpreter
import concurrent.futures

class Memory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
            cls._instance.mem = {}
            cls._instance.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        return cls._instance

    def write(self, key, val):
        self.mem[key] = val

    def get(self, key):
        return self.mem.get(key, None)

    def getraw(self):
        return self.mem

    def clss(self, script):
        def run_script():
            interpreter.clss(script)
        future = self.executor.submit(run_script)
        return future
    
    def clss_blocking(self, script):
        interpreter.clss(script)
