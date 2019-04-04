import re
from add_relationship import AddRelationship
import globals



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

		"""
		This is a list of ORDER 1 relationships based on which higher order custom relationships can be formed
		eg. mother in law -- "wife.mother+husband.mother"
		This list mostly exists to make it easy to add complicated relationshps
		and to be able to add relationships like brother/sister 
		(mother.son or mother.daughter will include the original person as well)
		"""
		self.relation_to_function ={
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
			lambda x:filter(lambda y:y[0]==x[relation_id],globals.person_list)[0],  #extracting person from relationship
			filter(#extracting the desired relationship for people in relationship_of
					lambda x:x[0]==relationship_type and x[relation_of_id] in [y[0] for y in input_people],
					globals.relationship_list
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

		rel = globals.order3_relationship_definition.get(custom_relationship,None)
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



