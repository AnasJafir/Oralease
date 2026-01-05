from app.repositories.treatment_repo import TreatmentRepository
from app.schemas.treatment_schema import treatment_plan_schema, treatment_plans_schema
from marshmallow import ValidationError

class TreatmentService:
    @staticmethod
    def get_treatments(patient_id=None):
        plans = TreatmentRepository.get_all(patient_id)
        return treatment_plans_schema.dump(plans)

    @staticmethod
    def get_treatment_by_id(id):
        plan = TreatmentRepository.get_by_id(id)
        return treatment_plan_schema.dump(plan)

    @staticmethod
    def create_treatment(data):
        try:
            # Validate data using schema (load returns dict or model depending on schema config)
            # Assuming schema loads into dict or we extract what we need
            validated_data = treatment_plan_schema.load(data)
            # If schema returns a model instance (load_instance=True), we might need to adjust repo
            # But based on current api, it seems to return an object. 
            # Let's check schema implementation if possible, but for now assume we pass dict to repo
            # If validated_data is an object, we convert to dict for repo or adjust repo to take object
            
            # Actually, looking at previous API: new_plan = treatment_plan_schema.load(json_data)
            # It seems load returns a TreatmentPlan object directly if load_instance=True in Marshmallow-SQLAlchemy
            # Let's assume we want to keep it simple and pass data to repo.
            
            # To be safe and consistent with the new architecture, let's assume the repo takes a dict.
            # But if the schema returns an object, we should use that.
            
            # Let's check if we can just pass the object to db.session.add in repo.
            # Yes, repo.create does TreatmentPlan(**data). This implies data is a dict.
            # If schema.load returns an object, we should change repo to accept object or change schema usage.
            
            # Let's stick to the previous pattern: 
            # new_plan = treatment_plan_schema.load(json_data) -> returns object
            # db.session.add(new_plan)
            
            # So my repo.create doing TreatmentPlan(**data) might be wrong if I pass an object.
            # I will adjust the service to handle this.
            
            # Wait, if I use the schema to load, I get an object (usually).
            # If I want to decouple, maybe I should validate and then pass dict.
            
            # Let's look at the previous API again:
            # new_plan = treatment_plan_schema.load(json_data)
            # db.session.add(new_plan)
            
            # So the schema creates the instance.
            # I will modify the repo to accept an instance or data.
            # Actually, let's make the service do the loading, and repo just saves.
            
            plan = treatment_plan_schema.load(data)
            saved_plan = TreatmentRepository.create(plan)
            return treatment_plan_schema.dump(saved_plan)
            
        except ValidationError as err:
            raise err

    @staticmethod
    def update_treatment(id, data):
        plan = TreatmentRepository.get_by_id(id)
        # Schema load with instance updates the plan object in place
        updated_plan = treatment_plan_schema.load(data, instance=plan, partial=True)
        # We pass the updated object to repo.update
        saved_plan = TreatmentRepository.update(plan, updated_plan)
        return treatment_plan_schema.dump(saved_plan)

    @staticmethod
    def delete_treatment(id):
        plan = TreatmentRepository.get_by_id(id)
        TreatmentRepository.delete(plan)
