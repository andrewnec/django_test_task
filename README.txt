The test task was completed in full

In ./videos/1.png you will see how the data is loaded into the sql database
2000 authors and 5000 books were used for the test, since loading about 90 GB of data on my laptop would take forever,
I thought that a smaller data set could be used for the test.

To determine the author of the book, I took the "author_name" field. There is also an "authors" field (usually there are several authors), but in some books it is empty, I did not take it into account.
I did not find any clarification on this point in the technical specifications.

Authors are loaded first, and then books. If the author of the book is not in the database, he is created there.

The search by book description does not occur, since this was not specified in the technical specifications. Search is performed only by the author's name and book title

In ./videos/2.mp4 and ./videos/3.mp4 I test live almost all the functionality, I only skipped
a few commands to save time, but rest assured that all the commands work.

You can see the entire list of commands in commands.txt

You can see a detailed description of the recommendation system in description_of_the_recommendation_system.txt
In ./videos/3.mp4 you can see how quickly (less 1 second) the list of recommendations is returned (but you should take into account that a relatively small set of data was used for the test)
