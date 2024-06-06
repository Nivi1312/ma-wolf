_Tested for Python v3.9.13, numpy v1.26.1, DockerEnigne v25.0.2, matplotlib v3.8.0, neurokit2 v0.2.6, pyunisens 1.4_



**Requirements**

The packages numpy, neurokit2, pyunisens and matplotlib need to be installed.
This can be done with: 
- 	pip install numpy
- 	pip install neurokit2
- 	pip install pyunisens
-   pip install matplotlib

Also install Docker Desktop if containerization is wished.


**Files**

- data_input.py : Handles creating a BPM-Database with ECG-Data from Corvolution.
- salient_point.py : Realization of Anonymization of a single users health data (curve) via the salient point algorithm.
- schemes.py : Class of the anonymization schemes described in my work (SP, SPA, SPC, SPAC, SPCA). Incorporates custom sensitvities and the Pre-Aggregations C-Category and k-Average.
- main.py : Complete pipeline. Loads data, anonymize data and build database, calculate average heart rate query and detect stressful times. Can be containerized.
- dockerfile : Blueprint of container image.
- evaluation_visualization.py : Evaluation and visualizations of complete pipeline. Not part of the containization.

**Setting-Up**

The database with the heartbeats per minute must be set up before any other function can be performed. This can be done with the
data_input.py script. The data path must be changed to the path of the "Corvolution" data folder.
Also change bpm_db_output to the current directory (do not change bpm_db_name). The data transformation process can take
a while.
Error of the form 'ERROR:root:File CAREMON.LOG does not exist' can be ignored.


**How to use** 

The core functionality can be executed using main.py.
For local execution, change the db_path to the full path of all_bpm.p (including name). 
The parameters epsilon, C and k can be changed in the top. 
Uncomment the schema to be used (comment out all others or make deepcopies of data if several are used).
Specify the sensitivity to be used for anonymization in anonymize_database(...) by selecting one of the keys 'theo', 'emp', 'cor'.

For visualizations and the MACE evaluation, use evaluation_visualization.py (the same adjustments must be made as in main.py, e.g. for db_path, and parameters).
The y- and x-axes currently have no value-transformation adjustment for categorization and k-means. Please take this into account when interpreting the diagrams.


**Containerization**

mainy.py and its dependencies (including all_bpm.p) are copied into a container. The evaluation_visualization.py file is not excluded for containerization.
For containerization, the bpm database all_bpm.p is expected to be located in the same folder. Then, simply change the db_path in main.py to "all_bpm.p".
Execute the docker command in the folder:  'docker build -t salient .' to build the container image.
Use 'docker run salient' to create and run the container instance.