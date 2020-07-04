Quad created by Saverio Simonelli MIT license 2020

Quad finds G-quadruplexes forming regions within a set of transcript sequences. It uses transcript IDs as in RefSeq annotation and it searches for their sequence from Genome Browser Database (https://genome.ucsc.edu). The program assigns them a stability score according to two preexisting algorithms:  QGRS and PQS. 

The first one, created by Ramapo group, is a software which has two versions: the first one working locally on computer (https://github.com/freezer333/qgrs-cpp), accessible by terminal, and the second being a web-based one, whose link is  http://bioinformatics.ramapo.edu/QGRS/index.php.

PQS is a R-library distributed by Bioconductor. In order to be used from Quad window, a R compiler needs to be present on Computer and the library must be discharged as explained at the following  link: https://bioconductor.org/packages/release/bioc/html/pqsfinder.html.

By using Quad, it is possible to choose between QGRS local version, QGRS web version (QGRS Mapper) or PQS (pqsfinder). 

Be careful: csv files should use semicolon (;) as separator.

Quad creates a database wired in the file system and outputs of each transcript set are coded in summary tables saved in the local database.

In order to use quad executable version: download source code, download executable file and save it in bin folder.

In case using Mac or Linux Operating Systems change file permissions from command line:
        sudo chmod 777 quad-linux 
        or
        sudo chmod 777 quad-mac
        sudo chmod 777 quad-mac-start

Use source files if it is not possibile run the executable file:
        from command line change directory to src folder
		Windows: 
			python quad.py
		Mac/Linux: 
			python3 quad.py
		If required:
				download Python version 3.x (https://www.python.org/)	
				install following Python Libraries:
					Windows: 
						pip install requests
						pip install numpy
						pip install pandas 
						pip install matplotlib
					Mac/Linux:
						pip3 install 
