# Create GDSN CIS messages

Program to create GDSN Catalogue Item Subscription (CIS) messages for a data recipient based on a list of supplier GLNS.

**Usage:**
1. Create a csv file in the input directory with the structure
gln_dr,gln_ds,tm
8710626000002,8719333002682,528

gln_dr = GLN Data recipient
gln_ds = GLN Data source
tm = target_market

2. Run the program from the command prompt with the name of the csv-file as parameter
create_cis.py test_file

3. In the directory output a new directory will be created with the same name as the csv file.
   In the created directory there a one or more batches with CIS messages
   
4. Upload the xml files via FTP or AS2 to your GDSN data pool

5. Messages will be processed by the datapool
