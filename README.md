# fligoo_challenge
repo to store files associated with the Fligoo chanllenge detailed here: 

https://colab.research.google.com/drive/1nrexF20P2sHnFqnTni0zcFDdaAWxTLly#scrollTo=_ZrmQTYqKXnA


# General considerations:
- I had cero experience with Airflow and Docker (while i did have a high level idea of how Docker works)
- I wanted to learn the basics of Airflow / Docker while developing this solution
- I needed to validate each building block by itself.

Then what i did was:

1- Log In into the Flights API to get a KEY. 

2- Develop a Jupiter notebook to test the API connection, data retrieval, transformation, etc. 

3- Make some tutorials on Airflow to learn the basics

4- Try to migrate the Jupiter python code to Airflow (here i got stuck when SQLALchemy failed on the writing to the db)

5- Search for a better way to implement the Docker solution as a multicontainer 

-------
How to run this?   

1- clone the repo

2- follow the steps described in stuff_to_be_run file

3- Copy the dags of the root to the dag folder, Test the Airflow DAG by hand (check that i commented the flight status filter as sometimes there are no flights under such condition)

4- Use the notebook called 'fligoo_output_test.ipynb' to test the results


Stuff i still didnt manage to get:
- when i migrated to this version i cant get for airflow server to be accessible on the web browser 
- how to create the table on startup of the docker image, i think it must have to do with the init-db.sql 
- configure the DAG to run automatically in a periodic fashion
- add checks and error handling 
- clean stuff
- make the first steps automatically executed when launching the container
- add a proper gitignore
