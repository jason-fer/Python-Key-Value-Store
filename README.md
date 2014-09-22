+-------------------------------------------------------------------------------
| Project 1
| Authors: Saikat Raphael Gomes, Jason Feriante, Rahul Chatterjee
| Date: 12 Sep 2014
| Emails: feriante@cs.wisc.edu, saikat@cs.wisc.edu, rchat@cs.wisc.edu
| Semester: CS739 Spring 2014
| Section: LEC 001
| Professor: Michael Swift
+-------------------------------------------------------------------------------

Our Group:
Saikat Raphael Gomes
Jason Feriante
Rahul Chatterjee

Partner Group:
Anusha Dasarakothapalli
Adalbert Gerald Soosairaj
Navneet Potti


Our Server:
python test_client.py http://seclab8.cs.wisc.edu:5000

Brandon's server:
python test_client.py http://adg-desktop-07.cs.wisc.edu:8080

python test_client.py localhost:5000

@todo:

Performance Tests:

-Throughput: requests per second in each scenario
  -get / put (best, worst, expected key value sizes)
  -Probability based get / put ratios (e.g. read heavy/ write heavy loads)

-Failure tolerance: 
  -heartbeat cron process sends heartbeat every 10 seconds. if the request
  times out, the server is restarted
  -find a way to overload server, confirm it correctly restarts

-Latency:
  -time for the round trip of a client to server request.
  -get latency averages for different scenarios
