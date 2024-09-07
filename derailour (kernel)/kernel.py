import threading
import importlib

# Simplified process representation
class Process:
    def __init__(self, name, target, *args):
        self.name = name
        self.target = target
        self.args = args
        self.thread = threading.Thread(target=self.run)
        self.pause_event = threading.Event()  # Event to handle pausing
        self.pause_event.set()  # Initially set to allow execution

    def run(self):
        print(f"Process {self.name} started.")
        self.pause_event.wait()  # Wait if the pause event is cleared
        try:
            self.target(*self.args)  # Passing arguments to the target function
        except Exception as e:
            print(f"Error in process {self.name}: {e}")
        print(f"Process {self.name} finished.")

# Kernel managing processes
class Kernel:
    def __init__(self):
        self.processes = []

    def create_process(self, name, target, *args):
        # Check if target is a callable function or needs to be imported
        if isinstance(target, str):
            target = self.import_function(target)
        process = Process(name, target, *args)
        self.processes.append(process)
        print(f"Created process: {name}")

    def run(self):
        for process in self.processes:
            process.thread.start()
        for process in self.processes:
            process.thread.join()

    @staticmethod
    def import_function(fullname):
        """Dynamically import a function from a module using 'module_name.function_name' format."""
        module_name, func_name = fullname.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, func_name)

# Example functions in an interpreter module
def clss(file):
    print(f"Executing clss function with file: {file}")

def python(code):
    eval(code)

# Example usage of the Kernel with import function
#kernel = Kernel()

# Assuming you have a file named 'interpreter.py' with a function called 'clss'
#kernel.create_process("Process 1", "interpreter.clss", 'test.clss')

# Running a built-in Python function from the '__main__' module (current script)
#kernel.create_process("Process 2", "__main__.python", 'print("hello from imported function")')

# Run all processes
#kernel.run()
