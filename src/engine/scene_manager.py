class SceneManager:
    def __init__(self, engine):
        self.engine = engine
        self.current = None
    
    def set_scene(self, name):
        self.current = name
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
