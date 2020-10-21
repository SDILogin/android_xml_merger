# android_xml_merger
Python util to merge project's xml files into single xml (without platform resources) 

### What is it
This is simple util to find new string in Android projects 

### How it works 
Util will walk through project directories (exclude "build") and collect string.xml files from default locale. 
Then all found xml files will be merged into single xml file. Util will try to find new strings in that new 
merged xml file. New string is a string that found in project, but not presented in base xml 

### How to run this util  
Assume that our base xml is localise.xml file with translated strings. We will try to 
determinate what strings we need to upload for localisation. 

Step 1: put `localise.xml` in a directory with `main.py`. `localise.xml` will be used as a base xml   
Step 2: choose an output file name. In our example it'll be `untranslated_strings.xml`  
Step 3: generate command like 

`$python3 main.py -p <path_to_android_project> --base-xml "localise.xml" --output "untranslated_strings.xml" --log-level DEBUG`
