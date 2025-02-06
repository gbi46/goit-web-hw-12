from datetime import datetime, timedelta
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session
from sqlalchemy.types import String
from src.schemas import ContactModel
from src.database.models import Contact, User
from typing import List

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        additional_info=body.additional_info,
        user_id=user.id,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return (db.query(Contact)
            .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
            .first())

async def get_contact_by_first_name(contact_first_name: str, user: User, db: Session) -> Contact:
    contact_first_name = contact_first_name
    return (db.query(Contact)
            .filter(and_(Contact.first_name == contact_first_name, Contact.user_id == user.id))
            .first())

async def get_contact_by_last_name(contact_last_name: str, user: User, db: Session) -> Contact:
    contact_last_name = contact_last_name.strip()
    return (db.query(Contact)
            .filter(Contact.last_name == contact_last_name, Contact.user_id == user.id)
            .first())

async def get_contact_by_email(contact_email: str, user: User, db: Session) -> Contact:
    contact_email = contact_email.strip()
    return (db.query(Contact)
            .filter(Contact.email == contact_email, Contact.user_id == user.id)
            .first())

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return (db.query(Contact)
            .filter(Contact.user_id == user.id)
            .offset(skip).limit(limit).all())

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact)
               .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
               .first())
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact:
    contact = (db.query(Contact)
               .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
               .first())
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact

async def get_upcoming_birthdays(user: User, db: Session) -> List[Contact]:
    today_date = datetime.now()
    dates_to_check = [(today_date + timedelta(days=i)).strftime("%m-%d") for i in range(8)]
    contacts = (db.query(Contact)
                .filter(and_(Contact.user_id == user.id,
                    or_(*[func.cast(Contact.birthday, String).like(f"%{d}%") for d in dates_to_check])))
                .all())
    return contacts