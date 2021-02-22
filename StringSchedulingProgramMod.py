#*********************************************
# * OPL 12.9.0.0 Model
# *********************************************

using CP;
 
# The model will only consider the first certain number of children  

int NumberOfChildrenToConsider = ...;

# Parameters to control CP engine

execute {
	# cp.param.randomseed = 1024;
	cp.param.OptimalityTolerance = 1.0;
	cp.param.RelativeOptimalityTolerance = 1.0;
	cp.param.timelimit = 7200;
	# cp.param.workmem = 1024;
}



# Data type for storing a range

tuple Pair {
	int lower;
	int upper;
};



# Different TypeOfClasss of classes

{string} RequiredClasses = { "Master", "Group" };
{string} ElectiveClasses = { "Music and Movement", "Art", "Fiddling", "Improvisation", 
							 "Compose and Compute", "Musicianship", "Dalcroze" };
{string} OptionalRequiredClasses = { "Orchestra" };
{string} AllNonTrivialClasses = RequiredClasses union ElectiveClasses union OptionalRequiredClasses;
{string} AllClasses = { "None" } union AllNonTrivialClasses;
{string} InstrumentDependentClasses = { "Master", "Group", "Fiddling" };
{string} AgeBasedClasses = { "Musicianship",  "Dalcroze" };
{string} BookBasedClasses = { "Master", "Group" };
{string} BatchBasedClasses = { "Orchestra" };
{string} OneInstrumentClasses = { "Group" };
{string} LargeRoomClasses = { "Group", "Fiddling", "Orchestra", "Music and Movement" };



{string} ExceptionInstruments = { "Viola" };


{string} ClassesWithRelaxedBookConstraints = { "Group" };
{string} ClassesWithRelaxedAgeConstraints = { };
int OptionalRequiredClassesToSchedule[OptionalRequiredClasses] = [1];

# Schedule children with only specified batch numbers

{int} BatchNumbersToSchedule = { 1, 2 }; 

# Classes for which special processing is required

int NoClass = ord(AllClasses, "None");
int MasterClass = ord(AllClasses, "Master");
int ComputeAndComposeClass = ord(AllClasses, "Compose and Compute" );
int GroupClass = ord(AllClasses, "Group");
int FiddlingClass = ord(AllClasses, "Fiddling");


# Maximum and minimum capacities for each type of class

int DefaultClassCapacities[AllClasses] = [ 0, 0, 0, 10, 12, 15, 15, 10, 12, 12, 50 ];

int MinimumClassSizes[AllClasses] = [ 0, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1 ];

# Number of concurrent classes of each type

int NumberOfConcurrentClasses[AllClasses] = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ];

int NumberOfLargeRoomsAvailable = 4;



# Total number of class types

int NumberOfClassTypes = card(AllClasses);
range RangeOfClassTypes = 0..NumberOfClassTypes - 1;


# Number of slots

int NumberOfClassesInADay = 5;
range Slots = 1..NumberOfClassesInADay;


# Different types of instruments

{string} Instruments = { "Violin", "Viola", "Cello" };

tuple InstrumentPair {
	string this;
	string that;
};

{InstrumentPair} ForbiddenPairOfInstrumentsForFiddling = { 
   <"Violin", "Cello">, 
   <"Viola", "Cello"> 
};


# Different book categories for each instrument for which classes can be scheduled together


{Pair} BookCategories[Instruments] = [ 
	{ <0,0>, <1,1>, <2,2>, <3,3>, <4,4>, <5,5>, <6,6>, <7,7>, <8,8>, <9,9>, <10,10>, <11,11> },	
    { <0,0>, <1,1>, <2,2>, <3,3>, <4,4>, <5,5>, <6,6>, <7,7>, <8,8>, <9,9>, <10,10>, <11,11> }, 
    { <0,0>, <1,1>, <2,2>, <3,3>, <4,4>, <5,5>, <6,6>, <7,7>, <8,8>, <9,9>, <10,10>, <11,11> }  
];

# Number of book categories for each instrument

int NumberOfBookCategories[Instruments] =  [
	card(BookCategories["Violin"]),
	card(BookCategories["Viola"]),
	card(BookCategories["Cello"])
];



# Maximum number of book categories for any instrument

int MaximumNumberOfBookCategories = (max(i in Instruments) NumberOfBookCategories[i]);
range RangeOfBookCategories = 0..MaximumNumberOfBookCategories-1;

# Book categories for each instrument as a set

{int} SetOfBookCategories[Instruments] = [
	asSet(0..NumberOfBookCategories["Violin"]-1),
	asSet(0..NumberOfBookCategories["Viola"]-1),
	asSet(0..NumberOfBookCategories["Cello"]-1)
]; 

# Control the variation in book levels and ages of children in book based classes

