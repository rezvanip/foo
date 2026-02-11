from kivy.uix.screenmanager import Screen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout

from .offers_screen import OffersScreen
from .applications_screen import ApplicationsScreen
from .profile_screen import ProfileScreen


class MainScreen(Screen):
    """Main screen with bottom navigation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the main UI with bottom navigation."""
        layout = MDBoxLayout(orientation='vertical')
        
        # Bottom Navigation
        bottom_nav = MDBottomNavigation()
        
        # Offers Tab
        offers_item = MDBottomNavigationItem(
            name='offers',
            text='Offers',
            icon='briefcase'
        )
        self.offers_screen = OffersScreen(name='offers_content')
        offers_item.bind(on_tab_press=self.offers_screen.on_press)
        offers_item.add_widget(self.offers_screen)
        
        # Applications Tab
        applications_item = MDBottomNavigationItem(
            name='applications',
            text='Applications',
            icon='file-document'
        )
        self.applications_screen = ApplicationsScreen(name='applications_content')
        applications_item.bind(on_tab_press=self.applications_screen.on_press)
        applications_item.add_widget(self.applications_screen)
        
        # Profile Tab
        profile_item = MDBottomNavigationItem(
            name='profile',
            text='Profile',
            icon='account'
        )
        self.profile_screen = ProfileScreen(name='profile_content')
        profile_item.bind(on_tab_press=self.profile_screen.on_press)
        profile_item.add_widget(self.profile_screen)
        
        bottom_nav.add_widget(offers_item)
        bottom_nav.add_widget(applications_item)
        bottom_nav.add_widget(profile_item)
        
        layout.add_widget(bottom_nav)
        self.add_widget(layout)
    
    def on_enter(self):
        """Called when screen is entered."""
        # TODO: Figure out How to handle the current user id
        self.offers_screen.user_id = self.manager.current_user_id
        self.applications_screen.user_id = self.manager.current_user_id
        self.profile_screen.user_id = self.manager.current_user_id

        self.offers_screen.load_offers()
        self.applications_screen.load_applications()
        self.profile_screen.load_profile()
