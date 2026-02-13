"""Screen for managing user profile, resume and profile picture."""
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard

from models import User
from repositories import UserRepository


class ProfileImage(MDCard):
    """Square profile image widget wrapping Kivy Image."""
    
    def __init__(self, source='', **kwargs):
        """Initialize card with image displaying given source path."""
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (150, 150)
        self.elevation = 4
        self.padding = 2
        
        self.image = Image(source=source if source else '', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)
    
    def set_source(self, source):
        """Update displayed image from file path."""
        self.image.source = source


class ProfileScreen(Screen):
    """Profile management screen with file upload and edit capabilities."""
    
    def __init__(self, **kwargs):
        """Initialize repository and build editable profile form."""
        super().__init__(**kwargs)
        self.user_repo = UserRepository()
        self.current_user = None
        self.file_popup = None
        self.user_id = None
        self.build_ui()
    
    def build_ui(self):
        """Construct scrollable form with image, fields and file uploaders."""
        scroll = MDScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        logout_btn = MDRaisedButton(
            text='Logout',
            on_release=self.logout,
        )
        layout.add_widget(logout_btn)
        
        self.profile_image = Image(source='', allow_stretch=True, keep_ratio=False, size=(150, 150), size_hint=(None, None))
        self.profile_image.bind(on_release=self.choose_profile_image)
        layout.add_widget(self.profile_image)
        
        self.fullname_field = MDTextField(hint_text='Full Name')
        self.email_field = MDTextField(hint_text='Email')
        self.bio_field = MDTextField(hint_text='Bio', multiline=True)
        self.skills_field = MDTextField(hint_text='Skills (comma separated)')
        
        layout.add_widget(MDLabel(text='Profile Information', font_style='H6'))
        layout.add_widget(self.fullname_field)
        layout.add_widget(self.email_field)
        layout.add_widget(self.bio_field)
        layout.add_widget(self.skills_field)
        
        layout.add_widget(MDLabel(text='Resume', font_style='H6'))
        resume_box = MDBoxLayout(size_hint_y=None, height=50)
        self.resume_label = MDLabel(text='No resume uploaded')
        resume_btn = MDIconButton(icon='file-upload', on_release=self.choose_resume)
        resume_box.add_widget(self.resume_label)
        resume_box.add_widget(resume_btn)
        layout.add_widget(resume_box)
        
        save_btn = MDRaisedButton(
            text='Save Changes',
            on_release=self.save_profile,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(save_btn)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def load_profile(self):
        """Populate form fields from current user database record."""

        self.current_user = self.user_repo.get_by_id(self.user_id)
        
        if self.current_user:
            self.fullname_field.text = self.current_user.full_name
            self.email_field.text = self.current_user.email
            self.bio_field.text = self.current_user.bio
            self.skills_field.text = self.current_user.skills_text
            self.profile_image.source = self.current_user.profile_path
            self.resume_label.text = self.current_user.resume_path.split('/')[-1]
    
    def choose_profile_image(self, instance):
        """Open file browser filtering for image files only."""
        self.show_file_chooser(['*.png', '*.jpg', '*.jpeg'], self.set_profile_image)
    
    def choose_resume(self, instance):
        """Open file browser filtering for document files."""
        self.show_file_chooser(['*.pdf', '*.doc', '*.docx', '*.txt'], self.set_resume)
    
    def show_file_chooser(self, filters, callback):
        """Display popup with file browser and select/cancel buttons."""
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserListView(
            filters=filters,
            size_hint=(1, 0.9)
        )
        
        button_box = BoxLayout(size_hint=(1, 0.1))
        cancel_btn = Button(text='Cancel', on_release=lambda x: self.file_popup.dismiss())
        select_btn = Button(text='Select', on_release=lambda x: self.select_file(filechooser.selection, callback))
        
        button_box.add_widget(cancel_btn)
        button_box.add_widget(select_btn)
        
        content.add_widget(filechooser)
        content.add_widget(button_box)
        
        self.file_popup = Popup(
            title='Choose File',
            content=content,
            size_hint=(0.9, 0.9)
        )
        self.file_popup.open()
    
    def select_file(self, selection, callback):
        """Invoke callback with selected file path and close popup."""
        if selection:
            callback(selection[0])
            self.file_popup.dismiss()
    
    def set_profile_image(self, path):
        """Update profile image widget and store path in user model."""
        self.profile_image.set_source(path)
        if self.current_user:
            self.current_user.profile_path = path
    
    def set_resume(self, path):
        """Update resume label and store path in user model."""
        self.resume_label.text = path.split('/')[-1]
        if self.current_user:
            self.current_user.resume_path = path
    
    def save_profile(self, instance):
        """Persist profile changes to database."""
        if self.current_user:
            self.current_user.bio = self.bio_field.text
            self.current_user.skills_text = self.skills_field.text
            self.user_repo.update(self.current_user)
    
    def logout(self, instance):
        """Clear user session and navigate to login screen."""
        manager = self.parent.parent.parent.parent.parent.manager
        if manager:
            manager.current_user_id = None
            manager.current = 'login'

    def on_press(self, *args, **kwargs):
        """Refresh profile data when tab becomes active."""
        self.load_profile()