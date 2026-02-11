from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton, MDFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar

import hashlib

from components import Toast

from database import get_db
from models import User
from repositories import UserRepository


class Tab(MDFloatLayout, MDTabsBase):
    """Base class for tabs."""
    pass


class LoginRegisterScreen(Screen):
    """Screen with tabs for login and registration."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_repo = UserRepository()
        self.build_ui()
    
    def build_ui(self):
        """Build the login/register UI."""
        layout = MDBoxLayout(orientation='vertical')
        
        # Title
        title = MDTopAppBar(title='Job Portal')
        layout.add_widget(title)
        
        # Tabs
        self.tabs = MDTabs()
        
        # Login Tab
        login_tab = Tab(title='Login')
        login_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.login_username = MDTextField(
            hint_text='Username',
            helper_text='Enter your username',
            helper_text_mode='on_error'
        )
        self.login_password = MDTextField(
            hint_text='Password',
            password=True,
            helper_text='Enter your password',
            helper_text_mode='on_error'
        )
        
        login_button = MDRectangleFlatButton(
            text='Login',
            pos_hint={'center_x': 0.5},
            on_release=self.do_login
        )
        
        # login_layout.add_widget(MDLabel(text='', size_hint_y=0.3))
        login_layout.add_widget(self.login_username)
        login_layout.add_widget(self.login_password)
        # login_layout.add_widget(MDLabel(text='', size_hint_y=0.1))
        login_layout.add_widget(login_button)
        login_layout.add_widget(MDLabel(text='', size_hint_y=0.3))
        
        login_tab.add_widget(login_layout)
        
        # Register Tab
        register_tab = Tab(title='Register')
        register_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=5)
        
        self.reg_username = MDTextField(hint_text='Username')
        self.reg_password = MDTextField(hint_text='Password', password=True)
        self.reg_fullname = MDTextField(hint_text='Full Name')
        self.reg_email = MDTextField(hint_text='Email')
        self.reg_bio = MDTextField(hint_text='Bio', multiline=True)
        self.reg_skills = MDTextField(hint_text='Skills (comma separated)')
        
        
        register_button = MDRectangleFlatButton(
            text='Register',
            pos_hint={'center_x': 0.5},
            on_release=self.do_register
        )
        
        register_layout.add_widget(self.reg_username)
        register_layout.add_widget(self.reg_password)
        register_layout.add_widget(self.reg_fullname)
        register_layout.add_widget(self.reg_email)
        register_layout.add_widget(self.reg_bio)
        register_layout.add_widget(self.reg_skills)
        register_layout.add_widget(register_button)
        register_layout.add_widget(MDLabel(text='', size_hint_y=1))
        
        register_tab.add_widget(register_layout)
        
        self.tabs.add_widget(login_tab)
        self.tabs.add_widget(register_tab)
        
        layout.add_widget(self.tabs)
        self.add_widget(layout)
    
    def hash_password(self, password: str) -> str:
        """Hash password using MD5."""
        return hashlib.md5(password.encode()).hexdigest()
    
    def do_login(self, instance):
        """Handle login."""
        username = self.login_username.text
        password = self.hash_password(self.login_password.text)
        
        # Find user by username
        user = self.user_repo.get_by_username(username)
        
        if user and user.password == password:
            # Success - go to main screen
            self.manager.current_user_id = user.id
            self.manager.current = 'main'

            Toast.success(f'Welcome, {user.full_name}!')
        else:
            self.clear_login_fields(with_error=True)
            Toast.error(f'Your username or password was incorrect.')

    
    def do_register(self, instance):
        """Handle registration."""
        user = User(
            id=0,
            username=self.reg_username.text,
            password=self.hash_password(self.reg_password.text),
            full_name=self.reg_fullname.text,
            email=self.reg_email.text,
            profile_path='',
            resume_path='',
            bio=self.reg_bio.text,
            skills_text=self.reg_skills.text
        )

        try:
            created_user = self.user_repo.create(user)
            if created_user.id:
                Toast.success('Registered successfully!')
        except Exception as e:
            Toast.error(str(e))
            self.clear_register_fields(with_error=True)
    
    def clear_login_fields(self, with_error=False):
        """Clear login fields."""
        self.login_username.text = ''
        self.login_password.text = ''
        self.login_username.error = with_error
        self.login_password.error = with_error
    
    def clear_register_fields(self, with_error=False):
        """Clear registration fields."""
        self.reg_username.text = ''
        self.reg_password.text = ''
        self.reg_fullname.text = ''
        self.reg_email.text = ''
        self.reg_bio.text = ''
        self.reg_skills.text = ''

        self.reg_username.error = with_error
        self.reg_password.error = with_error
        self.reg_fullname.error = with_error
        self.reg_email.error = with_error
        self.reg_bio.error = with_error
        self.reg_skills.error = with_error
