<h1 align='center'>WIKIPAGES - PAGERANK</h1>
<h4 align='center' >This project involves extracting data from a Wikipedia dump and utilizing the information to generate useful insights using the PageRank algorithm.
</h4>
<br/>
<h2 align='center'>Wikipedia Dump Analysis using PageRank Algorithm</h2>

The project follows these key steps:

1. **Data Extraction**:

    1.1. Utilize the Wikipedia dump to extract page titles, redirect titles, and page children links.

    1.2. Generate two text files: "alias.txt" containing title and redirect title, and "edges.txt" containing title and children links.

2. **Preprocessing and Dictionary Creation**:

    2.1. Process the text files and create Python dictionaries from the extracted data.

    2.2. Store the dictionaries in pickle files for efficient storage and retrieval.

3. **Main File Execution**:

    3.1. Utilize the generated pickle files to run the main file of the project.

    3.2. The main file implements the PageRank algorithm and performs random walks on the Wikipedia graph.

4. **Output Generation**:

    4.1. Obtain the top 'k' pages based on the PageRank scores calculated.

    4.2. Retrieve and display all the links associated with a specific page.

The project aims to leverage the PageRank algorithm's principles to identify the most influential pages within the Wikipedia dataset. By performing random walks on the graph, the algorithm assigns importance scores to each page, aiding in the discovery of highly relevant information and understanding the interlinking structure of Wikipedia articles.


<h2 align='center'>Steps to use</h2>

1. Libraries used - random and pickle 

2. Copy the zip file containing all code files from this github repository

3. Download the dump file from this link https://dumps.wikimedia.org/enwiki/latest/  named as enwiki-latest-pages-articles.xml.bz2-rss.xml , this is the dump of all the pages available on wikipedia

4. To save your time from extracting the important information from this dump using the getfiles.py file I have uploaded premade files by me on the drive link https://drive.google.com/drive/folders/1_Py3DXHjLF01nW3tPVDauCrMfxdS0XC-?usp=sharing 

5. You can download the original files named alias.txt and edges.txt or the smaller version of them named as alias1.txt and edges1.txt

6. This drive link contains some pickle files as well in which all the lists that we have made while running storedict.py

7. Some images are uploaded in the images folder to understand the project well

8. And also I have made a bz2file.txt that shows you the format of data stored in dump file as it is very complicated to open it

9. Now you can directly download these pickle files and run main.py to get the results 