int BookVariance[Instruments][RangeOfBookCategories] = [ 
	[ 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1 ],
	[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
	[ 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1 ]  
];

int BookRelaxationLocal[Instruments][RangeOfBookCategories] = [ 
	[ 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
	[ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 ], 
	[ 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
];
int BookRelaxationGlobal = 1;


int BookRelaxationLocalFlag = 1;
int BookRelaxationGlobalFlag = 0;

int MaximumBookVariance[i in Instruments][b in RangeOfBookCategories][c in BookBasedClasses] =
	BookVariance[i][b] + 
	(c in ClassesWithRelaxedBookConstraints) * BookRelaxationLocalFlag * BookRelaxationLocal[i][b] +
	(c in ClassesWithRelaxedBookConstraints) * BookRelaxationGlobalFlag * BookRelaxationGlobal; 
	  



# Different age categories

{Pair} AgeCategories = { <0,0>,   <1,1>,   <2,2>,   <3,3>,   <4,4>, 
						 <5,5>,   <6,6>,   <7,7>,   <8,8>,   <9,9>, 
						 <10,10>, <11,11>, <12,12>, <13,13>, <14,14>, 
						 <15,15>, <16,16>, <17,17>, <18,100> };
     

int NumberOfAgeCategories = card(AgeCategories);
range RangeOfAgeCategories = 0..NumberOfAgeCategories-1;

int AgeVariance[RangeOfAgeCategories] = [ 
	2, 2, 2, 2, 2, 
	2, 3, 3, 3, 3, 
	3, 3, 4, 4, 4, 
	5, 5, 5, 100 
];

int AgeRelaxationLocal[RangeOfAgeCategories] = [ 
	0, 0, 0, 0, 0, 
	0, 0, 0, 1, 1, 
	1, 1, 2, 2, 2, 
	2, 2, 2, 100
];



int AgeRelaxationGlobal = 1;

int AgeRelaxationLocalFlag = 1;
int AgeRelaxationGlobalFlag = 0;

int MaximumAgeVariance[a in RangeOfAgeCategories][c in AgeBasedClasses] =
	AgeVariance[a] + 
	(c in ClassesWithRelaxedAgeConstraints) * AgeRelaxationLocalFlag * AgeRelaxationLocal[a] +
	(c in ClassesWithRelaxedAgeConstraints) * AgeRelaxationGlobalFlag * AgeRelaxationGlobal; 
	
	
	
# Constraints on siblings taking classes concurrently

int MaximumNumberOfSiblingsInMasterClassesPerSlot = 2;

# Capacities for Masterclass for each combination of instrument and book category 

int CapacitiesForMasterclassBasedOnBookCategory[Instruments][RangeOfBookCategories] = [
	[ 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2 ],
	[ 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2 ],
	[ 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2 ]
];

int CapacitiesForComposeAndComputeClass[Slots] = [ 10, 4, 4, 5, 10 ];

int CapacitiesForGroupClass[Instruments] = [ 30, 30, 10 ];



# Some elective classes require children to be at a certain book level

{int} BooksEligibleForElectiveClasses[ElectiveClasses][Instruments] = [
   [asSet(0..11), asSet(0..11), asSet(0..11)],
   [asSet(1..11), asSet(1..11), asSet(1..11)],
   [asSet(2..11), asSet(2..11), asSet(3..11)],
   [asSet(2..11), asSet(2..11), asSet(2..11)],
   [asSet(3..11), asSet(3..11), asSet(3..11)],
   [asSet(1..11), asSet(1..11), asSet(1..11)],
   [asSet(0..11), asSet(0..11), asSet(0..11)]
];
   
   
# Some elective classes require children to be of a certain age
 					 
{int} AgesEligibleForElectiveClasses[ElectiveClasses][Instruments] = [
   [asSet(0..6), asSet(0..6), asSet(0..6)],
   [asSet(0..100), asSet(0..100), asSet(0..100)],
   [asSet(0..100), asSet(0..100), asSet(0..100)],
   [asSet(0..100), asSet(0..100), asSet(0..100)],
   [asSet(10..100), asSet(10..100), asSet(10..100)],
   [asSet(0..100), asSet(0..100), asSet(0..100)],
   [asSet(0..100), asSet(0..100), asSet(0..100)]
];



# Young children should only be scheduled for morning slots

{int} SlotsForPreTwinklers = { 1, 2, 3 };



#* USER GIVEN MODEL DATA *#

# Child specific data



# Data type to specify the set of attributes for a child

tuple ChildAttributes {
	key string name;
	string lastName;
	string firstName;
	int age;
	string instrument;
 	int book;
	string teacher;
	int numberOfElectiveClasses;
	int enrolled[OptionalRequiredClasses];
	int rank[ElectiveClasses];
 	int batch;
};


{ChildAttributes} ChildrenDataSet = ...;


{string} DontScheduleForInstruments = ...;
{string} DontScheduleForChildren = ...;

{ChildAttributes} ChildrenDataSetPruned = { e | e in ChildrenDataSet : e.instrument not in DontScheduleForInstruments && e.name not in DontScheduleForChildren };

int NumberOfChildren = card(ChildrenDataSetPruned);
range Children = 0..minl(NumberOfChildren, NumberOfChildrenToConsider)-1;

# Attributes for all children

ChildAttributes ChildrenData[c in Children] =  item(ChildrenDataSetPruned, c);

{string} NamesOfChildren = { c.name | c in ChildrenDataSetPruned : ord(ChildrenDataSetPruned, c) in Children };




int MaximumBatchNumber = max(c in Children) ChildrenData[c].batch;
range RangeOfBatchNumbers = 0..MaximumBatchNumber;

# Data type to specify siblings in a family

tuple FamilySet {
	{string} siblings;
};

{FamilySet} SiblingsDataSet = ...;

int NumberOfSiblingsFamilies = card(SiblingsDataSet);
range SiblingsFamilies = 0..NumberOfSiblingsFamilies-1;

{int} SiblingsData[f in SiblingsFamilies] = { ord(NamesOfChildren, c)  | c in item(SiblingsDataSet, f).siblings : c in NamesOfChildren };




 
# Teacher specific data

# Data type to specify the set of attributes for a teacher

# Attributes for all teachers

tuple TeacherAttributes {
	key string name;
	string lastName;
	string firstName;
	{string} proficiences;
	{string} instruments;
	int minimumBookLevel[Instruments];
	int maximumBookLevel[Instruments];
	Pair ageRange;
	int availability[Slots];
	int numberOfClasses;
	int accompanist;
};


{TeacherAttributes} TeachersDataSet = ...;

int NumberOfTeachers = card(TeachersDataSet);
range Teachers = 0..NumberOfTeachers-1;

{string} NamesOfTeachers = { t.name | t in TeachersDataSet };

# {string} NamesOfTeachers = { t.name | t in TeachersDataSet };
TeacherAttributes TeachersData[t in Teachers] = item(TeachersDataSet, t);


tuple RequiredClass {
	string name;
	string type;
	int value;
} 

{RequiredClass} TeachersRequiredClasses = ...;

tuple ClassPreference {
	string child;
	string teacher;
};

{ClassPreference} DoNotWantAsMasterClassTeacherSet = ...;


tuple TeacherSet {
	{string} teachers;
};

{TeacherSet} ForbiddenPrivateTeacherMasterClassTeacherCombinations = ...;


{string} TeachersNotRequiringAccompanist = ...; 

#* CONVENIENCE EXPRESSIONS *#

# int NumberOfStudents[i in Instruments] = card({c | c in Children: ChildrenData[c].instrument == i});


# Find the book category of each child
int ChildrenBookCategory[c in Children] = (max(e in BookCategories[ChildrenData[c].instrument]) 
										  	((ChildrenData[c].book >= e.lower) && (ChildrenData[c].book <= e.upper)) * 
											ord(BookCategories[ChildrenData[c].instrument], e)); 



# Find the age catgory of each child
int ChildrenAgeCategory[c in Children] = (max(e in AgeCategories) 
										 	(ChildrenData[c].age >= e.lower && ChildrenData[c].age <= e.upper) * ord(AgeCategories, e));
											


# Find the batch number of each child
int ChildrenBatchNumber[c in Children] = ChildrenData[c].batch;


# Find the maximum rank value of elective classes for each child 
int MaximumRankValuePerChild[c in Children] = max(e in ElectiveClasses) ChildrenData[c].rank[e];

# #*
# # Adjust the rank values of elective classes so that children with book level below three are not assigned composition class
# int AdjustedRanksOfElectiveClasses[c in Children][e in ElectiveClasses] = 
# 	(ord(AllClasses, e) == ComputeAndComposeClass) * (ChildrenData[c].book < MinimumBookLevelForComposeAndComputeClass) * (MaximumRankValuePerChild[c]+1) + 
# 	(ord(AllClasses, e) == ComputeAndComposeClass) * (ChildrenData[c].book >= MinimumBookLevelForComposeAndComputeClass) * ChildrenData[c].rank[e] + 
# 	(ord(AllClasses, e) == MusicAndMovementClass) * (ChildrenData[c].age > MaximumAgeForMusicAndMovementClass) * (MaximumRankValuePerChild[c]+1) + 
# 	(ord(AllClasses, e) == MusicAndMovementClass) * (ChildrenData[c].age <= MaximumAgeForMusicAndMovementClass) * ChildrenData[c].rank[e] + 
# 	(ord(AllClasses, e) == ImprovisationClass) * (ChildrenData[c].book < MinimumBookLevelForImprovisationClass) * (MaximumRankValuePerChild[c]+1) + 
# 	(ord(AllClasses, e) == ImprovisationClass) * (ChildrenData[c].book >= MinimumBookLevelForImprovisationClass) * ChildrenData[c].rank[e] + 
# 	(e not in ElectivesWithSpecialConstraints) * ChildrenData[c].rank[e];
# *#

int AdjustedRanksOfElectiveClasses[c in Children][e in ElectiveClasses] = 
	(((ChildrenData[c].book in BooksEligibleForElectiveClasses[e][ChildrenData[c].instrument]) && 
	  (ChildrenData[c].age in AgesEligibleForElectiveClasses[e][ChildrenData[c].instrument])) * ChildrenData[c].rank[e]) + 
	(((ChildrenData[c].book not in BooksEligibleForElectiveClasses[e][ChildrenData[c].instrument]) || 
	  (ChildrenData[c].age not in AgesEligibleForElectiveClasses[e][ChildrenData[c].instrument])) * (MaximumRankValuePerChild[c]+1));

# Find the number of elective classes that each child has to take
# int NumberOfElectiveClasses[c in Children] = ChildrenData[c].numberOfClasses - card(RequiredClasses) - (sum(o in OptionalRequiredClasses) ChildrenData[c].enrolled[o]);

# Express the rank of elective classes for each child as a set
sorted {Pair} RanksOfElectiveClassesAsSet[c in Children] = 
	{ <AdjustedRanksOfElectiveClasses[c][e], ord(ElectiveClasses, e)> | e in ElectiveClasses };

# Find the lower bound on the rank of elective classes for each child 
int LowerBoundsOnRank[c in Children] = item(RanksOfElectiveClassesAsSet[c], ChildrenData[c].numberOfElectiveClasses-1).lower;

# Find the upper bound on the rank of elective classes for each child 
int UpperBoundsOnRank[c in Children] = item(RanksOfElectiveClassesAsSet[c], card(ElectiveClasses)-1).lower;

# Find the upper bound on the value of the objective function
int OFUpperBoundValue = max(c in Children) (UpperBoundsOnRank[c] - LowerBoundsOnRank[c]);

# #***********************************************************************************************************#

# #* ASSERTIONS *#

# #* Perform a limited check to ensure that a feasible solution is possible *#


# ensure that, for every non trivia class, there is at least one teacher who can teach the class

assert
	forall(a in AllNonTrivialClasses) 
		(sum(t in Teachers) (a in TeachersData[t].proficiences)) >= 1; 




execute {
	
    var quote = "\"";

	for(var a in AgeBasedClasses) {
		var found = false;	
		for(var c in AllClasses) {
			if (a == c) {
				found = true;			
			}				
		}	
	
		
		if (!found) {
			writeln(quote + a + quote + " not found in set of all classes!");
			assert (1 == 0);
		}				
	}
}

# #*
# 	ensure that, for every child, there is at least one teacher who can teach that child's instrument at that child's book and age levels
# *#
assert
	forall(c in Children) 
		(sum(t in Teachers) 
			(ChildrenData[c].instrument in TeachersData[t].instruments) *
			(ChildrenData[c].book >= TeachersData[t].minimumBookLevel[ChildrenData[c].instrument]) * 
			(ChildrenData[c].book <= TeachersData[t].maximumBookLevel[ChildrenData[c].instrument]) *
			(ChildrenData[c].age >= TeachersData[t].ageRange.lower) *
			(ChildrenData[c].age <= TeachersData[t].ageRange.upper)) >= 1;

# ensure that group based classes are only taken by children at a certain book level or higher
assert
	(sum(c in Children)
		(ChildrenData[c].book < 1) * (ChildrenData[c].batch > 0)) <= 0;
	  		
	  		 
# #***********************************************************************************************************#
	
# #* DECISION VARIABLES *#

# # Independent decision variables

# dvar int SchedulingInstance[Children][Teachers][Slots] in 0..1;

# dvar int TypeOfClass[Teachers][Slots] in 0..NumberOfClassTypes-1;

# # Dependent decision variables

# #*

dvar int ClassesInstrumentPresent[Teachers][Slots][Instruments] in 0..1;

dvar int ClassesBookCategory[Teachers][Slots][Instruments] in 0..MaximumNumberOfBookCategories-1;

dvar int ClassesAgeCategory[Teachers][Slots] in RangeOfAgeCategories;

dvar int ClassesBatchNumber[Teachers][Slots] in RangeOfBatchNumbers;


dvar int HighestRankedPerChild[Children] in 0..OFUpperBoundValue;

*#




dexpr int ClassesInstrumentPresent[t in Teachers][s in Slots][i in Instruments] =
			(count(all(c in Children : ChildrenData[c].instrument == i) SchedulingInstance[c][t][s], 1) > 0);

			
dexpr int ClassesBookCategory[t in Teachers][s in Slots][i in Instruments] =
			(max(c in Children) (SchedulingInstance[c][t][s] == 1) * (ChildrenData[c].instrument == i) * ChildrenBookCategory[c]);


dexpr int ClassesAgeCategory[t in Teachers][s in Slots] =
			(max(c in Children) (SchedulingInstance[c][t][s] == 1) * ChildrenAgeCategory[c]);
			
			
dexpr int ClassesBatchNumber[t in Teachers][s in Slots] =
			(max(c in Children, b in BatchBasedClasses) 
				(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) * ChildrenBatchNumber[c]);							


dexpr int HighestRankedPerChild[c in Children] = 
	(max(t in Teachers, s in Slots, e in ElectiveClasses) 
		(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, e)) * 
	 	 AdjustedRanksOfElectiveClasses[c][e]) - LowerBoundsOnRank[c];

#*
dexpr int NumberOfRelaxations =
	(sum(c in Children : ChildrenData[c].instrument not in ExceptionInstruments, t in Teachers, s in Slots, b in BookBasedClasses)	
		(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) * 
		(ClassesBookCategory[t][s][ChildrenData[c].instrument] - ChildrenBookCategory[c] > BookVariance[ChildrenData[c].instrument][ChildrenBookCategory[c]]));



dexpr int ClassesSize[t in Teachers][s in Slots] =
	count(all(c in Children) SchedulingInstance[c][t][s], 1);
	
dexpr int TooFewStudentsClasses = 
	(sum(t in Teachers, s in Slots)
		(TypeOfClass[t][s] == MasterClass) * (ClassesSize[t][s] <= 1)) + 
	(sum(t in Teachers, s in Slots)
		(TypeOfClass[t][s] == GroupClass) * (ClassesSize[t][s] <= 2));
		
*#



dvar int HighestRankedOverall in 0..OFUpperBoundValue;


# dexpr int HighestRankedOverall = max(c in Children)  HighestRankedPerChild[c];


#*

execute {

	
	var f = cp.factory;
   	cp.setSearchPhases(f.searchPhase(HighestRankedOverall, 
   					   				 f.selectSmallest(f.domainMin( )), 
   					   				 f.selectRandomValue( )
   					   				));
}

*#


#* OBJECTIVE FUNCTION AND THE CONSTRAINTS *#

minimize HighestRankedOverall;



subject to 
{

	
	
	
	# Compute the value of the objective function
	HighestRankedOverall == max(c in Children)  HighestRankedPerChild[c];
	
	
	
	#*
	forall(c in Children)
		HighestRankedPerChild[c] == 
			(max(t in Teachers, s in Slots, e in ElectiveClasses) 
				(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, e)) * 
				AdjustedRanksOfElectiveClasses[c][e]) - LowerBoundsOnRank[c];
	*#
	
		
	
	#* MANDATORY CONSTRAINTS *#		
	
		
	# No child should be scheduled for a trivial class      
	forall(t in Teachers, s in Slots)    
		(sum(c in Children) (SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == NoClass)) <= 0;

			
	# No class for a child should be scheduled when the teacher is not available
	forall(t in Teachers, s in Slots)
	    (sum(c in Children) (SchedulingInstance[c][t][s] == 1) * (TeachersData[t].availability[s] == 0)) <= 0;	
	    

	   
	# A child can attend class with at most one teacher in any slot
	forall(c in Children, s in Slots) 
		count(all(t in Teachers) SchedulingInstance[c][t][s], 1) <= 1;
		

		
	
	# The number of classes a child can attend is consistent with the enrollment data
	forall(c in Children)
	  	count(all(t in Teachers, s in Slots) SchedulingInstance[c][t][s], 1) == 
	  		card(RequiredClasses) + ChildrenData[c].numberOfElectiveClasses + 
	  		(sum(o in OptionalRequiredClasses) 
	  			(ChildrenData[c].enrolled[o] == 1) * (OptionalRequiredClassesToSchedule[o] == 1) * 
	  			(ChildrenData[c].batch in BatchNumbersToSchedule));
	
		
		
	# A child can only attend at most one non-trivial class of any type
	forall(c in Children, a in AllNonTrivialClasses)
		(sum(t in Teachers, s in Slots) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, a))) <= 1;


	# A child has to be scheduled at least once for each required class
	forall(c in Children, r in RequiredClasses)
		(sum(t in Teachers, s in Slots) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, r))) >= 1;	


	# A child should be scheduled for an optional required class if and only if registered for it
	forall(c in Children, o in OptionalRequiredClasses)
		(sum(t in Teachers, s in Slots) 
			(SchedulingInstance[c][t][s] == 1) * 
			(TypeOfClass[t][s] == ord(AllClasses, o))) == 
				((ChildrenData[c].enrolled[o] == 1) * 
				 (OptionalRequiredClassesToSchedule[o] == 1) *
				 (ChildrenData[c].batch in BatchNumbersToSchedule));
				 

	
	
	# Only a certain number of classes of the same type can be scheduled during the same slot
	forall(a in AllNonTrivialClasses : NumberOfConcurrentClasses[a] > 0, s in Slots)
	  	count(all(t in Teachers) TypeOfClass[t][s], ord(AllClasses, a)) <= NumberOfConcurrentClasses[a];
		
	# Each class should contain a minimum number of children
	forall(t in Teachers, s in Slots, a in AllNonTrivialClasses : MinimumClassSizes[a] > 0)
		count(all(c in Children) SchedulingInstance[c][t][s], 1) >= MinimumClassSizes[a] * (TypeOfClass[t][s] == ord(AllClasses, a));
			
	
	# The number of children scheduled to attend the same class does not exceed the capacity of the class
	forall(t in Teachers, s in Slots, a in AllNonTrivialClasses: DefaultClassCapacities[a] > 0)
		(sum(c in Children) 
			(SchedulingInstance[c][t][s] == 1) * 
			(TypeOfClass[t][s] == ord(AllClasses, a))) <= DefaultClassCapacities[a];
			
	
	
	#* Constraints related to teacher *#
	
	
	# A class scheduled for a teacher should be consistent with the expertise of the teacher
	forall(t in Teachers, s in Slots)
		(sum(p in TeachersData[t].proficiences) 
			(TypeOfClass[t][s] == ord(AllClasses, p))) >= (TypeOfClass[t][s] != NoClass);
	
	
	
	# The instrument of a child should be consistent with that of his/her teacher
	forall(c in Children, t in Teachers, s in Slots)
		(sum(i in InstrumentDependentClasses) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, i)) * 
			(ChildrenData[c].instrument not in TeachersData[t].instruments)) <= 0;
			

	# A teacher should only teach children whose book levels are consistent with his/her preference (I)			
	forall(c in Children, t in Teachers, s in Slots)
		(sum(b in BookBasedClasses) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) * 
			(ChildrenData[c].book < TeachersData[t].minimumBookLevel[ChildrenData[c].instrument])) <= 0; 
	
	# A teacher should only teach children whose book levels are consistent with his/her preference (II)	
	forall(c in Children, t in Teachers, s in Slots)
		(sum(b in BookBasedClasses) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) * 
			(ChildrenData[c].book > TeachersData[t].maximumBookLevel[ChildrenData[c].instrument])) <= 0; 			
		
	
	# A teacher should only teach children whose ages are consistent with his/her preference (I)
	forall(t in Teachers, s in Slots)
			(sum(c in Children) (SchedulingInstance[c][t][s] == 1) * (ChildrenData[c].age < TeachersData[t].ageRange.lower)) <= 0;
		
	# A teacher should only teach children whose ages are consistent with his/her preference (II)
		forall(t in Teachers, s in Slots)
			(sum(c in Children) (SchedulingInstance[c][t][s] == 1) * (ChildrenData[c].age > TeachersData[t].ageRange.upper)) <= 0;

	
	# The number of classes a teacher is scheduled to teach does not exceed his/her availability  
	forall(t in Teachers)
	  	count(all(s in Slots) TypeOfClass[t][s], NoClass) >= NumberOfClassesInADay - TeachersData[t].numberOfClasses;


	#* Attributes of classes *#
	
	
	#*
	# For each class, find if it has at least one student with a given instrument
	forall(t in Teachers, s in Slots, i in Instruments) 
		ClassesInstrumentPresent[t][s][i] ==
			(count(all(c in Children : ChildrenData[c].instrument == i) SchedulingInstance[c][t][s], 1) > 0);
	
	
		
	# Find the book category for each class
	forall(t in Teachers, s in Slots, i in Instruments)   
		ClassesBookCategory[t][s][i] == 
			(max(c in Children) 
				(SchedulingInstance[c][t][s] == 1) * 
				(ChildrenData[c].instrument == i) * ChildrenBookCategory[c]);
			
			
	# Find the age category for each class
	forall(t in Teachers, s in Slots)   
		ClassesAgeCategory[t][s] == 
			(max(c in Children) (SchedulingInstance[c][t][s] == 1) * ChildrenAgeCategory[c]);
			
	# Find the batch number for each class
	forall(t in Teachers, s in Slots)   
		ClassesBatchNumber[t][s] == 
			(max(c in Children, b in BatchBasedClasses) 
				(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) * ChildrenBatchNumber[c]);	

	
	*#


	#* Constraints related to children *#


      	
      	
	# A single instrument class should have children learning the same instrument
	
	#*
	forall(c in Children)
	  	(sum(t in Teachers, s in Slots, o in OneInstrumentClasses, d in Children)
			(SchedulingInstance[c][t][s] == 1) * (SchedulingInstance[d][t][s] == 1) * 
			(TypeOfClass[t][s] == ord(AllClasses, o)) *
			(ChildrenData[c].instrument != ChildrenData[d].instrument)) <= 0;
			
	*#
	
	forall(t in Teachers, s in Slots, o in OneInstrumentClasses)
	  	(sum(i in Instruments) (TypeOfClass[t][s] == ord(AllClasses, o)) * (ClassesInstrumentPresent[t][s][i] == 1)) <= 1; 
	  	# count(all(i in Instruments) ClassesInstrumentPresent[t][s][i], 1) <= 1;
		
	 				
	# A book based class should have children at similar book levels
	forall(c in Children : ChildrenData[c].instrument not in ExceptionInstruments)	
		(sum(t in Teachers, s in Slots, b in BookBasedClasses) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) *
			(ChildrenBookCategory[c] + 
			 MaximumBookVariance[ChildrenData[c].instrument][ChildrenBookCategory[c]][b] <
			 						ClassesBookCategory[t][s][ChildrenData[c].instrument])) <= 0;
		
		
	
			 						
			 							

	# An age based class should have children of similar ages (based on age category)    
	forall(c in Children)	
		(sum(t in Teachers, s in Slots, a in AgeBasedClasses)
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, a)) *
			(ChildrenAgeCategory[c] + 
			 MaximumAgeVariance[ChildrenAgeCategory[c]][a] <
			 						ClassesAgeCategory[t][s])) <= 0;
			 	
			
		
	
	# All children with the same batch number should be scheduled for the same class		
	forall(c in Children)
		(sum(t in Teachers, s in Slots, b in BatchBasedClasses)
	  		(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == ord(AllClasses, b)) * 
	  		(ChildrenData[c].batch != ClassesBatchNumber[t][s])) <= 0;
	
		
	# All children in a batch based class should have the same batch number
	forall(b in BatchBasedClasses, r in RangeOfBatchNumbers : r > 0)
		(sum(t in Teachers, s in Slots) 
			(TypeOfClass[t][s] == ord(AllClasses, b)) * (ClassesBatchNumber[t][s] == r)) <= 1;
			
			
	#* Constraints related to classes that require special processing *#
	
	
	# The Masterclass of a child cannot be with his/her private teacher
	forall(c in Children, s in Slots)
		(sum(t in Teachers) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == MasterClass) * 
			(ChildrenData[c].teacher == TeachersData[t].lastName)) <= 0;
	
	
	# The Masterclass of a child enrolled at SMID cannot be with a SMID teacher
	forall(c in Children, s in Slots)
		(sum(t in Teachers, f in ForbiddenPrivateTeacherMasterClassTeacherCombinations) 
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == MasterClass) * 
			(ChildrenData[c].teacher in f.teachers) * (TeachersData[t].lastName in f.teachers) ) <= 0;
	
			
	# Number of siblings scheduled to attend master classes during the same slot is upper bounded
	forall(s in Slots, f in SiblingsFamilies : card(SiblingsData[f]) > MaximumNumberOfSiblingsInMasterClassesPerSlot )
		(sum(t in Teachers, c in SiblingsData[f])
			(TypeOfClass[t][s] == MasterClass) * 
			(SchedulingInstance[c][t][s] == 1)) <= MaximumNumberOfSiblingsInMasterClassesPerSlot;  	
			
			
	
	# The number of children scheduled to attend the same Masterclass does not exceed the capacity of the class for that book category
	forall(t in Teachers, s in Slots)
		forall(i in Instruments, b in SetOfBookCategories[i])
			(TypeOfClass[t][s] == MasterClass) * 
			count(all(c in Children) SchedulingInstance[c][t][s], 1) *
			(count(all(c in Children : ChildrenData[c].instrument == i && ChildrenData[c].book == b) SchedulingInstance[c][t][s], 1) > 0)
				<= 
			CapacitiesForMasterclassBasedOnBookCategory[i][b];
	
	# The number of children scheduled to attend the same Compose and Compute class does not exceed the availability for that slot
	forall(t in Teachers, s in Slots)
		(sum(c in Children) 
			(SchedulingInstance[c][t][s] == 1)) * 
			(TypeOfClass[t][s] == ComputeAndComposeClass) <= CapacitiesForComposeAndComputeClass[s];  		


	#*
	
	# Any child scheduled for Compose and Compute class should be at least at a certain book level
	forall(c in Children)
		(sum(t in Teachers, s in Slots)
			(SchedulingInstance[c][t][s] == 1) * 
			(TypeOfClass[t][s] == ComputeAndComposeClass) * 
			(ChildrenData[c].book < MinimumBookLevelForComposeAndComputeClass)) <= 0;
	
	# Any child scheduled for Improvisation class should be at least at a certain book level		
	forall(c in Children)
		(sum(t in Teachers, s in Slots)
			(SchedulingInstance[c][t][s] == 1) * 
			(TypeOfClass[t][s] == ImprovisationClass) * 
			(ChildrenData[c].book < MinimumBookLevelForImprovisationClass)) <= 0;
	
	
	# Any child scheduled for Music and Movement class should not be older than certain age
	forall(c in Children)
	  	(sum(t in Teachers, s in Slots)
	  		(SchedulingInstance[c][t][s] == 1) * 
	  		(TypeOfClass[t][s] == MusicAndMovementClass) * 
	  		(ChildrenData[c].age > MaximumAgeForMusicAndMovementClass)) <= 0;
	*#
	
	
	
	
	# Ensure that students with certain instrument types are not in the same Fiddling class 
	forall(t in Teachers, s in Slots)
		(sum(f in ForbiddenPairOfInstrumentsForFiddling) 
			(TypeOfClass[t][s] == FiddlingClass) * (ClassesInstrumentPresent[t][s][f.this] == 1) * 
			(ClassesInstrumentPresent[t][s][f.that] == 1)) <= 0;	
	
	
	# The number of children scheduled to attend the same Group class does not exceed the capacity of the class for that instrument
	forall(t in Teachers, s in Slots)
		(sum(c in Children)
			(SchedulingInstance[c][t][s] == 1) *
			(TypeOfClass[t][s] == GroupClass)) <= (max(i in Instruments) CapacitiesForGroupClass[i] * (ClassesInstrumentPresent[t][s][i] == 1));
			
			
	#* Constraints related to teachers that require special processing *#
	
	# Ensure that the constraints related to the minimum number of classes to be taught by a teacher are satisfied
	forall(e in TeachersRequiredClasses)
	  	count(all(s in Slots) TypeOfClass[ord(NamesOfTeachers, e.name)][s], ord(AllClasses, e.type)) >= e.value;
	 
	
	# Ensure that special requests for undesirable Masterclass teacher are honored 
	forall(e in DoNotWantAsMasterClassTeacherSet)
		(sum(c in Children, t in Teachers, s in Slots)
			(SchedulingInstance[c][t][s] == 1) * (TypeOfClass[t][s] == MasterClass) * 
			(ChildrenData[c].name == e.child) * (TeachersData[t].name == e.teacher)) <= 0;
	
	
	
	
	
	
	
	# large rooms constraints
	forall(s in Slots)
		(sum(t in Teachers, l in LargeRoomClasses) 
			(TypeOfClass[t][s] == ord(AllClasses, l))) <= NumberOfLargeRoomsAvailable; 
			
	
	# pre twinklers
	forall(c in Children: ChildrenData[c].book == 0)
		count(all( t in Teachers, s in Slots : s not in SlotsForPreTwinklers) SchedulingInstance[c][t][s], 1) == 0;
		
	
	# book based constraints	
	forall(e in ElectiveClasses)
		(sum(c in Children, t in Teachers, s in Slots)
			(TypeOfClass[t][s] == ord(AllClasses, e)) * (SchedulingInstance[c][t][s] == 1) *
			(ChildrenData[c].book not in BooksEligibleForElectiveClasses[e][ChildrenData[c].instrument])) <= 0;
	
	# age based constraints 		
	forall(e in ElectiveClasses)
		(sum(c in Children, t in Teachers, s in Slots)
			(TypeOfClass[t][s] == ord(AllClasses, e)) * (SchedulingInstance[c][t][s] == 1) *	
			(ChildrenData[c].age not in AgesEligibleForElectiveClasses[e][ChildrenData[c].instrument])) <= 0;
			
	
	# Accompanist		
	forall(s in Slots)
	    count(all(t in Teachers: TeachersData[t].name not in TeachersNotRequiringAccompanist) TypeOfClass[t][s], GroupClass) <= 
	  	count(all(t in Teachers: TeachersData[t].accompanist == 1 && TeachersData[t].availability[s] == 1) TypeOfClass[t][s], NoClass);
};	
	


