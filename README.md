# Word Game Level Generator
 Level and wordlist generator for a word game that generates, validates and sorts by frequency in English.

 5letter.py can be used for generating 5 lettered words and its sub words in excel format.
 
 6letter.py can be used for generating 6 lettered words and its sub words in excel format.

 words.py can be executed to generate levels that takes six_letter_words_list.xlsx and five_letter_words_list.xlsx into consideration and generates satisfied_distributions.xlsx that fits the distributions.txt file. Program also takes used.txt as an input to avoid generating same letters that used before. In my example distributions.txt and used.txt is filled as an example. You should change contents that is in these txt files. 

 5letter.py and 6letter.py should be exxecuted before words.py in order to create excel tables for words.py to take into consideration.


 As I stated in the code you can change iteration count of for loop in 6letter.py and 5letter.py. Iteration count set to 2000 as default in the code but you can change it for your needs. Just note that bigger iteration counts can increase the execution time of program. 

 I hope it helps a lot for your projects and games.

-VSCB
