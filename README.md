# Instagram_like_follow


This bot is developed to first like some Posts of an user and then follow him/her.
It will run by starting "main.py"


It will work in the following steps :-

1. It will log into instagram using username and password stored in credentials.xlsx
2. It will use the parameters.xlsx to get the location of file "insta_search.xlsx"  
3. It will first read the Username written in file "insta_search_found.xlsx".
4. Then will like atmost 3 posts (which depends on the no of posts available).
5. Then will follow the user.
6. After following will write "OK" in status coloumn.
6. In case the username is private this will follow him/her without liking the posts.
7. In case the username is incorrect (which may happen if the user had changed his\her username recently) :- then will write "WRONG" in status column.
8. This will repeat the whole process for all usernames.

9. The bot will pause itself for the time limit(given) if it reaches the limit (given).
10. Once it works for all the username in "insta_search_found.xlsx", then will rename the file into "insta_search_found_done.xlsx".




Note :- 

   > Make sure you are writing the path(location) of directory(folder) in which "insta_search_found.xlsx" is there, in "parameter.xlsx". Not the path of the file itself.
    
   > Example :- 
      It should be like -- C:\Python\Projects\Insta_followers\assets
      Not like          -- C:\Python\Projects\Insta_followers\assets\insta_search_found.xlsx
      
   > Make sure to write correct username and password, otherwise the bot will show unwanted errors.
    
   > Make sure to write all the three coloumns in "parameter.xlsx" before running the scrips. ( Please write time limit in minutes ).
   
   > If the bot is opening the Chrome window (i.e Is not running silently) then please dont minimize, change the shape of the window to run it smoothly.
    
    
	
 For Technical Information
 The library's used :- 
    -selenium
    -openpyxl
    -time
    -shutil 		--pytest-shutil
    -os
    -sys
    -pause          --pause
    -datetime
    -logging
 
