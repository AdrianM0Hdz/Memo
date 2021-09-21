from . import db
import datetime

class FieldOfStudy(db.Model):

    __tablename__ = 'fields_of_study'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    url_alias = db.Column(db.String(64), unique=True, nullable=False)
    empty = db.Column(db.Boolean(), nullable=False)
    currently_reviewing = db.Column(db.Boolean(), nullable=False)
    notes = db.relationship('Note')

    def __repr__(self):
        return f'<FieldOfStudy id: {self.id} name: {self.name} url_alias: {self.url_alias} empty: {self.empty}>'

class Note(db.Model):

    _LOSS_PER_DAY = 0.5
    _GAIN_PER_REVIEW = 0.9 

    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    what = db.Column(db.String(128), unique=True, nullable=False)
    definition = db.Column(db.String(512), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields_of_study.id')) 
    _last_reviewed = db.Column(db.Date(), nullable=False, default=datetime.date.today())
    _strength = db.Column(db.Float(), nullable=False, default=1.0) # representative number of how well does the user know the note
    
    def _update_strength(self, add=0):
        """ Updates strength according to the last Day Reviewed"""
        delta = datetime.date.today() - self._last_reviewed
        self._strength -= (self._LOSS_PER_DAY * delta.days)
        self._strength += add 
    
    @property
    def strength(self):
        self._update_strength()
        return self._strength
    
    def review(self):
        """ Function review will update the note attributes taking into consideration
        that it just got correctly reviewed at the datetime of the calling of 
        the function 
        """
        self._update_strenght(add=self._GAIN_PER_REVIEW)
        self._last_reviewed = datetime.date.today()

    def __repr__(self):
        return f'Note what: {self.what}'