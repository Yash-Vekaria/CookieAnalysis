# CookieAnalysis
This repository constitues Quantcast's Summer Internship 2024 related coding implementation.

The assigned task is to extract the most active cookie corresponding to the queried date from a cookie log file consisting of cookies and timestamps. 

Task instruction details provided by Quantcast recruiter can be found in the ```Quantcast Coding Task Exercise.pdf```. 

Following are the steps to execute/test my solution:
1. Clone the repository on your local:
   ```
   git clone https://github.com/Yash-Vekaria/CookieAnalysis.git
   ```
2. Grant full permission to all the files in the ```CookieAnalysis``` directory (if you get ```permission denied:``` error) as follows:
   ```
   chmod -R 777 CookieAnalysis/
   ```
3. Change directory to CookieAnalysis
   ```
   cd CookieAnalysis
   ```
4. Ensure that the cookie log file CSV exists in the same directory as the ```most_active_cookie``` file.
5. Provide the name of the CSV log file as a positional command line argument and the query date with ```-d``` flag.
6. Finally run the code as mentioned in the instructions document provided by Quantcast.
7. Unit Tests can be run for the implementation as follows:
   ```
   python test.py
   ```

The report regarding this assignment explaining approach, code, and the testing scenarios can be referred to in the file: ```Quantcast Summer Internship 2024 Report.pdf```.
