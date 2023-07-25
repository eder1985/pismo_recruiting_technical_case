from faker import Faker
from faker.providers import BaseProvider
from datetime import datetime
from json import dumps
import pandas as pd
import random
import collections
import glob
import os

class ProjectDomainProvider(BaseProvider):
    def project_domain_name(self):
        list_project_domain_names = ['account','transaction']
        return random.choice(list_project_domain_names)

class StatusTypeProvider(BaseProvider):
    def status_type(self):
        list_status_types = ['ACTIVE','INACTIVE','SUSPENDED','BLOCKED', 'DELETED']
        return random.choice(list_status_types)

class CustomUUIDProvider(BaseProvider):
    def custom_uuid(self):
        list_uuids = [
            '1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a',
            '2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b'
            ]
        return random.choice(list_uuids)

def write_fake_data(fake, length, destination_path, unique_uuid = True):

    database = []
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = 'fake_events_'+current_time

    for x in range(length):
        uuid = fake.uuid4() if unique_uuid else fake.custom_uuid()
        project_domain_name = fake.project_domain_name()
        event_type = project_domain_name + "-status-change"

        database.append(collections.OrderedDict([
            ('event_id', uuid),
            ('timestamp', datetime.strftime(fake.date_time_between(start_date='-3y', end_date='now'),"%Y-%m-%dT%H:%M:%S")),
            ('domain', project_domain_name),
            ('event_type', event_type),
            ('data', collections.OrderedDict([
                ('id', fake.random_number(digits=6)),
                ('old_status', fake.status_type()),
                ('new_status', fake.status_type()),
                ('reason', fake.sentence(nb_words=5))
            ]))
        ]))

    with open('%s%s.json' % (destination_path, filename), 'w') as output:
        output.write(dumps(database, indent=4, sort_keys=False, default=str))

    print("Done.")

def read_fake_data(json_filepath):
    json_files = [os.path.normpath(i) for i in glob.glob(json_filepath)]
    df = pd.concat([pd.read_json(f) for f in json_files])
    return df

def run(unique_uuid = True):
    fake = Faker()
    Faker.seed(random.randrange(0, 99999999999999999999, 1))
    fake.add_provider(ProjectDomainProvider)
    fake.add_provider(StatusTypeProvider)
    fake.add_provider(CustomUUIDProvider)

    length = 10
    destination_path = 'C:/Users/Eder/Documents/EDER/projetos/pismo_recruiting_technical_case/work/data/raw/events/'
    write_fake_data(fake, length, destination_path,unique_uuid)

    json_filepath = destination_path+'*.json'
    fake_data = read_fake_data(json_filepath)
    print(fake_data)

#run()
run(unique_uuid = False)