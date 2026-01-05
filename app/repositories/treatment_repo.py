from app.models import TreatmentPlan
from app.extensions import db

class TreatmentRepository:
    @staticmethod
    def get_all(patient_id=None):
        if patient_id:
            return TreatmentPlan.query.filter_by(patient_id=patient_id).all()
        return TreatmentPlan.query.all()

    @staticmethod
    def get_by_id(id):
        return TreatmentPlan.query.get_or_404(id)

    @staticmethod
    def create(data):
        # If data is already an instance, just save it
        if isinstance(data, TreatmentPlan):
            return TreatmentRepository.save(data)
        # Otherwise create new instance
        new_plan = TreatmentPlan(**data)
        return TreatmentRepository.save(new_plan)

    @staticmethod
    def save(plan):
        db.session.add(plan)
        db.session.commit()
        return plan

    @staticmethod
    def update(plan, data):
        # If data is a dict, update attributes
        if isinstance(data, dict):
            for key, value in data.items():
                setattr(plan, key, value)
        # If data is object (from schema load with instance=plan), it's already updated, just commit
        db.session.commit()
        return plan

    @staticmethod
    def delete(plan):
        db.session.delete(plan)
        db.session.commit()
