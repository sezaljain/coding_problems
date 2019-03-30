#Designing a relationship
"""

two functions -- add child and add spouse
two modes -- traditional, modern family (restrictions on the above functions vary based on the mode)

child edge: person_id  bio_mother_id bio_father_id parent1_id parent2_id
spouse edge: husband_id wife_id

person: id, gender, name, dob
relationship: id, slug, english_name, hindi_name, pattern

base relationships to define any relationships--
wife,husband,father,mother,brother,sister,son, daughter

nanad:
.husband.sister
saas:
.husband.mother+.wife.mother
samdhi:
.daughter.husband.father+.son.wife.father
samdhan:
.daughter.husband.mother+.son.wife.mother
"""

# data will be person, relationships(child/spouse)
# import csv,uuid
# from dataclasses import dataclass,astuple

# def read_csv(filepath):
# 	data = []
# 	with open(filepath) as f:
# 		reader=csv.reader(f)
# 		# next(reader, None)
# 		for row in reader:
# 			if row:
# 				data.append(row)
# 	return data

# def calc_uid():
# 	return uuid.uuid4().hex[:6]

def calc_id(obj):
	obj_to_list_map = {Person:person_list,
						SpouseRelationship:spouse_list,
						ChildParentRelationship:child_list}
	obj_list = obj_to_list_map[type(obj)]
	current_max = 0
	if obj_list:
		current_max = max(obj_list,key=lambda x:int(x.id)).id
	return current_max+1


class Person(object):
	def __init__(self,**kwargs):
		super(Person, self).__init__()
		self.id=kwargs.get('id',calc_id(self))
		self.gender=kwargs.get('gender')
		self.name=kwargs.get('name')
		self.uid=calc_uid()
		person_list.append(self)


	@staticmethod
	def get_from_id(id_):
		id_=int(id_)
		output = filter(lambda x : x.id==id_, person_list)
		if len(output)>1:
			raise ValueError("Multiple ppl with same id")
		return output[0]

	@staticmethod
	def get_from_name(name_):
		output = filter(lambda x : x.name==name_, person_list)
		if len(output)>1:
			raise ValueError("Multiple ppl with same name")
		if len(output)==0:
			return None
		return output[0]

	@classmethod
	def get_or_create(cls,name,gender):
		output = filter(lambda x:x.gender==gender and x.name==name, person_list)
		if len(output)>1:
			raise ValueError("Multiple ppl with same name and gender")
		elif len(output)==1:
			return output[0]
		elif len(output)==0:
			p= cls(name=name,gender=gender)
			return p


	def __repr__(self):
		return "#{} {} {}".format(self.id,self.name,self.gender)

	def mother(self):
		# return ChildParentRelationship.
		pass

	def get_relationship(self,person_name,relationship_name):
		pass


class ChildParentRelationship(object):
	""" The Edge to represent a parent child relationship. Father has been omitted for now, but can be easily added
		While adding this edge: 
			CHILD_ADDITION_FAILED
			CHILD_ALREADY_EXISTS
			CHILD_ADDITION_FAILED
	"""
	def __init__(self,**kwargs):
		super(ChildParentRelationship, self).__init__()
		self.id=kwargs.get('id',calc_id(self))
		self.child = kwargs.get('child')
		self.mother = kwargs.get('mother')
		# self.father = kwargs.get('father')
		child_list.append(self)


	def __repr__(self):
		return "Mother:{} Child:{}".format(self.mother,self.child)

	@staticmethod
	def get_child_rel(**kwargs):
		child = kwargs.get('child')
		mother = kwargs.get('mother',None)
		# father = kwargs.get('father',None)
		success,relationship,msg = False,None,''
		rels = child_list
		rels = filter(lambda x:x.child==child,rels)
		if len(rels)>1:
			msg="A person cant be a child of two mothers"
		elif len(rels)==0:
			success = True
		elif mother and rels[0].mother!=mother:
			msg = "Already a child of other mother"
		else:
			success,relationship = True,rels[0]
		return success,msg,relationship

	# @classmethod
	# def get_or_create_via_name(cls,child_name,child_gender,mother_name,father_name):
	# 	child = Person.get_or_create(child_name)
	# 	mother = Person.get_or_create(mother_name,'Female')
	# 	# father = Person.get_or_create(father_name,'Male')
	# 	cls.get_or_create(child,mother)

	# @classmethods
	# def get(cls,child,mother):
	# 	success,existing = cls.get_child_rel(child=child,mother=mother)
	# 	if not success:
	# 		return success,msg
	# 	if existing:
	# 		return success,""
	# 	else:
	# 		c = cls(child=child,mother=mother)
			# return c

	@classmethod
	def add_child_for_mother(cls,child_name,child_gender,mother_name):
		mother = Person.get_from_name(mother_name)
		if not mother:
			return False, "CHILD_ADDITION_FAILED"
		elif mother.gender!='Female':
			return False, "CHILD_ADDITION_FAILED"

		child = Person.get_or_create(child_name,child_gender)
		success,msg,relationship = cls.get_child_rel(child=child,mother=mother)	
		if not success:
			return False, "CHILD_ADDITION_FAILED"
		elif relationship:
			return False, "CHILD_ALREADY_EXISTS"

		cls(child=child,mother=mother)
		return True,"CHILD_ADDITION_SUCCEEDED" 




