import random
import string

from fake_web_server import FakeWebServer, add_route
from flask import jsonify

from books import Book
from database import DictDataBase
from api.exceptions import ItemNotExist
from api.helpers import get_args_from_req
from validations import validate_book_args


class WebServerBooks(FakeWebServer):
    def __init__(self):
        super().__init__()
        self.database = DictDataBase()

    @add_route('/', ['GET'])
    def welcome(self):
        return jsonify('welcome'), 200

    @add_route('/books/<book_id>', methods=(["GET"]))
    def get_book_by_id(self, book_id):
        try:
            book = self.database.get_one(book_id)
        except ItemNotExist as e:
            return f"error: {e}", 404
        except Exception as e:
            return f"error: {e}", 500
        return jsonify(book), 200

    @add_route('/books/', methods=(["GET"]))
    def get_books(self):
        try:
            books = self.database.get_all()
        except Exception as e:
            return f"error: {e}", 400
        return jsonify(books), 200

    @add_route('/books/', methods=(["POST"]))
    def post_book(self):
        try:
            args = get_args_from_req()
            validate_book_args(args)
            book_dict = args["book"]
            new_book = Book(**book_dict)
            self.database.insert_one(new_book)
        except Exception as e:
            return jsonify(e), e.status_code
        except KeyError:
            return jsonify(f"msg: Missing crucial required args - _id , amount, state"), 400
        return jsonify(f"Post book success: {new_book.book_id}"), 201

    @add_route('/books/<book_id>', methods=(["PUT"]))
    def update_book_by_id(self, book_id):
        try:
            args = get_args_from_req()
            validate_book_args(args)
            self.database.update_one(book_id, args)
        except ItemNotExist as e:
            return f"error: {e}", 404
        except KeyError as e:
            return f"error: key doesn't exist: {e}", 400
        return jsonify(f'{book_id} was updated'), 200

    @add_route('/books/<book_id>', methods=(["DELETE"]))
    def delete_book_by_id(self, book_id):
        try:
            book = self.database.delete_one(book_id)
        except ItemNotExist as e:
            return f"error: {e}", 404
        return jsonify(f'Removed book is: {book}'), 200

    def reset_database(self):
        self.database = DictDataBase()

    # @add_route("/list_clusters")
    # def list_clusters(self):
    #     return {'Clusters': [{'name': cluster_name,
    #                           'cluster_id': config['cluster_id'],
    #                           'cluster_conf': config['cluster_conf'],
    #                           'desired_state': config['desired_state'],
    #                           'actual_state': config['actual_state'],
    #                           'aws_state_change_reason': config.get('aws_state_change_reason',
    #                                                                 DEFAULT_CLUSTER_STATE_CHANGE_REASON)}
    #                          for cluster_name, config in self.clusters.items()]}
    #
    # @add_route("/restart_cluster", methods=['POST'])
    # def restart_cluster(self):
    #     cluster_name = request.args['cluster_name']
    #     cluster_id = generate_cluster_id()
    #     self.clusters[cluster_name]['cluster_id'] = cluster_id
    #     self.clusters[cluster_name]['actual_state'] = ClusterActualState.RUNNING.name
    #     return {'msg': f'Cluster {cluster_id} is starting', 'platform_tracking_url': 'http:....'}
    #
    # @add_route("/terminate_cluster", methods=['POST'])
    # def terminate_cluster(self):
    #     cluster_name = request.args['cluster_name']
    #     del self.clusters[cluster_name]
    #     return jsonify({'msg': 'cluster terminated successfully'})
    #
    # @add_route("/list_apps")
    # def list_apps(self):
    #     cluster_name = request.args['cluster_name']
    #     if not self.clusters.get(cluster_name):
    #         return jsonify({"Applications": []})
    #     apps = list(self.clusters[cluster_name].get('applications', []).values())
    #     return jsonify({"Applications": apps})
    #
    # @add_route("/start_app", methods=['POST'])
    # def start_app(self):
    #     cluster_name = request.args['cluster_name']
    #     application_name = request.args['app_name']
    #     app = {application_name: {'app_params': request.json['app_params'],
    #                               'desired_state': AppDesiredState.Running.value,
    #                               'actual_state': AppActualState.RUNNING.value,
    #                               'name': application_name,
    #                               'cluster_name': cluster_name,
    #                               'batch_id': generate_application_id()}}
    #     self.clusters[cluster_name]['applications'].update(app)
    #     return jsonify({'msg': f'Application {application_name} is starting in cluster {cluster_name}, ',
    #                     'platform_tracking_url': f"...",
    #                     'livy_url': '...'})
    #
    # @add_route("/restart_app", methods=['POST'])
    # def restart_app(self):
    #     cluster_name = request.args['cluster_name']
    #     application_name = request.args['app_name']
    #     app = self.clusters[cluster_name]['applications'][application_name]
    #     app['actual_state'] = AppActualState.RUNNING.value
    #     self.clusters[cluster_name]['applications'].update(app)
    #     return jsonify({'msg': f'Application {application_name} is Re-starting in cluster {cluster_name}, ',
    #                     'platform_tracking_url': "...",
    #                     'livy_url': '...'})
    #
    # @add_route("/kill_app", methods=['POST'])
    # def kill_app(self):
    #     cluster_name = request.args['cluster_name']
    #     application_name = request.args['app_name']
    #     del self.clusters[cluster_name]['applications'][application_name]
    #     return jsonify({'msg': ''})
    #
    # @add_route("/remove_app", methods=['POST'])
    # def remove_app(self):
    #     cluster_name = request.args['cluster_name']
    #     application_name = request.args['app_name']
    #     del self.clusters[cluster_name]['applications'][application_name]
    #     return jsonify({'msg': 'app removed from db'})
    #
    # def set_cluster_actual_state(self, cluster_name: str, cluster_state: ClusterActualState):
    #     self.clusters[cluster_name]['actual_state'] = cluster_state.name
    #
    # def set_aws_state_change_reason(self, cluster_name: str,
    #                                 aws_state_change_reason: str = DEFAULT_CLUSTER_STATE_CHANGE_REASON):
    #     self.clusters[cluster_name]['aws_state_change_reason'] = aws_state_change_reason
    #
    # def set_app_actual_state(self, cluster_name: str, app_name: str, app_state: AppActualState):
    #     self.clusters[cluster_name]['applications'][app_name]['actual_state'] = app_state.value
    #


def generate_cluster_id():
    cluster_id = ''.join(random.choices(string.ascii_uppercase, k=13))
    return f'j-{cluster_id}'


def generate_application_id():
    return str(random.randint(1, 100))
