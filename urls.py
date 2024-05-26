from app import app
from views import AdView, UserView

ad_view = AdView.as_view('advertisements')
user_view = UserView.as_view('users')

app.add_url_rule('/ad/show/<int:ad_id>', view_func=ad_view, methods=['GET'])
app.add_url_rule('/ad/<int:ad_id>', view_func=ad_view, methods=['DELETE'])
app.add_url_rule('/user/<int:user_id>/ad/<int:ad_id>', view_func=ad_view, methods=['PATCH'])
app.add_url_rule('/user/<int:user_id>/ad', view_func=ad_view, methods=['POST'])

app.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user', view_func=user_view, methods=['POST'])
