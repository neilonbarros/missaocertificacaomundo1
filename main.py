from app import models as appmodels
from app import packages as apppackages

model_department = appmodels.ApplicationDepartments()
model_department.department = 'desenvolvimento'
model_department.save()

model_jobposition = appmodels.ApplicationJobPositions()
model_jobposition.department = model_department
model_jobposition.jobposition = 'desenvolvedor'
model_jobposition.save()

model_people = appmodels.ApplicationPeoples()
model_people.department = model_department
model_people.jobposition = model_jobposition
model_people.status = True
model_people.cpf = '41337418897'
model_people.fullname = 'wellington cesar fonseca'
model_people.save()

salt, hashed = apppackages.text.hashed.hash_new_password('wellington')

model_password = appmodels.ApplicationPasswords()
model_password.people = model_people
model_password.salt = salt
model_password.hashed = hashed
model_password.save()
