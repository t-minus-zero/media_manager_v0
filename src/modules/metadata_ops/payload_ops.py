from src.modules.local_ops.os_ops import OSFileManager
from src.modules.local_ops.json_ops import JSONFileManager
from src.modules.utility_ops.utility_ops import UtilityOps
import uuid


class PayloadOps:

    @staticmethod
    def create_payload(jobs):
        payload = {
            'info': {
                'payload-id' : str(uuid.uuid4()),
                'status' : 'queued',
                'job-index' : 0,
                'job-count' : len(jobs)
            },
            'jobs': jobs
        }
        return payload
    
    @staticmethod
    def create_jobs(items):
        jobs = [PayloadOps.create_job(item['item-data'], item['version-index']) for item in items]
        return jobs
        

    @staticmethod
    def create_job(item_data, version_index, procedures):
        print("item data edits: " + str(item_data['versions'][version_index]['edits']))
        job = {
            'item-data': item_data,
            'version-index' : version_index,
            'status' : 'queued',
            'edits' : [edit for edit in item_data['versions'][version_index]['edits'] if edit['status'] != 'completed']
        }

        for edit in job['edits']:
            # Assign the procedure directly as a dictionary instead of a list containing one item
            matching_procedure = next((procedure for procedure in procedures if procedure['info']['name'] == edit['name']), None)
            if matching_procedure:
                edit['procedure'] = matching_procedure
            else:
                edit['procedure'] = {}

        return job        

    
    