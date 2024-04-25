from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import requests

from .serializers import InputSerializer, OutputSerializer

class PredictionAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InputSerializer(data=request.data, many=True)
        if serializer.is_valid():
            # Fetch the dataset from an external API
            try:
                response = requests.get('http://example.com/api/data')
                response.raise_for_status()
                data = response.json()
                dataset = pd.DataFrame(data)
            except requests.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Initialize OneHotEncoder with handle_unknown='ignore' to handle unseen categories
            ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(handle_unknown='ignore'), [0])], remainder='passthrough')
            X = ct.fit_transform(dataset.drop('timeSpentInOrderPreparation', axis=1))
            y = dataset['timeSpentInOrderPreparation'].values
            regressor = LinearRegression()
            regressor.fit(X, y)

            # Process each validated item one by one
            results = []
            for item in serializer.validated_data:
                item_df = pd.DataFrame([item])
                try:
                    X_item = ct.transform(item_df)  # Use transform(), not fit_transform()
                    y_pred = regressor.predict(X_item)
                    predicted_time = float(y_pred[0])
                except:
                    # If category is unseen and ignored, handle accordingly, e.g., use a default prediction
                    predicted_time = -1  # Example: Default or indicative value for unseen categories

                results.append({
                    "source": item["source"],
                    "timePredicted": predicted_time,
                    "score": 0 if predicted_time < 0 else None  # Set score as 0 for negative predictions immediately
                })

            # Sorting results by predicted time in ascending order and assigning scores
            results_valid = [result for result in results if result['timePredicted'] >= 0]
            results_sorted = sorted(results_valid, key=lambda x: x['timePredicted'])
            total_items = len(results_sorted)
            for i, result in enumerate(results_sorted):
                result['score'] = total_items - i  # Assigning scores to valid predictions

            output_serializer = OutputSerializer(results, many=True)  # Ensure to return all results, adjusted for scoring
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
