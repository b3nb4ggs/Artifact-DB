import sqlite3

c = sqlite3.connect('Database.db')

def create_tables():

	c.execute('''CREATE TABLE Artifact
(ID int NOT NULL UNIQUE,
 Type varchar(30),
 Size numeric (2,1) DEFAULT(1),
 Characteristic varchar(30) DEFAULT('NA'),
 Value int default(0),
 pid int,
 cid int,
 clid int,
 PRIMARY KEY(ID)
 FOREIGN KEY(pid) REFERENCES Place(id)
 FOREIGN KEY(cid) REFERENCES Certifier(id)
 FOREIGN KEY(clid) REFERENCES Culture(id)
 
 
	); 
	''')
	c.execute('''CREATE TABLE Place
	(
	id int NOT NULL UNIQUE,
  Price int DEFAULT(0),
  Found int DEFAULT(0),
  Date int,
  Location varchar(30),
  PRIMARY KEY(id)
	);
	''')

	c.execute('''CREATE TABLE Certifier (
	id int NOT NULL UNIQUE,
	Date int DEFAULT(0),
	Organization varchar(30) DEFAULT('n/a'),
	Name varchar(30) DEFAULT('n/a'),
	Authenticity int DEFAULT(1),
	PRIMARY KEY(id)
	); 
	''')

	c.execute('''CREATE TABLE Culture (
	id int NOT NULL UNIQUE, 
 	Name varchar(30),
 	Era varchar(30),
 	Location varchar(30),
 	PRIMARY KEY(id) 
	);
	''')
def list_certified():
	data = c.execute('''SELECT Type, Size, Name, Organization 
	FROM Artifact, Certifier
	WHERE Artifact.cid = Certifier.id  AND Certifier.Authenticity=1
	''')
	for line in data:
		print(line)
def value_over(n):

	data = c.execute("SELECT Type, Size, Value FROM Artifact where Value>?", (n,))
	for line in data:
		print(line)
def total_value():
	data = c.execute("SELECT SUM(value) FROM Artifact")
	for line in data:
		output=line
	print("$",line[0])
def who_cert():
	data =c.execute("SELECT Name, Organization FROM Certifier, Artifact WHERE Certifier.id=Artifact.cid AND Artifact.value> 1000")
	for line in data:
		print(line)
def best_craftsman():
	data = c.execute("SELECT Name, Era, Location FROM Culture, Artifact "
									 "WHERE Artifact.value > 100 "
									 "order by Artifact.Value desc limit 5")
	for line in data:
		print(line)
def bought_artifacts():
	data =  c.execute("SELECT Type, Value "
										"FROM Artifact, Place "
										"WHERE Artifact.pid = Place.id AND Place.id IN "
										"(SELECT id "
										"FROM Place "
										"WHERE Place.Found = 0) ")
	for line in data:
		print(line)
def correlate_area():
	data = c.execute("SELECT Name "
										"FROM Culture "
										"INNER JOIN Place on Place.Location=Culture.Location "
										"WHERE Place.Found=1 ")
	for line in data:
		print(line)
def bargain_shopper():
	data = c.execute("SELECT Type, Value, Artifact.ID "
										"FROM Artifact "
										"INNER JOIN Place ON Artifact.pid = Place.id "
										"WHERE Place.Price <= Artifact.Value AND Place.Found = 0 ")
	for line in data:
		print(line)
def biggest_fan():
	data = c.execute("SELECT Name, COUNT(Name) AS value_occurrence "
										"FROM Culture "
										"GROUP BY Name "
										"ORDER BY value_occurrence DESC "
										"LIMIT 1 ")
	for line in data:
		print(line)
def fertile_ground():
	data = c.execute("SELECT Location, COUNT(*) as count "
										"FROM Place "
										"GROUP BY Location "
										"ORDER BY count DESC ")
	for line in data:
		print(line)
def counterfit():
	data = c.execute("SELECT Type, Size "
						"FROM Artifact, Certifier "
						"WHERE Artifact.cid = Certifier.id and Certifier.Authenticity=0 ")
	for line in data:
		print(line)
def insert():
	data=c.execute("SELECT MAX(ID) FROM Artifact")
	for line in data:
		id=line
	id=id[0]+1
	type = input("What type of artifact?")
	size = input("What size is the artifact?")
	charicter = input("List defining characteristics")
	value = input("List value of artifact (default 0)")
	c.execute("INSERT INTO Artifact (ID,Type, Size, Characteristic, Value)VALUES (?,?,?,?,?);", (id,type, size, charicter,value,))
def delete():
	data = c.execute("SELECT * FROM Artifact")
	for line in data:
		print(line)
	choice = input("Which item do you want to delete?")
	c.execute("DELETE FROM Artifact WHERE ID=(?)",(choice,))


choice = 0

while(True):
	print("\n\nHello, welcome to my database project\n"
				"Select from the following queries(Enter a number and press enter)\n"
				"Press 0 to exit\n"
				"1) Find all certified Artifacts in the collection\n"
				"2) Find artifacts worth more than a number you input\n"
				"3) List the current value of the entire collection\n"
				"4) Find your most trusted certification specialist\n"
				"5) Find the culture of you most valuable artifacts\n"
				"6) Find artifacts that were purchased instead of found\n"
				"7) List cultures of artifacts that were found in their indigenous area.\n"
				"8) Find artifacts that were appraise for more than what they were bought for\n"
				"9) Find what culture I have the most artifacts from\n"
				"10) Find where we found the most artifacts\n"
				"11) List confirmed counterfit artifacts\n"
				"12) To add artifact\n"
				"13) To delete an artifact\n")
	choice = input()
	if int(choice) == 0:
		exit()
	elif int(choice) == 1:
		list_certified()
	elif int(choice) == 2:
		value=0
		value = input("Please list a value")
		value_over(value)
	elif int(choice) == 3:
		total_value()
	elif int(choice) == 4:
		who_cert()
	elif int(choice) == 5:
		best_craftsman()
	elif int(choice) == 6:
		bought_artifacts()
	elif int(choice) == 7:
		correlate_area()
	elif int(choice) == 8:
		bargain_shopper()
	elif int(choice) == 9:
		biggest_fan()
	elif int(choice) == 10:
		fertile_ground()
	elif int(choice) == 11:
		counterfit()
	elif int(choice) == 12:
		insert()
	elif int(choice) == 13:
		delete()
	else:
		print("I don't know how to program")