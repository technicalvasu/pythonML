from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(request):
    person={'name':'vasu', 'title':'leader'}
    y_pred = regressor.predict(X_test)
    return Response(person)