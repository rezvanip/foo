from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from screens import LoginRegisterScreen, MainScreen


class JobPortalApp(MDApp):
    """Main application class."""
    
    def build(self):
        """Build the app."""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # Create screen manager
        sm = ScreenManager(transition=SlideTransition())
        sm.current_user_id = None  # Store logged in user ID
        
        # Add screens
        sm.add_widget(LoginRegisterScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        
        return sm


if __name__ == '__main__':
    JobPortalApp().run()
