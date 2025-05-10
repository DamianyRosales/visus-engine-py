import win32com.client, sys
from utils import logger as log

class Client:
    _self = None
    
    # Singleton
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self 
    
    def __init__(self, dispatch="PowerPoint.Application", visible=True):
        self.dispatch = dispatch
        self.visible = visible
        self.powerpoint_app = None

        try:
            if self.powerpoint_app  is None:
                log.info(f"Creating COM client")
                self.powerpoint_app = win32com.client.Dispatch(self.dispatch)
                self.powerpoint_app.Visible = self.visible
                return

        except Exception as error:
            log.error(f"Failed to initialize COM client", error)
            self.powerpoint_app  = None
            sys.exit(1)
        
    # Get PowerPoint instance
    def get_app(self):
        return self.powerpoint_app
    
    # Delete PowerPoint instance
    def quit(self):
        if self.powerpoint_app:
            try:
                self.powerpoint_app.Quit()
            except Exception as e:
                log.error(f"Failed to quit COM client: {e}")
            finally:
                self.powerpoint_app = None
        else:
            log.warn("PowerPoint application object is not initialized, nothing to quit.")