#*************************************************************************************************************#



# Variables used to print the output in human-friendly manner


string NamesOfClasses[r in RangeOfClassTypes] = item(AllClasses, r); 
string NamesOfSlots[Slots] = [
   "9:00AM-9:50AM", "10:00AM-10:50AM", "11:00AM-11:50AM", "1:30PM-2:20PM", "2:30PM-3:20PM" 
];

#*
execute {

	var file = new IloOplOutputFile( "statistics.dat" );

	for(var t in Teachers)
		for(var s in Slots)
		{
			var delta = 0;
			
			for(var c in Children)
			{
 				if ((SchedulingInstance[c][t][s] == 1))
 				{
   					if (delta < ClassesAgeCategory[t][s] - ChildrenAgeCategory[c])
   						delta = ClassesAgeCategory[t][s] - ChildrenAgeCategory[c];
 				}						
			}
			
			file.writeln(delta);
		}	
	file.close();	
			
}

*#

execute { 

	var quote = "\"";
	var comma = ",";
	var colon = ": ";
	var newline = "";
	var separator = " + ";

    # open the output file
	var file = new IloOplOutputFile("ScheduleForTeachers.csv");

	# write the header row
  	file.write("Slot");
  	
  	for(var t in Teachers) {
  		file.write(comma + quote + TeachersData[t].name + quote);
	}  	   
  	   
  	file.writeln("");
  	
  	# write each data row
  	for(var s in Slots) {
 		file.write(quote + NamesOfSlots[s] + quote);
 		
 		for(var t in Teachers) {
 		
 		    file.write(comma + quote)
 			
 		
 			file.write(NamesOfClasses[TypeOfClass[t][s]] + colon); 		
 		    
 		    var firstChild = true;
 		    
 			for(var c in Children) {
 				if (SchedulingInstance[c][t][s] == 1) {
 			    	if (firstChild) { 				
 			 			file.write(ChildrenData[c].name);
 			 			file.write(" (" + ChildrenData[c].age + comma + ChildrenData[c].instrument + "@" + ChildrenData[c].book + ")");  
 			 			firstChild = false;
     				} else {
     					file.write(separator + ChildrenData[c].name);  
     					file.write(" (" + ChildrenData[c].age + comma + ChildrenData[c].instrument + "@" + ChildrenData[c].book + ")");  				
     				}
     			 				 				 			
 				} 		 		
 			}
  			 			
 			file.write(quote);
 		} 
 		
 		file.writeln("");		  	  	
  	}
 	
 	
  	file.close( );	
}
 
 
 
 execute { 

	var quote = "\"";
	var comma = ",";
	var space =  " ";
	var colon = ": ";
	var newline = "";

    # open the output file
	var file = new IloOplOutputFile( "ScheduleForChildren.csv" );

	# write the header row
  	file.write("Last Name" + comma + "First Name");
  	
  	for(var s in Slots) {
  		file.write(comma + NamesOfSlots[s]);
	}  	   
  	   
  	file.writeln("");
  	
  	# write each data row
  	for(var c in Children) {
 		file.write(ChildrenData[c].lastName + comma + ChildrenData[c].firstName);
 		
 		for(var s in Slots) {
 		
 		    file.write(comma);
 		
 			for(var t in Teachers) {
  				if (SchedulingInstance[c][t][s] == 1) {
  			   		
  			   		file.write(quote + NamesOfClasses[TypeOfClass[t][s]] + colon);
  			   		file.write(TeachersData[t].name + quote);  			   
  			   			   	 			 			
 				}
  			} 			
 			
 		} 
 		
 		file.writeln("");
 	} 					
 	
  	file.close( );	
}