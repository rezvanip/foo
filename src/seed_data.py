"""Seed database with sample data for testing."""
from database import init_db
from models import User, Company, Offer, Application, Status
from repositories import UserRepository, CompanyRepository, OfferRepository, ApplicationRepository
import hashlib


def seed_database():
    """Add sample data to database."""
    user_repo = UserRepository()
    company_repo = CompanyRepository()
    offer_repo = OfferRepository()
    app_repo = ApplicationRepository()

    # Create sample user
    user = User(
        id=0,
        username='demo',
        password=hashlib.md5('demo'.encode()).hexdigest(),
        full_name='Demo User',
        email='demo@example.com',
        profile_path='assets/profile.jpg',
        resume_path='assets/resume.pdf',
        bio='Experienced software developer',
        skills_text='Python, SQL, JavaScript, React'
    )
    created_user = user_repo.create(user)
    print(f"Created user: {created_user.username}")

    # Create sample companies
    companies = [
        Company(id=0, name='Tech Corp', logo_path='assets/tech-corp.jpg', location='San Francisco', description='Leading tech company'),
        Company(id=0, name='StartupXYZ', logo_path='assets/startupxyz.jpg', location='New York', description='Fast-growing startup'),
        Company(id=0, name='Enterprise Inc', logo_path='assets/enterprise.jpg', location='Chicago', description='Fortune 500 company')
    ]
    
    created_companies = []
    for company in companies:
        created = company_repo.create(company)
        created_companies.append(created)
        print(f"Created company: {created.name}")
    
    # Create sample offers
    offers = [
        Offer(id=0, company_id=created_companies[0].id, title='Python Developer', 
              skill_tags='Python, SQL, Django', salary=90000.0, 
              description='Looking for experienced Python developer', created_at=1234567890),
        Offer(id=0, company_id=created_companies[1].id, title='Frontend Developer',
              skill_tags='JavaScript, React, CSS', salary=80000.0,
              description='Frontend role with modern stack', created_at=1234567891),
        Offer(id=0, company_id=created_companies[2].id, title='Full Stack Developer',
              skill_tags='Python, JavaScript, SQL', salary=95000.0,
              description='Full stack position', created_at=1234567892),
        Offer(id=0, company_id=created_companies[0].id, title='Data Scientist',
              skill_tags='Python, Machine Learning, SQL', salary=100000.0,
              description='ML and data analysis role', created_at=1234567893)
    ]
    
    created_offers = []
    for offer in offers:
        created = offer_repo.create(offer)
        created_offers.append(created)
        print(f"Created offer: {created.title}")
    
    # Create sample application
    application = Application(
        id=0,
        user_id=created_user.id,
        offer_id=created_offers[0].id,
        status=Status.Applied
    )
    created_app = app_repo.create(application)
    print(f"Created application for user {created_app.user_id}")
    
    print("\nSample data created successfully!")
    print(f"Login with: username='demo', password='demo'")


if __name__ == '__main__':
    # Initialize fresh database
    init_db.init_database()
    seed_database()