class SpouseRelationship(object):
	def __init__(self,**kwargs):
		super(SpouseRelationship, self).__init__()
		self.id=kwargs.get('id',calc_id(self))
		self.wife = kwargs.get('wife')
		self.husband = kwargs.get('husband')
		spouse_list.append(self)

	def __repr__(self):
		return "Husband:{} Wife:{}".format(self.husband,self.wife)

	@staticmethod
	def get_spouse_rel(**kwargs):
		wife = kwargs.get('wife',None)
		husband = kwargs.get('husband',None)
		rels = spouse_list
		if husband:
			rels = filter(lambda x:x.husband==husband ,rels)
		if wife:
			rels = filter(lambda x:x.wife==wife ,rels)
		if len(rels)>1:
			raise ValueError("Multiple existing relationships")
		elif len(rels)==0:
			return None
		else:
			return rels[0]

	@classmethod
	def get_or_create_via_name(cls,husband_name,wife_name):
		success = False
		husband = Person.get_from_name(husband_name)
		if husband and husband.gender!='Male':
			return success,"the first entry in the row in male"
		wife = Person.get_from_name(wife_name)
		if wife and wife.gender!='Female':
			return success,"the second entry in the row in female"
		husband = Person.get_or_create(husband_name,'Male')
		wife = Person.get_or_create(wife_name,'Female')
		cls.get_or_create(husband,wife)
		return success,"SPOUSE_ADDITION_SUCCEEDED"

	@classmethod
	def get_or_create(cls,husband,wife):
		existing = cls.get_spouse_rel(husband=husband,wife=wife)
		if existing:
			return existing
		else:
			s = cls(husband=husband,wife=wife)
			return s



def request_tree(request_type,data):
	if request_type=='ADD_SPOUSE':
		# First entry is husband and second is wife
		success,msg = SpouseRelationship.get_or_create_via_name(data[0],data[1])
	elif request_type=='ADD_CHILD':
		# Mother should already be in table
		# First entry is mother name, then child name and gender
		success,msg = ChildParentRelationship.add_child_for_mother(data[1],data[2],data[0])
	elif request_type=='GET_RELATIONSHIP':
		# First entry is name, second entry is relationship name
		success,msg = Person.get_relationship(data[0],data[1])
		pass
	# print request_type,data,
	print msg


def main():
	print ("Welcome to Shan family")
	global person_list
	global spouse_list
	global child_list
	person_list = []
	spouse_list = []
	child_list = []
	with open("initial.txt") as file1:
		reader = csv.reader(file1,delimiter=" ")
		for row in  reader:
			request_type = row.pop(0)
			request_tree(request_type,row)
	# for p in person_list:
	# 		print p
	# for p in spouse_list:
	# 		print p
	# for p in child_list:
	# 		print p


if __name__ == '__main__':
	main()

import csv,uuid
# from dataclasses import dataclass,astuple

def read_csv(filepath):
	data = []
	with open(filepath) as f:
		reader=csv.reader(f)
		# next(reader, None)
		for row in reader:
			if row:
				data.append(row)
	return data

def calc_uid():
	return uuid.uuid4().hex[:6]


custom_relationship_options=[
["Paternal-Uncle", "father.brother"],
["Maternal-Uncle", "mother.brother"],
["Paternal-Aunt", "father.sister"],
["Maternal-Aunt", "mother.sister"],
["Sister-In-Law", "husband.sister+wife.sister+.brother.wife"],
["Brother-In-Law", "wife.brother+husband.brother+.sister.husband"],
["Sibling", "brother+.sister"]]


#wife,husband,father,mother,brother,sister,son, daughter
base_relationships=["husband","daughter","son"]

class AddRelationship:
	"""
	Adding new relationships in the tree. The ones permitted are spouse relationships and mother to child relationships
	"""
	def __init__():
		pass
	def self.validate_add_person(self,person_name,person_gender):
		# Rule 1:Person should have a name not already in tree
		return True, "go ahead"

	def add_person(self,person_name,person_gender):
		# success,msg = self.validate_add_person()
		person_list.append([person_name,person_gender])
		pass

	def validate_add_child(self,mother_name,child_name,child_gender):
		# Rule 1: Mother should already exist in the tree
		# Rule 2: Mother should be female
		# Rule 3: child name should not be in tree already (tree has unique names)
		# Rule 4: the same relationship should not exist already
		return True,"go ahead"

	def validate_add_spouse(self,wife_name,husband_name):
		# Rule 1: Wife should be male if already in tree
		# Rule 2: Husband should be male if already in tree
		# Rule 3: Neither of wife or husband should already have a spouse relationship in tree
		return True,"go ahead"

	def add_child(self,mother_name,child_name,child_gender):
		success,msg = self.validate_add_child(mother_name,child_name,child_gender)
		if success:
			mother = self.get_person(mother_name)
			child = self.get_person(child_name,child_gender)
			if not child:
				child = self.add_person(child_name,child_gender)
			rel = "daughter" if child_gender=="Female" else "son"
			relationship_list.append(rel,mother[0],child[0])
		return success,msg

	def add_spouse(self,wife_name,husband_name):
		success,msg = self.validate_add_spouse(wife_name,husband_name)
		if success:
			wife = self.get_person(wife_name)
			if not wife:
				wife = self.add_person(wife_name,"Female")
			husband = self.get_person(husband_name)
			if not husband:
				husband = self.add_person(husband_name,"Male")
			relationship_list.append("husband",wife[0],husband[0])
		return success,msg


