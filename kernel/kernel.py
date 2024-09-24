import interpreter
import concurrent.futures
import pygame
from pynput import keyboard

class clk:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(clk, cls).__new__(cls)
            cls._instance.mem = {}
            cls._instance.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            cls._instance.pressed_keys = []  # Array to store all characters pressed
            cls._instance.listener = keyboard.Listener(on_press=cls._instance.on_press)
            cls._instance.listener.start()  # Start the key listener in the background
            
            # Pygame initialization
            pygame.init()
            cls._instance.screen = pygame.display.set_mode((800, 600))
            cls._instance.font = pygame.font.SysFont('Arial', 24)
            cls._instance.clock = pygame.time.Clock()
        return cls._instance

    def on_press(self, key):
        """Callback function to handle key press event"""
        try:
            # Convert the key to its char form, if possible, and append to the pressed_keys array
            self.pressed_keys.append(key.char)
        except AttributeError:
            # For special keys (like space, enter), handle them differently and append the string
            self.pressed_keys.append(str(key))

        # Update the memory with the array of pressed keys
        self.write('pressed_keys', self.pressed_keys)

    def write(self, key, val):
        self.mem[key] = val

    def get(self, key):
        if not key in self.mem:
            return ""
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

    def graphics(self):
        if "graphics" in self.mem:
            g = self.mem["graphics"]
            
            # Ensure 'graphics' is stored as a list
            if isinstance(g, str):
                try:
                    # Attempt to convert the string to a list
                    g = eval(g)
                except:
                    print("Failed to convert graphics to a list.")
                    return
            
            # Clear the screen
            self.screen.fill((255, 255, 255))  # Fill with white background
            size = 20

            while g:
                if g[0] == 'line':
                    g.pop(0)
                    pygame.draw.line(self.screen, (0, 0, 0), (g[0], g[1]), (g[2], g[3]), 5)
                    g = g[4:]
                elif g[0] == 'txt':
                    g.pop(0)
                    text_surface = self.font.render(g[0], True, (0, 0, 0))
                    self.screen.blit(text_surface, (g[1], g[2]))
                    g.pop(0)
                elif g[0] == 'color':
                    g.pop(0)
                    color = g[0]
                    g.pop(0)
                elif g[0] == 'size':
                    g.pop(0)
                    size = g[0]
                    self.font = pygame.font.SysFont('Arial', size)
                    g.pop(0)
                elif g[0] == 'clr':
                    g.pop(0)
                    self.screen.fill((255, 255, 255))  # Clear the screen to white
                else:
                    g.pop(0)

            # Update the display
            pygame.display.flip()

        # Call this to update the screen and maintain the frame rate
        def update_screen(self):
            self.clock.tick(60)  # Limit to 60 frames per second
