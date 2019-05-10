The script has been written in python 2.7
Important files:
	relationship.py  --> python script
	initial.txt --> commands to setup tree given in assignment
	order3_relationships.csv  --> list of 'Relationships to handle' and their definition. Can add any more definitions here. Use . and + operators to define relationships. Usage of . chains relationships eg brother.wife means wife of brother. Usage of + denotes a union of relationships eg. brother+sister means either of them
	input.txt --> Any additional commands to be run on the tree after it has been initialized

List of commands
ADD_CHILD <mother_name> <child_name> <child_gender>
ADD_SPOUSE <wife_name> <husband_name>
GET_RELATIONSHIP <person_name> <order3_relationship_name>

Please run the program using the command:
python main.py input.txt


Testing:
pytest test_family_tree.py