class GetRelationship:
	""" This is a class instead of a function to make it chainable
	ORDER 0 relationships -- husband, daughter and son. These go into the data table
	ORDER 1 relationship -- listed in relation_to_function. These are used to describe any possible relationship in a family tree
	ORDER 2 relationship -- any possible combination user can come up using order 1 relationships. examples in custom_relationship_options

	All functions accept a list of people as input. This is so that the function can be chained
	for eg. for brother in law  -- sister.husband
		if there are multiple sisters .. the function will work on all of them together to get a list of husbands

	"""

	def __init__(self,initial_person_list):
		self.relationship_of = initial_person_list

		self.relation_to_function ={
		##This is a list of ORDER 1 relationships based on which higher order custom relationships can be formed
		## eg. mother in law -- "wife.mother+husband.mother"
		## This list mostly exists to make it easy to add complicated relationshps
		## and to be able to add relationships like brother/sister 
		## (mother.son or mother.daughter will include the original person as well)
		"daughter":self.get_daughter,
		"son":self.get_son,
		"husband":self.get_husband,
		"mother":self.get_mother,
		"wife":self.get_wife,
		"father":self.get_father,
		"brother":self.get_brother,
		"sister":self.get_sister,
		}

	def get_relationship(self,input_people,relationship_type,inverse=False):
		""" This is the lowest order get relationship function
			only works if relationship_type is in [daughter,son,husband]
		"""
		if inverse == False:
			relation_of_id,relation_id = 1,2
		else:
			relation_of_id,relation_id = 2,1
		output_person_list = map(
			lambda x:filter(lambda y:y[0]==x[relation_id],person_list)[0],  #extracting person from relationship
			filter(#extracting the desired relationship for people in relationship_of
					lambda x:x[0]==relationship_type and x[relation_of_id] in [y[0] for y in input_people],
					relationship_list
					)
		)
		return output_person_list


	def get_husband(self,input_people):
		return self.get_relationship(input_people,"husband")

	def get_wife(self,input_people):
		return self.get_relationship(input_people,"husband",inverse=True)

	def get_daughter(self,input_people):
		return self.get_relationship(input_people,"daughter")

	def get_son(self,input_people):
		return self.get_relationship(input_people,"son")

	def get_mother(self,input_people):
		output_person_list = self.get_relationship(input_people,"daughter",True)+self.get_relationship(input_people,"son",True)
		return output_person_list

	def get_father(self,input_people):
		mother_list = self.get_mother(input_people)
		output_person_list = self.get_husband(mother_list)
		return output_person_list

	def get_sibling(self,input_people,gender):
		final_output_person_list = []
		for person in input_people:
			#Find motherr of the input_people first
			mother_list = self.get_mother([person])

			#Then based on the gender, check for daughter or son relationship
			relationship_type='daughter' if gender=='Female' else 'son'
			output_person_list=self.get_relationship(mother_list,relationship_type)

			#Finally remove the original person from the sibling
			#This is why we have looped over input_people
			output_person_list.remove(person)
			final_output_person_list = final_output_person_list+output_person_list

		return final_output_person_list

	def get_brother(self,input_people):
		return self.get_sibling(input_people,'Male')

	def get_sister(self,input_people):
		return self.get_sibling(input_people,'Female')

	@staticmethod
	def check_validity_of_relationship(custom_relationship):
		#Step1: lookup relationship in relationship_options
		filter(lambda x:x[0]==custom_relationship,custom_relationship_options)

	def get_custom_relationship(self,custom_relationship):
		input_people = self.relationship_of
		for custom_relationship_part in custom_relationship.split('+'):
			for order1_rel in custom_relationship_part.split('.'):
				output_people = self.relation_to_function[order1_rel](input_people)
				input_people=output_people
				print "output_people",output_people




# custom_relationship_options
# base_relationship



person_list =[
[1,"Arya1","Female"],
[2,"Arya2","Female"],
[3,"Arya3","Female"],
[4,"Arya4","Female"],
[5,"Arya5","Female"],
[6,"Arya6","Female"],
[7,"Arya7","Female"],
[8,"Geoff","Male"],

]
relationship_list =[ 
["daughter",1,2],
["daughter",1,3],
["daughter",3,4],
["daughter",3,5],
["husband",1,8]]