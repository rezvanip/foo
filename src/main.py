"""Main application entry point."""
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from screens import LoginRegisterScreen, MainScreen


class JobPortalApp(MDApp):
    """Main KivyMD application managing screen navigation and theming."""
    
    def build(self):
        """Initialize screen manager with login and main screens."""
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
