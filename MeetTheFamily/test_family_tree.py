import pytest

import csv,sys
from get_relationship import GetRelationship
from add_relationship import AddRelationship

import globals

def test_basic_rel():
	globals.initialize()
	fp = open('order3_relationships.txt')
	reader = csv.DictReader(filter(lambda row: row[0]!='#', fp))
	for row in reader:
		globals.order3_relationship_definition[row['Name']]=row['Definition'].strip()

	test_family_arr = [
	["ADD_SPOUSE","Lyarra","Rickard"],
	["ADD_CHILD","Lyarra","Ned","Male"],
	["ADD_CHILD","Lyarra","Lyanna","Female"],
	["ADD_SPOUSE", "Catelyn","Ned"],
	["ADD_CHILD", "Catelyn", "Arya", "Female"],
	["ADD_CHILD", "Catelyn", "Sansa", "Female"],
	["ADD_SPOUSE","Lyanna","Rhaegar"],
	["ADD_CHILD","Lyanna","Jon","Male"],
	]


	a = AddRelationship()

	print "Adding members in the tree"
	for row in test_family_arr:
		if row[0]=='ADD_SPOUSE':
			output = a.add_spouse(row[1],row[2])
		elif row[0]=='ADD_CHILD':
			output = a.add_child(row[1],row[2],row[3])
		print output

	g = GetRelationship()
	output = g.get_custom_relationship_wrapper("Arya","Sister")
	assert (output["msg"]=="Sansa"),"Sansa should be Arya's sister"
	output = g.get_custom_relationship_wrapper("Sansa","Sister")
	assert (output["msg"]=="Arya"),"Arya should be Sansa's sister"

	output = g.get_custom_relationship_wrapper("Rickard","Wife")
	assert (output["msg"]=="Lyarra"),"Lyarra Should be wife"


	output = g.get_custom_relationship_wrapper("Jon","Maternal-Uncle")
	assert (output["msg"]=="Ned"),"Ned is Jon's uncle"
	output = g.get_custom_relationship_wrapper("Ned","Nephew")
	assert (output["msg"]=="Jon"),"Ned is Jon's uncle"

