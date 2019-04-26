# Task:

Without using existing solutions (like Scrapy), write a library in Python that can scrape images from flickr.com.
Let's limit the scope to scraping Paris, Rome, and New York, e.g. https://www.flickr.com/search/?text=paris.

Your library should process multiple images concurrently / in parallel and extract file names and GPS information from
images. If you don't see GPS info in the images, you can pull it form JavaScript. As a final step, insert
extracted metadata into a relational database (sqlite is fine). Include a couple of unit tests in your code.

Your design for the solution should be suitable for a highly scalable environment and can fetch data from Flickr
at the same rate if multiple locations are added into the scope and process all locations in parallel.

subtasks taking the task above literally:

- [x] create function to get the page and find all image links
- [ ] create function that will extract GPS info from an image
- [x] write to the DB
- [x] write some tests
    - [ ] test get page and that is has links
    - [ ] test GPS extraction from image
    - [ ] test writing to the DB
- [x] update to add parallel functions

# some post work notes:

while trying to see what was happening from the main search page, i noticed that the 
images were being loaded as i scrolled down the page.  
that is a javascript behavior. i don't think it's easy to write a python script 
that will simulate this behavior.   
i also noticed though that the javascript was making API calls.  
i was able to make the same calls via Postman.  
Then i discovered that Flickr has friendly API documentation.  
the Flickr docs mention that only the "_o" (for original) files have GPS embedded in the exif data.  
using the API , i found the URL of an *original* file that had GPS info in it's json data.  
i downloaded the file and *unsuccessfully* attempted to read the exif data using 3 different tools:
 
1. imagemagick
2. [exifread](https://pypi.python.org/pypi/ExifRead)
3. and jhead 

i was never able to extract the GPS data from any file that was scraped.
the only GPS data i am able to get is through the Search API.

i did write some simple tests, and wrote code to insert the results into a sqlite DB.
i used locks b/c sqlite can only be open for writing by one thread at a time.

## to execute 

please use python version: `Python 3.6.3`
i did not test with any other versions of python 3.
python __2__ will not work b/c the libraries and function annotations are not backward compatible.

   
### the scrape script

    python scrape.py   

- does not extract GPS data.
- does download the files that are pre-loaded in the main html at the start.
- does not go back for more data like the javascript does as the user scrolls down.

### the api script
    
    python api.py

- gets the total count from the first hit 
- keeps going back for more results until there are no more to be retrieved.
- was written b/c in real world situations, someone might scrape data b/c no API exists. once we learn of an API, 
we should use it. 

### both scripts:
   
- do their work in parallel, starting a few threads that then spawn more threads of their own.
- do write to the db, creating the table if it does not exist.

i also setup sphinx to autodocument, but did not have time to circle back around to the functions to fill in the 
docstring info. I did my best to write the functions with meaningful/obvious names, and implemented function annotations
as much as possible.


if i had more time, i would:
- add some re-try functionality for cases where the server returns 502 error (or any 500 error)
- follow up with Mavrx to see how the GPS data might be better extracted
- write the improved docstrings and regenerate the sphinx docs. 
currently they are [bare bones](sphinx_docs/build/html/index.html) (btw, this link will not work in github.com)
 

i deliberately did not use BeautifulSoup , requests, or even django.

this was a fun POC. 



