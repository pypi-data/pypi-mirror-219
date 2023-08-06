# logger-local-python-package

# Initialize
run this command in the root directory of your project :

    pip install logger-local-python-package

# Import 
import instance from the package : 

from LoggerLocalPythonPackage.LoggerServiceSingleton import locallgr

# Usage
Note that you must have a .env file with the environment variables.

you can insert log into DB with 2 difference approach :

1. Writing a message :
    * locallgr.info("your-message");
    * locallgr.error("your-message");
    * locallgr.warn("your-message");
    * locallgr.debug("your-message");
    * locallgr.verbose("your-message");

2. Writing an object (Dictionary) :
    
   In case you have more properties to insert into the database,
   
   you can create a Dictionary object that contains the appropriate fields from the table and send it as a parameter.

   the Dictionary's keys should be the same as the table's columns names and the values should be with the same type as the table's columns types.

        objectToInsert = {
            'user_id': 1,
            'profile_id': 1,
            'activity': 'logged in the system',
            'payload': 'your-message',
        }

        locallgr.info(object=objectToInsert);
    
    None of the fields are mandatory.


Please add to requirements.txt
replace the x with the latest version in pypi.org/project/logger-local
logger-local==0.0.x

Please includ at least two Logger calls in each method:
"Start " + class.method names "( "+ parameters + ")";
"Start " + class.method names + " returned " + return values;

TOOD: We nee to add Unit Tests so this command will work
python -m unittest .\tests\test_writer.py


pip install -r .\requirements.txt