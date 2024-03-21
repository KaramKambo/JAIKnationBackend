from sqlalchemy import Column, Integer, String
from .. import db

class ML(db.Model):
    __tablename__ = "ml"
    id = Column(Integer, primary_key=True)
    _username = Column(String, nullable=False)
    _password = Column(String, nullable=False)

    def __init__(self, name, socialclass, age, sex, siblings, alone):
        self._name = name
        self._socialclass = socialclass
        self._age = age
        self._sex = sex
        self._siblings = siblings
        self._alone = alone
    
    def __repr__(self):
        return "id='%s', name='%s', socialclass='%s, age='%s, sex='%s, siblings='%s, alone='%s '" % (self.id, self.name, self.socialclass, self.age, self.sex, self.siblings, self.alone)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def socialclass(self):
        return self._socialclass
    
    @socialclass.setter
    def socialclass(self, value):
        self._socialclass = value
        
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
    
    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, value):
        self._sex = value
    
    @property
    def siblings(self):
        return self._siblings
    
    @siblings.setter
    def siblings(self, value):
        self._siblings = value
        
    @property
    def alone(self):
        return self._alone
    
    @alone.setter
    def alone(self, value):
        self._alone = value

    def to_dict(self):
        return {"id": self.id, "name": self.name, "socialclass": self.socialclass,"age": self.age, "sex": self.sex, "siblings": self.siblings, "alone": self.alone,}
    
def init_ml():
    db.session.commit()
