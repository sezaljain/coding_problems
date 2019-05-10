import uuid
import globals

def calc_uid():
	uid = uuid.uuid4().hex[:6]
	conflict = filter(lambda x:x[0]==uid,globals.person_list)
	if conflict:
		uid = calc_uid()
	return uid
	


class AddRelationship:
	"""
	Adding new relationships in the tree. The ones permitted are spouse relationships and mother to child relationships
	ADD_CHILD <mother_name> <child_name> <child_gender>
	ADD_SPOUSE <wife_name> <husband_name>
	"""
	def __repr__(self):
		return "AddRelationship:add_spouse/add_child"

	def get_person(self,person_name):
		matching_people = filter(lambda x:x[1]==person_name,globals.person_list)
		assert len(matching_people)<=1,"Should not be more than one person with the same name"
		if matching_people:
			return matching_people[0]
			# assert(person[2]==person_gender,"Person exists with another gender")
		return None

	def validate_add_person(self,person_name,person_gender):
		# Rule 1:Person should have a name not already in tree
		if self.get_person(person_name):
			return False, "Person with name already exists"
		return True, "go ahead"

	def add_person(self,person_name,person_gender):
		p = [calc_uid(),person_name,person_gender]
		globals.person_list.append(p)
		return p

	def validate_add_child(self,mother_name,child_name,child_gender):
		"""
		Rule 1: Mother should already exist in the tree
		Rule 2: Mother should be female
		Rule 3: child name should not be in tree already (tree has unique names)
		Rule 4: the same relationship should not exist already"""
		data = {'success':False}
		mother = self.get_person(mother_name)
		child = self.get_person(child_name)

		print mother,child
		if not mother:
			data['msg'] = "PERSON_NOT_FOUND"
			return data
		elif mother[2]!="Female":
			data['msg'] = "CHILD_ADDITION_FAILED"#"MOTHER_NOT_FEMALE"
			return data
		if child:
			data['msg'] = "CHILD_ALREADY_IN_TREE"
			return data
		data['success'] = True
		data['mother'] = mother
		data['child'] = child
		return data

	def validate_add_spouse(self,wife_name,husband_name):
		"""
		Rule 1: Wife should be female if already in tree
		Rule 2: Husband should be male if already in tree
		Rule 3: Neither of wife or husband should already have a spouse relationship in tree
		"""
		data = {'success':False}
		wife = self.get_person(wife_name)
		husband = self.get_person(husband_name)
		if wife:
			#Rule 1
			if wife[2]!="Female":
				data['msg'] = "WIFE_NOT_FEMALE"
				return data
			#Rule 3
			conflict = filter(lambda x:x[0]=="husband" and (x[1]==wife[0]),globals.relationship_list)
			if conflict:
				data['msg'] = "WIFE_MARRIED_TO_OTHER"
				return data
		if husband:
			#Rule 2
			if husband[2]!="Male":
				data['msg'] = "HUSBAND_NOT_MALE"
				return data
			#Rule 3
			conflict = filter(lambda x:x[0]=="husband" and (x[2]==husband[0]),globals.relationship_list)
			if conflict:
				data['msg'] = "HUSBAND_MARRIED_TO_OTHER"
				return data

		data['success']=True
		data['wife']=wife
		data['husband']=husband
		return data 

	def add_child(self,mother_name,child_name,child_gender):
		data = self.validate_add_child(mother_name,child_name,child_gender)
		print "aa", data
		if data['success']:
			mother = data.get('mother',None)
			child = data.get('child',None)
			if not child:
				child = self.add_person(child_name,child_gender)
			rel = "daughter" if child_gender=="Female" else "son"
			globals.relationship_list.append([rel,mother[0],child[0]])
			data['msg'] = "CHILD_ADDITION_SUCCEEDED"
		return data

	def add_spouse(self,wife_name,husband_name):
		data = self.validate_add_spouse(wife_name,husband_name)
		if data['success']:
			wife = data.get('wife',None)
			if not wife:
				wife = self.add_person(wife_name,"Female")
			husband = data.get('husband',None)
			if not husband:
				husband = self.add_person(husband_name,"Male")
			globals.relationship_list.append(["husband",wife[0],husband[0]])
			data['msg'] = "SPOUSE_ADDED_SUCCESSFULLY"
		return data