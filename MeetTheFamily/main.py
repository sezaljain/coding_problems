import csv,sys
from get_relationship import GetRelationship
from add_relationship import AddRelationship
from global_var import *


def read_csv(filepath):
	data = []
	with open(filepath) as f:
		reader=csv.reader(f)
		# next(reader, None)
		for row in reader:
			if row:
				data.append(row)
	return data


def request_tree(request_type,data):
	print person_list
	a = AddRelationship(person_list,relationship_list)
	g = GetRelationship(person_list,relationship_list,order3_relationship_definition)
	output={'msg':''}
	if request_type=='ADD_SPOUSE':
		output = a.add_spouse(data[0],data[1])
	elif request_type=='ADD_CHILD':
		output = a.add_child(data[0],data[1],data[2])
	elif request_type=='GET_RELATIONSHIP':
		output = g.get_custom_relationship_wrapper(data[0],data[1])

	return output['msg']


def main():
	initialize_global()
	print ("Welcome to Shan family")
	input_file = sys.argv[1]
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


if __name__ == '__main__':
	main()

