import win32com.client, sys
from utils import logger as log

class Client:
    _self = None
    _initialized_com = False
    
    # Singleton
    def __new__(cls, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
            # Initialize instance-specific flag; __init__ will use this
            # to ensure it only fully initializes once.
            cls._self._instance_initialized = False
        return cls._self 
    
    def __init__(self, dispatch="PowerPoint.Application", visible=True):
        # If this specific instance has already been initialized, do nothing
        if self._instance_initialized:
            if self.dispatch != dispatch or self.visible != visible:
                log.warn(
                    f"Client already initialized with dispatch='{self.dispatch}', visible={self.visible}. "
                    f"Ignoring new parameters dispatch='{dispatch}', visible={visible}."
                )
            return

        
        self.dispatch = dispatch
        self.visible = visible
        self.powerpoint_app = None

        try:
            log.info(f"Creating COM client for '{self.dispatch}', Visible: {self.visible}")
            self.powerpoint_app = win32com.client.Dispatch(self.dispatch)
            self.powerpoint_app.Visible = self.visible
            self._instance_initialized = True # Mark instance as initialized

        except Exception as error:
            log.error(f"Failed to initialize COM client for '{self.dispatch}'", error)
            self.powerpoint_app = None
            sys.exit(1)
        
    # Get PowerPoint instance
    def get_app(self):
        if not self._instance_initialized:
            log.warn(f"COM client for '{self.dispatch}' was not successfully initialized. get_app() will return None.")
            return None
        return self.powerpoint_app

    # Delete PowerPoint instance
    def quit(self):
        if self.powerpoint_app:
            try:
                log.info(f"Attempting to quit COM client for '{self.dispatch}'...")
                self.powerpoint_app.Quit()
                log.info(f"Successfully quit COM client for '{self.dispatch}'.")
            except Exception as error:
                log.error(f"Failed to quit COM client for '{self.dispatch}'", error)

            finally:
                self.powerpoint_app = None
        else:
            log.warn(f"COM client for '{self.dispatch}' already quit or application instance not found.")

