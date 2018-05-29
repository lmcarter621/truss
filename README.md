# Truss Exercise

## Running the application

From the command line, 
1.  Navigate to the location that you've cloned the git repo. 
2.  Run ```python data_adapter.py {filename}```
3.  The results will be located in "results/cleansed_data_{datetime}"

## Notes
* The notes column doesn't convert invalid UTF-8 characters
* Time did not permit for tests, but under normal conditions I would write tests for all the conditions laid out in the original readme
* This exercise has been scoped according to the requirements, in large scope and scaled project, I would expect that 
   ** the files would be dropped in a static location where they could be read from
   ** there would be a single location where the files would all be written to
   ** There would be more data adapations that would require each class to have it's own file
* I chose Python as opposed to Java or Rails because of it is lightweight.  Java would have been too much overhead for the minimal calculations that needed to be done.  Rails would have been a lot of framework to place around a data adapter.
