from App.database import db

class Accolade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) # Gold Badge
    description = db.Column(db.String(200), nullable=True) # Awarded for 1000 hours of voulnteering
    threshold = db.Column(db.Integer, nullable=False) # 1000 hours

    def __init__(self, name, description, threshold):
        self.name = name
        self.description = description
        self.threshold= threshold

    def __repr__(self):
        return f'<Accolade {self.name}>'
    
    