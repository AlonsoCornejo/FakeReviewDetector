*****************************************************************************
* Annotated by: Nitin Jindal and Bing Liu, 2006.
*		Department of Computer Sicence
*               University of Illinois at Chicago              
*
* Contact: Nitin Jindal, njindal@cs.uic.edu 
*****************************************************************************

1. The file labeledSentences.txt contains annotated data from varios sources.

	1. Amazon customer reviews on 
		digital camera: Canon G3
		digital camera: Nikon coolpix 4300
		celluar phone: Nokia 6610
		mp3 player: Creative Labs Nomad Jukebox Zen Xtra 40GB
		dvd player: Apex AD2600 Progressive-scan DVD player
	2. Reviews comparing Intel AMD from http://www.epinions.com
	3. Reviews on digital cameras from http://www.dcresource.com
		Fuji FinePix Z1
		Fuji FinePix A210
		Fuji FinePix Z1
		Casio Exilim EX-Z750, and some more
	4. Articles from 
		PC World on HP Pavilion dv4000
		Sys Technology Freestyle M7500
		iPod nano, and some more
	5. Random articles on Google vs Yahoo, Coke vs Pepsi, cars, etc.

Note: Each line contains one sentence which were separated by using a tokenizer.

2. The file listOfkeywords.txt contains the list of comparative words and phrases used

The data was used in the following 
two papers:

Nitin Jindal and Bing Liu. "Identifying Comparative Sentences in Text Documents". 
   Proceedings of the ACM SIGIR International Conference on 
   Information Retreival (SIGIR-06), 2006.

Minqing Hu and Bing Liu. "Mining Opinion Features in Customer 
   Reviews." Proceedings of Twenty First National Conference on 
   Artificial Intellgience (AAAI-2006), 2006.


Symbols used in the annotated text: 

Sentences enclosed in following xml style tags are comparative sentences
<cs-1>...</cs-1> ---> Non-equal gradable
<cs-1>...</cs-2> ---> Equative
<cs-1>...</cs-3> ---> Superlative 
<cs-4>...</cs-4> ---> Non-gradable
First three types are gradable comparative sentences
Rest of the sentences are non-comparatives

Each comparative sentence is followed by the relations expressed in the sentence (each in single line) in the format:
A_<Name> * (comparative phrases)

where,
A is type of constituent of relation, which can be 1 (entity S1), 2 (entity S2) or 3 (feature)
<Name> is the name of entity or feature
comparative phrase: is the word or phrase which is used for that comparative relation.

Ex:
<cs-1>
creative zen also costs a lot less than the ipod .
</cs-1>
1_creative zen 2_ipod 3_costs (less)

Type: Gradable Comparative
entity S1: creative zen
entity S2: ipod
feature: costs
keyword: less
