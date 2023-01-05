"""
Program to create GDSN Catalogue Item Subscription (CIS) messages based on a list of supplier GLNS.
Author: Sjoerd Schaper - GS1 Nederland
"""
import csv
import sys
import time
import os
import random
import string

def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if len(sys.argv) > 1:
    source_file = sys.argv[1]
else:
    source_file = "test_file"

headers = ['gln_dr','gln_ds','tm']
infile = os.path.join('input', source_file + '.csv')

# Change this to the GLN of your data pool
data_pool_gln = '8712345013042'

cntr = 1
b_nr = 1

# To prevent overloading the data pool the messages are split up in batches  
batch_size = 100

batch = os.path.join('output', 'batch_001')
if not os.path.exists(batch):
    os.makedirs(batch)

with open(infile, 'r', encoding='utf-8', errors='ignore') as fp:

    reader = csv.DictReader(fp, fieldnames=headers, skipinitialspace=True)
    for row in reader:
        if row.get('gln_dr') != 'gln_dr':

            print(row.get('gln_ds'))
            time_sys = time.strftime("%Y-%m-%dT%H:%M:%S")
            timestr = time.strftime("%Y_%m_%dT%H_%M_%S")
            file_id = get_random_string(8)
            inst_id = get_random_string(8)
            if cntr % batch_size == 0:
                b_nr = b_nr + 1
                batch = os.path.join('output', 'batch_' + str(b_nr).zfill(3))
                if not os.path.exists(batch):
                    os.makedirs(batch)
            file_name = os.path.join(batch, f'CIS_{source_file.upper()}_{row.get("gln_dr")}_{row.get("gln_ds")}_{file_id}.xml')
            outfile = open(str(file_name), "w", encoding='utf-8')
            outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
            outfile.write('<catalogue_item_subscription:catalogueItemSubscriptionMessage xmlns:catalogue_item_subscription="urn:gs1:gdsn:catalogue_item_subscription:xsd:3" xmlns:sh="http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:gs1:gdsn:catalogue_item_subscription:xsd:3 http://www.gdsregistry.org/3.1/schemas/gs1/gdsn/CatalogueItemSubscription.xsd">\n')
            outfile.write('<sh:StandardBusinessDocumentHeader>\n')
            outfile.write('<sh:HeaderVersion>1.0</sh:HeaderVersion>\n')
            outfile.write('<sh:Sender>\n')
            outfile.write(f'<sh:Identifier Authority="GS1">{row.get("gln_dr")}</sh:Identifier>\n')
            outfile.write('</sh:Sender>\n')
            outfile.write('<sh:Receiver>\n')
            outfile.write(f'<sh:Identifier Authority="GS1">{data_pool_gln}</sh:Identifier>\n')
            outfile.write('</sh:Receiver>\n')
            outfile.write('<sh:DocumentIdentification>\n')
            outfile.write('<sh:Standard>GS1</sh:Standard>\n')
            outfile.write('<sh:TypeVersion>3.1</sh:TypeVersion>\n')
            outfile.write(f'<sh:InstanceIdentifier>CIS_{row.get("gln_dr")}_{timestr}_{inst_id}</sh:InstanceIdentifier>\n')
            outfile.write('<sh:Type>catalogueItemSubscription</sh:Type>\n')
            outfile.write(f'<sh:CreationDateAndTime>{time_sys}</sh:CreationDateAndTime>\n')
            outfile.write('</sh:DocumentIdentification>\n')
            outfile.write('</sh:StandardBusinessDocumentHeader>\n')

            # transactiom
            trans_id = get_random_string(8)
            outfile.write('<transaction>\n')
            outfile.write('<transactionIdentification>\n')
            outfile.write(f'<entityIdentification>CIS_ADD_{row.get("gln_dr")}_{trans_id}</entityIdentification>\n')
            outfile.write('<contentOwner>\n')
            outfile.write(f'<gln>{row.get("gln_dr")}</gln>\n')
            outfile.write('</contentOwner>\n')
            outfile.write('</transactionIdentification>\n')

            # document
            doc_id = get_random_string(8)
            outfile.write('<documentCommand>\n')
            outfile.write('<documentCommandHeader type="ADD">\n')
            outfile.write('<documentCommandIdentification>\n')
            outfile.write(f'<entityIdentification>CIS_ADD_{row.get("gln_dr")}_{doc_id}</entityIdentification>\n')
            outfile.write('<contentOwner>\n')
            outfile.write(f'<gln>{row.get("gln_dr")}</gln>\n')
            outfile.write('</contentOwner>\n')
            outfile.write('</documentCommandIdentification>\n')
            outfile.write('</documentCommandHeader>\n')
            outfile.write('<catalogue_item_subscription:catalogueItemSubscription>\n')
            outfile.write(f'<creationDateTime>{time_sys}</creationDateTime>\n')
            outfile.write('<documentStatusCode>ORIGINAL</documentStatusCode>\n')
            outfile.write('<catalogueItemSubscriptionIdentification>\n')
            outfile.write(f'<entityIdentification>Subscription_{row.get("gln_ds")}_{row.get("tm")}_{doc_id}</entityIdentification>\n')
            outfile.write('<contentOwner>\n')
            outfile.write(f'<gln>{row.get("gln_dr")}</gln>\n')
            outfile.write('</contentOwner>\n')
            outfile.write('</catalogueItemSubscriptionIdentification>\n')
            outfile.write(f'<dataRecipient>{row.get("gln_dr")}</dataRecipient>\n')
            outfile.write(f'<dataSource>{row.get("gln_ds")}</dataSource>\n')
            outfile.write('<targetMarket>\n')
            outfile.write(f'<targetMarketCountryCode>{row.get("tm")}</targetMarketCountryCode>\n')
            outfile.write('</targetMarket>\n')
            outfile.write('</catalogue_item_subscription:catalogueItemSubscription>\n')
            outfile.write('</documentCommand>\n')
            outfile.write('</transaction>\n')
            cntr = cntr + 1

            outfile.write('</catalogue_item_subscription:catalogueItemSubscriptionMessage>\n')
            outfile.close()

