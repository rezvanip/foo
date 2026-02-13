"""Screen displaying user's job applications with status tracking."""
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip

from models import Application, Offer, Company
from repositories import ApplicationRepository, OfferRepository, CompanyRepository


class ApplicationCard(MDCard):
    """Card showing job application with color-coded status indicator."""
    
    def __init__(self, application: Application, offer: Offer, company: Company, **kwargs):
        """Initialize with application, offer and company data."""
        super().__init__(**kwargs)
        self.application = application
        self.offer = offer
        self.company = company
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 100
        self.padding = 10
        self.spacing = 5
        self.elevation = 2
        self.build_ui()
    
    def build_ui(self):
        """Build card layout with title, company and status color."""
        title = MDLabel(
            text=self.offer.title,
            font_style='H6',
            size_hint_y=None,
            height=25
        )
        company = MDLabel(
            text=f"Company: {self.company.name}",
            theme_text_color='Secondary',
            size_hint_y=None,
            height=20
        )
        
        status_box = MDBoxLayout(size_hint_y=None, height=30)
        status_label = MDLabel(
            text=f"Status: {self.application.status.value.upper()}",
            theme_text_color='Custom',
            text_color=self.get_status_color(),
            bold=True
        )
        status_box.add_widget(status_label)
        
        self.add_widget(title)
        self.add_widget(company)
        self.add_widget(status_box)
    
    def get_status_color(self):
        """Return RGBA color tuple based on application status."""
        status = self.application.status
        if status.value == 'applied':
            return (0.2, 0.4, 1, 1)  # Blue
        elif status.value == 'pending':
            return (1, 0.6, 0.2, 1)  # Orange
        elif status.value == 'rejected':
            return (1, 0.2, 0.2, 1)  # Red
        elif status.value == 'accepted':
            return (0.2, 0.8, 0.2, 1)  # Green
        return (0.5, 0.5, 0.5, 1)


class ApplicationsScreen(Screen):
    """Screen listing all applications submitted by current user."""
    
    def __init__(self, **kwargs):
        """Initialize repositories and build UI."""
        super().__init__(**kwargs)
        self.application_repo = ApplicationRepository()
        self.offer_repo = OfferRepository()
        self.company_repo = CompanyRepository()
        self.user_id = None
        self.build_ui()
    
    def build_ui(self):
        """Create scrollable list layout for application cards."""
        layout = MDBoxLayout(orientation='vertical')
        
        header = MDBoxLayout(size_hint_y=None, height=50, padding=10)
        title = MDLabel(
            text='My Applications',
            font_style='H5'
        )
        header.add_widget(title)
        layout.add_widget(header)
        
        scroll = MDScrollView()
        self.applications_list = MDList(spacing=10)
        scroll.add_widget(self.applications_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_applications(self):
        """Fetch and display applications for current user."""
        self.applications_list.clear_widgets()
        applications = self.application_repo.get_by_user(self.user_id)
        
        for application in applications:
            offer = self.offer_repo.get_by_id(application.offer_id)
            if offer:
                company = self.company_repo.get_by_id(offer.company_id)
                if company:
                    card = ApplicationCard(application, offer, company)
                    self.applications_list.add_widget(card)

    def on_press(self, *args, **kwargs):
        """Refresh applications list when tab selected."""
        self.load_applications()
