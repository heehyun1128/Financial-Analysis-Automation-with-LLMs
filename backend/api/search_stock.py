# Example Flask endpoint in your backend
from flask import Flask, request, jsonify, Blueprint
from ..utils.perform_rag import perform_rag_query
from ..utils.get_data import get_stock_info



index_name = "stocks"
namespace = "stock-descriptions"

search_routes = Blueprint('search_routes', __name__)

@search_routes.route('/', methods=['POST'])
def search_stocks():
    data = request.json
    search_query = data.get('searchTerm')

    result=perform_rag_query(search_query, index_name, namespace)
    return jsonify(result)