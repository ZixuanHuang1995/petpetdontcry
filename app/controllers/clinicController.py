from ..models import clinic
def get_clinic_data(ID):
    return clinic.query.filter_by(ID=ID).first()