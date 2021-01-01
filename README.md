# internship :
A file based key-value data store that supports the basic CRD(create-read-delete) operations.

## Functional Requirement Checklist :
- [x]  It can be initialized using an optional file path.If one is not provided, then it will reliably create itself in "py" folder.
- [x] A new key-value pair can be added to the data store using the Create operation. The key = a string = 32chars = always. The value = Valid JSON object = 16KB = always.
- [x] duplicate_keyFound_error if create is invoked for an existing key.
- [x] read/get operation on a key results in retrieval of valid value in the form of associated JSON Object.
- [x] delete/remove operation clears key-value pair 
- [x] Every key supports setting a Time-To-Live property with default value of 2592000 seconds(30 days).
- [x] Appropriate error responses with the help of raise keyword in the python.

## Non-Functional Requirement Checklist :
- [x] The size of the file storing data must never exceed 1 GB.
- [ ] More than one client process cannot be allowed to use the same file as a data Store at any given time. 
- [ ] Tried to achieve **thread-safe** operations on Data Store by wrapping all write operations like "set", "rem", etc. with a thread lock but needs some fine tuning.
- [x] With the autodump=True/False feature , the database will not/be written to the file after each operation. This minimizes write I/O operation.

## Submission :
- unit tests performed for create , read , delete operation of the key.
- Development is entirely made on windows machine and have used filepath. Needs little tweaking in terms of filepath on Linux.
