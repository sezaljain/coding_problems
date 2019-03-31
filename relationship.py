import csv,uuid,re,sys

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
	uid = uuid.uuid4().hex[:6]
	conflict = filter(lambda x:x[0]==uid,person_list)
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
		matching_people = filter(lambda x:x[1]==person_name,person_list)
		assert len(matching_people)<=1,"Should not be more than one person with the same name"
		if matching_people:
			return matching_people[0]
			# assert(person[2]==person_gender,"Person exists with another gender")
		return None

	def validate_add_person(self,person_name,person_gender):
		# Rule 1:Person should have a name not already in tree
		return True, "go ahead"

	def add_person(self,person_name,person_gender):
		# success,msg = self.validate_add_person()
		p = [calc_uid(),person_name,person_gender]
		person_list.append(p)
		return p

	def validate_add_child(self,mother_name,child_name,child_gender):
		# Rule 1: Mother should already exist in the tree
		# Rule 2: Mother should be female
		# Rule 3: child name should not be in tree already (tree has unique names)
		# Rule 4: the same relationship should not exist already
		data = {'success':False}
		mother = self.get_person(mother_name)
		child = self.get_person(child_name)
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
		# Rule 1: Wife should be female if already in tree
		# Rule 2: Husband should be male if already in tree
		# Rule 3: Neither of wife or husband should already have a spouse relationship in tree
		data = {'success':False}
		wife = self.get_person(wife_name)
		husband = self.get_person(husband_name)
		if wife:
			#Rule 1
			if wife[2]!="Female":
				data['msg'] = "WIFE_NOT_FEMALE"
				return data
			#Rule 3
			conflict = filter(lambda x:x[0]=="husband" and (x[1]==wife[0]),relationship_list)
			if conflict:
				data['msg'] = "WIFE_MARRIED_TO_OTHER"
				return data
		if husband:
			#Rule 2
			if husband[2]!="Male":
				data['msg'] = "HUSBAND_NOT_MALE"
				return data
			#Rule 3
			conflict = filter(lambda x:x[0]=="husband" and (x[2]==husband[0]),relationship_list)
			if conflict:
				data['msg'] = "HUSBAND_MARRIED_TO_OTHER"
				return data

		data['success']=True
		data['wife']=wife
		data['husband']=husband
		return data 

	def add_child(self,mother_name,child_name,child_gender):
		data = self.validate_add_child(mother_name,child_name,child_gender)
		if data['success']:
			mother = data.get('mother',None)
			child = data.get('child',None)
			if not child:
				child = self.add_person(child_name,child_gender)
			rel = "daughter" if child_gender=="Female" else "son"
			# print mother,child
			relationship_list.append([rel,mother[0],child[0]])
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
			relationship_list.append(["husband",wife[0],husband[0]])
			data['msg'] = "SPOUSE_ADDED_SUCCESSFULLY"
		return data


class GetRelationship:
	""" This is a class instead of a function to make it chainable
	ORDER 0 relationships -- husband, daughter and son. These go into the data table
	ORDER 1 relationship -- listed in relation_to_function. These are used to describe any possible relationship in a family tree
	ORDER 2 relationship -- any possible combination user can come up using order 1 relationships. examples in custom_relationship_options

	All functions accept a list of people as input. This is so that the function can be chained
	for eg. for brother in law  -- sister.husband
		if there are multiple sisters .. the function will work on all of them together to get a list of husbands

	"""
	def __repr__(self):
		return "GetRelationship(person,order3_relationship)"
		
	def __init__(self,*args,**kwargs):
		# self.relationship_of = initial_person_list

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
			if person in output_person_list:
				output_person_list.remove(person)
			final_output_person_list = final_output_person_list+output_person_list

		return final_output_person_list

	def get_brother(self,input_people):
		return self.get_sibling(input_people,'Male')

	def get_sister(self,input_people):
		return self.get_sibling(input_people,'Female')

	@staticmethod
	def validate_get_relationship(person_name,custom_relationship):
		#Step1: lookup relationship in relationship_options
		data={'success':False}

		rel = order3_relationship_definition.get(custom_relationship,None)
		if not rel:
			data['msg'] = "RELATIONSHIP_NOT_FOUND"
			return data
		data['relationship_def'] = rel

		a = AddRelationship()
		person = a.get_person(person_name)
		if not person:
			data['msg'] = "PERSON_NOT_FOUND"
			return data
		data['person']=person

		data['success']=True
		return data

	def get_custom_relationship(self,input_people,custom_relationship):
		""" input_people is a list of 'person' (subset of person_list)
			custom_relationship is the definition of any order3 relationship eg. husband.brother
		"""
		
		custom_relationship = re.sub(r"[^a-zA-Z.+]", '', custom_relationship)
		output_people =[]
		for custom_relationship_part in custom_relationship.split('+'):
			input_people_ = input_people   #relationships separated by '+'' start by being chained to original input_people
			for order1_rel in custom_relationship_part.split('.'):
				output_people_ = self.relation_to_function[order1_rel](input_people_)
				input_people_= output_people_
			output_people = output_people+output_people_
		 

		##preparing output msg
		data = {'msg':''}
		if output_people:
			data['msg'] = ' '.join(map(lambda x:x[1],output_people))
		else:
			data['msg'] = "NO_RELATIONSHIPS_FOUND"
		return data

	def get_custom_relationship_wrapper(self,person_name,custom_relationship_name):
		data = self.validate_get_relationship(person_name,custom_relationship_name)
		if data['success']:
			data = self.get_custom_relationship([data['person']],data['relationship_def'])
		return data





def request_tree(request_type,data):
	a = AddRelationship()
	g = GetRelationship()
	output={'msg':''}
	if request_type=='ADD_SPOUSE':
		output = a.add_spouse(data[0],data[1])
	elif request_type=='ADD_CHILD':
		output = a.add_child(data[0],data[1],data[2])
	elif request_type=='GET_RELATIONSHIP':
		output = g.get_custom_relationship_wrapper(data[0],data[1])

	return output['msg']


def main():
	print ("Welcome to Shan family")
	input_file = sys.argv[1]
	global person_list
	global relationship_list
	global order3_relationship_definition
	person_list = []
	relationship_list = []
	order3_relationship_definition = {}

	fp = open('order3_relationships.txt')
	reader = csv.DictReader(filter(lambda row: row[0]!='#', fp))
	for row in reader:
		order3_relationship_definition[row['Name']]=row['Definition'].strip()
	fp = open('initial.txt')
	reader = csv.DictReader(filter(lambda row: row[0]!='#', fp),delimiter=" ")
	for row in reader:
		out = request_tree(row['type'],row[None])
		# print out
	print "Initial Tree setup done"
	print "-----------------------"

	# ##Any new commands can go in the input.txt file
	fp = open(input_file)
	reader = csv.reader(fp,delimiter = " ")
	for row in reader:
		request_type = row.pop(0)
		out = request_tree(request_type,row)
		print out

	# print person_list
	# print relationship_list

if __name__ == '__main__':
	main()

