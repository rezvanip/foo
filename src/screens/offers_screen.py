from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout

from models import Offer, Company, Application, Status
from repositories import OfferRepository, CompanyRepository, ApplicationRepository


class OfferCard(MDCard):
    """Card widget for displaying an offer."""
    
    def __init__(self, offer: Offer, company: Company, on_click=None, **kwargs):
        super().__init__(**kwargs)
        self.offer = offer
        self.company = company
        self.on_click = on_click
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 120
        self.padding = 10
        self.spacing = 5
        self.elevation = 2
        self.build_ui()
    
    def build_ui(self):
        """Build the card UI."""

        layout = MDBoxLayout(spacing=10)
        company_logo = Image(source=self.company.logo_path, allow_stretch=True, keep_ratio=True, size_hint_x=0.1)
        layout.add_widget(company_logo)

        details_layout = MDBoxLayout(orientation='vertical')
        details_layout.add_widget(MDLabel(
            text=self.offer.title,
            font_style='H6',
            size_hint_y=None,
            height=30
        ))

        details_layout.add_widget(MDLabel(
            text=f"{self.company.name}",
            theme_text_color='Secondary',
            size_hint_y=None,
            height=20
        ))

        details_layout.add_widget(MDLabel(
            text=f"{self.company.location} | ${self.offer.salary:,.0f}",
            theme_text_color='Secondary',
            size_hint_y=None,
            height=20
        ))

        layout.add_widget(details_layout)

        self.add_widget(layout)
        
        # Bind click
        self.bind(on_release=self.on_card_click)
    
    def on_card_click(self, instance):
        """Handle card click."""
        if self.on_click:
            self.on_click(self.offer, self.company)


class OffersScreen(Screen):
    """Screen for displaying job offers."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.offer_repo = OfferRepository()
        self.company_repo = CompanyRepository()
        self.application_repo = ApplicationRepository()
        self.offers = []
        self.dialog = None
        self.filter_dialog = None
        self.build_ui()

    def build_ui(self):
        """Build the offers UI."""
        layout = MDBoxLayout(orientation='vertical')
        
        # Header with filter button
        header = MDBoxLayout(size_hint_y=None, height=50, padding=10)
        title = MDLabel(
            text='Job Offers',
            font_style='H5',
            size_hint_x=0.8
        )
        filter_btn = MDIconButton(
            icon='filter',
            on_release=self.show_filter_dialog
        )
        header.add_widget(title)
        header.add_widget(filter_btn)
        layout.add_widget(header)
        
        # Scrollable list
        scroll = MDScrollView()
        self.offers_list = MDList(spacing=10)
        scroll.add_widget(self.offers_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

        self.create_filter_dialog()
    
    def load_offers(self, user_id=None):
        """Load and display offers."""
        self.offers_list.clear_widgets()
        self.offers = self.offer_repo.get_all()
        
        for offer in self.offers:
            company = self.company_repo.get_by_id(offer.company_id)
            if company:
                card = OfferCard(offer, company, on_click=self.show_offer_details)
                self.offers_list.add_widget(card)
    
    def create_filter_dialog(self):
        """Create the filter dialog once to preserve state."""
        content = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=250)
        
        self.filter_title = MDTextField(hint_text='Title contains')
        self.filter_min_salary = MDTextField(hint_text='Min Salary', input_filter='float')
        self.filter_max_salary = MDTextField(hint_text='Max Salary', input_filter='float')
        self.filter_skills = MDTextField(hint_text='Skills (comma separated)')
        
        content.add_widget(self.filter_title)
        content.add_widget(self.filter_min_salary)
        content.add_widget(self.filter_max_salary)
        content.add_widget(self.filter_skills)
        
        self.filter_dialog = MDDialog(
            title='Filter Offers',
            type='custom',
            content_cls=content,
            buttons=[
                MDRaisedButton(text='Clear', on_release=self.clear_filters),
                MDRaisedButton(text='Cancel', on_release=self.close_filter_dialog),
                MDRaisedButton(text='Apply', on_release=self.apply_filter)
            ]
        )
    
    def show_filter_dialog(self, instance):
        """Show filter dialog."""
        self.filter_dialog.open()
    
    def close_filter_dialog(self, instance):
        """Close the filter dialog (preserve content)."""
        if self.filter_dialog:
            self.filter_dialog.dismiss()
    
    def clear_filters(self, instance):
        """Clear all filter fields."""
        self.filter_title.text = ''
        self.filter_min_salary.text = ''
        self.filter_max_salary.text = ''
        self.filter_skills.text = ''
    
    def apply_filter(self, instance):
        """Apply filters to offers."""
        title_filter = self.filter_title.text.lower()
        min_salary = float(self.filter_min_salary.text) if self.filter_min_salary.text else 0
        max_salary = float(self.filter_max_salary.text) if self.filter_max_salary.text else float('inf')
        skills_filter = [s.strip().lower() for s in self.filter_skills.text.split(',')] if self.filter_skills.text else []
        
        self.offers_list.clear_widgets()
        
        for offer in self.offers:
            # Check title
            if title_filter and title_filter not in offer.title.lower():
                continue
            
            # Check salary
            if offer.salary < min_salary or offer.salary > max_salary:
                continue
            
            # Check skills
            if skills_filter:
                offer_skills = [s.strip().lower() for s in offer.skill_tags.split(',')]
                if not any(skill in offer_skills for skill in skills_filter):
                    continue
            
            company = self.company_repo.get_by_id(offer.company_id)
            if company:
                card = OfferCard(offer, company, on_click=self.show_offer_details)
                self.offers_list.add_widget(card)
        
        self.close_filter_dialog(None)
    
    def show_offer_details(self, offer: Offer, company: Company):
        """Show offer details dialog."""
        content = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        
        content.add_widget(MDLabel(text=f"Title: {offer.title}", font_style='H6'))
        content.add_widget(MDLabel(text=f"Company: {company.name}"))
        content.add_widget(MDLabel(text=f"Location: {company.location}"))
        content.add_widget(MDLabel(text=f"Salary: ${offer.salary:,.0f}"))
        content.add_widget(MDLabel(text=f"Skills: {offer.skill_tags}"))
        content.add_widget(MDLabel(text=f"Description: {offer.description}", theme_text_color='Secondary'))
        
        self.dialog = MDDialog(
            title='Offer Details',
            type='custom',
            content_cls=content,
            buttons=[
                MDRaisedButton(text='Close', on_release=self.close_dialog),
                MDRaisedButton(text='Apply', on_release=lambda x: self.apply_to_offer(offer))
            ]
        )
        self.dialog.open()
    
    def close_dialog(self, instance):
        """Close the dialog."""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
    
    def apply_to_offer(self, offer: Offer):
        """Apply to an offer."""
        user_id = self.manager.current_user_id if self.manager else None
        
        if user_id is None:
            self.close_dialog(None)
            return
        
        # Check if already applied
        existing = self.application_repo.get_by_user_and_offer(user_id, offer.id)
        if existing:
            self.close_dialog(None)
            return
        
        # Create application
        application = Application(
            id=0,
            user_id=user_id,
            offer_id=offer.id,
            status=Status.Applied
        )
        self.application_repo.create(application)
        self.close_dialog(None)

    def on_press(self, *args, **kwargs):
        self.load_offers()
