from ipproxy_pool.db.MongodbManager import mongodbManager
from ipproxy_pool.config.kafka_config import store_config
import logging

commit_fail_code = -17001
create_fail_code = -17002
save_fail_code = -17003
_logger = logging.getLogger('kafka-python')


class Mongo(object):

    def __init__(self):
        self.database = store_config['mongo_connect']['database']
        self.collection = store_config['mongo_connect']['collection']
        self.client = mongodbManager(database=self.database, collection=self.collection).mongo_collection()

    def get_offset(self, topic, partition, group_id):
        query = {'topic': topic, 'partition': partition, 'group_id': group_id}
        return self.client.find_one(query)

    def create_offset(self, topic, partition, group_id):
        try:
            self.client.insert_one({'topic': topic, 'partition': partition, 'group_id': group_id})
        except Exception as e:
            _logger.error(
                'code:{0} , topic:{1} , partition:{2} , group_id:{3} commit offset fail:{4}'.format(create_fail_code,
                                                                                                    topic, partition,
                                                                                                    group_id, e))

    def commit_offset(self, topic, partition, group_id, offset):
        try:

            field = {'current_offset': offset}

            self.client.update(
                {'topic': topic, 'partition': partition, 'group_id': group_id},
                {"$set": field}
            )
        except Exception as e:
            _logger.error(
                'code:{0} , topic:{1} , partition:{2} , group_id:{3} commit offset fail:{4}'.format(commit_fail_code,
                                                                                                    topic, partition,
                                                                                                    group_id, e))
