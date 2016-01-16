README.txt

Name: Wen Chuan Lee
x500: leex7095 (4927941)

How to run the server and clients

	./db-server <db_port> (provided for us)
	./dir-server.py <ds_port>
	./app-server.py <ds_port>
	./app-client.py <ds_port> <db_port>

If that does not work make sure to run `chmod +x <file>.py` first, or else just do `python3 <file>.py`

- dir-server is located at apollo.cselabs.umn.edu
- db-server is located at atlas.cselabs.umn.edu
- app-server is located at csel-kh4250-06 at 128.101.37.6 
- app-server-2 is located at 128.101.37.20
- app-client is located at lind40-10 at 134.84.62.110 
- app-client-2 is located at lind40-15 at 134.84.62.115

Additional Notes: 
- Files to be sent over the network can be changed at Line 145 of app-client.py (in the main function)
- selectedAppServer can be chosen at L27 of app-client.py where we pick the app-server based on index
- files to be sent were generated with base64 /dev/urandom | head -c 100k > 100k.dat for a 100k sized file of random b64 numbers
- 2 client_record sets were included, one when manual runs where done, and one more when everything was completely automated.
- All file transfers were done with 5 trial runs and the average collected before being sent to the db-server for records. 

