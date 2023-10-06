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


To DO:
- clean code, optimize it
- use environments
- make the schema and table to be created at container initialization
- build a jupiter notebook to consume the db data.
