Quad created by Saverio Simonelli MIT license 2020

Quad finds G-quadruplexes forming regions within a set of transcript sequences. It uses transcript IDs as in RefSeq annotation and it searches for their sequence from Genome Browser Database (https://genome.ucsc.edu). The program assigns them a stability score according to two preexisting algorithms:  QGRS and PQS. 

The first one, created by Ramapo group, is a software which has two versions: the first one working locally on computer (https://github.com/freezer333/qgrs-cpp), accessible by terminal, and the second being a web-based one, whose link is  http://bioinformatics.ramapo.edu/QGRS/index.php.

PQS is a R-library distributed by Bioconductor. In order to be used from Quad window, a R compiler needs to be present on Computer and the library must be discharged as explained at the following  link: https://bioconductor.org/packages/release/bioc/html/pqsfinder.html.

By using Quad, it is possible to choose between QGRS local version, QGRS web version (QGRS Mapper) or PQS (pqsfinder). 

Be careful: csv files should use semicolon (;) as separator.

Quad creates a database wired in the file system and outputs of each transcript set are coded in summary tables saved in the local database.

In order to use quad executable version: download source code, download executable file and save it in bin folder.
<pre>
In case using Mac or Linux Operating Systems change file permissions from command line:<br>
        sudo chmod 777 quad-linux<br>
        or<br>
        sudo chmod 777 quad-mac<br>
        sudo chmod 777 quad-mac-start<br>

Use source files if it is not possibile run the executable file:<br>
        from command line change directory to src folder<br>
		Windows:<br>
			python quad.py<br>
		Mac/Linux:<br>
			python3 quad.py<br>
		If required:<br>
				download Python version 3.x (https://www.python.org/)<br>	
				install following Python Libraries:<br>
					Windows:<br>
						pip install requests<br>
						pip install numpy<br>
						pip install pandas<br> 
						pip install matplotlib<br>
					Mac/Linux:
						pip3 install 
</pre>
