import os
import jwt
import uuid
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.models import Exercise,CustomUser,RecentlySelectedExercise,UserPlan,Queries
import json
from .serializers import ExerciseSerializer, BodyPartSerializer,WorkshopSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django_filters import rest_framework as filters
import httpx
from Workshops.models import Workshop
import random
from rest_framework import status

class AllExerciseAPIView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseAPIView(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    lookup_field = 'id'

class FilterBodyPartAPIView(APIView):
    def get(self,request,bodypart):
        print(bodypart)
        q= Exercise.objects.filter(bodyPart=bodypart)
        serializer = ExerciseSerializer(q,many=True)
        return Response(serializer.data)

class FilterTarget(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('target','bodyPart','equipment')

class BodyPartsAPIView(APIView):
    def get(self, request):
        bodyParts = []
        obj = Exercise.objects.values('bodyPart').distinct()
        serializers = BodyPartSerializer(obj, many=True)
        data = json.loads(json.dumps(serializers.data))
        for item in data:
            bodyParts.append(item["bodyPart"])
        return Response(bodyParts)

class FavouritesAPIView(APIView):
    def get(self,request):
        # user = CustomUser.objects.get(id=request.GET.get("user_id"))
        fav = request.user.favourites.all()
        serializers = ExerciseSerializer(fav, many=True)
        return Response(serializers.data)

    def post(self,request):
        if (request.GET.get('action') == "add"):
            # user = CustomUser.objects.get(id=request.GET.get("user_id"))
            ex = Exercise.objects.get(id=request.GET.get("ex_id"))
            request.user.favourites.add(ex)
            fav = request.user.favourites.all()
            serializers = ExerciseSerializer(fav, many=True)
            return Response({"exercises": serializers.data,
                             "message": "Added to Favourites"})
        if (request.GET.get('action') == "remove"):
            # user = CustomUser.objects.get(id=request.GET.get("user_id"))
            ex = Exercise.objects.get(id=request.GET.get("ex_id"))
            request.user.favourites.remove(ex)
            fav = request.user.favourites.all()
            serializers = ExerciseSerializer(fav, many=True)
            return Response({"exercises": serializers.data,
                             "message": "Removed from Favourites"})

def getManagementToken():
    app_access_key = os.environ.get('MS_ACCESS_KEY')
    app_secret = os.environ.get('MS_APP_SECRET')
    expires = 24 * 3600
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(seconds=expires)
    token = jwt.encode(payload={
        'access_key': app_access_key,
        'type': 'management',
        'version': 2,
        'jti': str(uuid.uuid4()),
        'iat': now,
        'exp': exp,
        'nbf': now
    }, key=app_secret)

    return token


class AllRooms(APIView):
    def get(self,request):
        rooms = Workshop.objects.all()
        serializers = WorkshopSerializer(rooms,many=True)
        return Response({"rooms":serializers.data})


class GetRoomCode(APIView):
    def get(self,request,role,roomId):
        token=getManagementToken()
        r= httpx.post(f"https://api.100ms.live/v2/room-codes/room/{roomId}/role/{role}" ,headers={"Authorization": f'Bearer {token}'})
        # print(r.json())
        return Response(r.json())


class ExercisePlanGeneratorAPIView(APIView):
    EXERCISES_PER_DAY = 5
    DAYS_IN_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    REST_DAYS = []
    RECENTLY_SELECTED_LIMIT = 20  # Number of previous workouts to consider for randomization constraint

    def post(self, request, format=None):
        user_preferences = request.data.get('preferences', {})
        print(user_preferences)
        self.EXERCISES_PER_DAY = user_preferences["workoutTime"]//15
        exercise_plan = self.generate_exercise_plan(user_preferences)
        return Response(exercise_plan)

    def generate_exercise_plan(self, user_preferences):
        exercise_plan = {}


        if (len(user_preferences["days"]) == 7):
            print(self.REST_DAYS)
            self.REST_DAYS.append("Sunday")

        for day in user_preferences["days"]:
            print("RESTTTTTTTTTTT",self.REST_DAYS)
            print("USERRRRRRRRRRR",user_preferences["days"])
            if day in self.REST_DAYS:
                exercise_plan[day] = []
            else:
                data=self.select_exercises(user_preferences)
                serializer = ExerciseSerializer(data,many=True)
                print(day,serializer.data)
                exercise_plan[day] = serializer.data
        return exercise_plan

    def select_exercises(self, user_preferences):
        exercises = Exercise.objects.all()
        recently_selected_exercises = self.get_recently_selected_exercises()

        # Apply filters based on user preferences
        if 'equipment' in user_preferences:
            exercises = exercises.filter(equipment=user_preferences['equipment'])
            print("EQUIPMENT",exercises.count())

        if 'body_parts' in user_preferences:
            bodypart_exercises = exercises.filter(bodyPart=user_preferences['body_parts'])
            print("BODYPARTS",bodypart_exercises.count())

        if 'target_muscles' in user_preferences:
            target_exercises = exercises.filter(target=user_preferences['target_muscles'])
            print("TARGET",target_exercises.count())

        exercises= bodypart_exercises.union(target_exercises)
        print("filtered exercises",exercises.count())
        # Assign weights to muscle groups and exercise types
        weights = {
            'chest': 3,
            'back': 3,
            'legs': 3,
            'shoulders': 2,
            'arms': 2,
            'abs': 1,
            'cardio': 1,
            'waist': 1
        }

        # Select exercises based on weighted scores and randomization constraint
        filtered_exercises = self.filter_exercises_by_randomization(exercises, recently_selected_exercises)
        if not filtered_exercises:
            return []
        scored_exercises = self.assign_scores(filtered_exercises, weights)

        selected_exercises = []
        for _ in range(self.EXERCISES_PER_DAY):
            exercise = self.select_exercise(scored_exercises)
            selected_exercises.append(exercise)
            # Create a new entry in the RecentlySelectedExercise table
            RecentlySelectedExercise.objects.create(exercise=exercise)


        return [exercise for exercise in selected_exercises]

    def get_recently_selected_exercises(self):
        recently_selected = RecentlySelectedExercise.objects.order_by('-timestamp')[:self.RECENTLY_SELECTED_LIMIT]
        print( "Recently",recently_selected.count())
        return [recently.exercise.name for recently in recently_selected]
    def filter_exercises_by_randomization(self, exercises, recently_selected_exercises):
        # Filter exercises to exclude the ones present in the recently selected exercises
        filtered_exercises = [exercise for exercise in exercises if exercise.name not in recently_selected_exercises]
        print("Randomization",len(filtered_exercises))
        return filtered_exercises

    def assign_scores(self, exercises, weights):
        # Assign scores to exercises based on weights for muscle groups and exercise types
        scored_exercises = []
        for exercise in exercises:
            score = 0
            if exercise.target in weights:
                score += weights[exercise.target]
            if exercise.bodyPart in weights:
                score += weights[exercise.bodyPart]
            scored_exercises.append((exercise, score))
        return scored_exercises

    def select_exercise(self,scores):
        total_score = sum(score for exercise, score in scores)
        weighted_choices = [(exercise, score / total_score) for exercise, score in scores]
        selected_exercise = random.choices(population=[exercise for exercise, _ in scores],
                                           weights=[weight for _, weight in weighted_choices])[0]
        return selected_exercise


class PlanByUser(APIView):
    def post(self,request):
        plan_json = json.dumps(request.data.get("plan"))

        if UserPlan.objects.filter(user=request.user).exists():
            if (request.GET.get("plan_type") == "exercise"):
                plan = UserPlan.objects.get(user=request.user)
                plan.exercise_plan = plan_json
                plan.save()
                return Response("Exercise Plan Updated and Saved")
            if(request.GET.get("plan_type")=="meal"):
                plan = UserPlan.objects.get(user=request.user)
                plan.meal_plan = plan_json
                plan.save()
                return Response("Meal Plan Updated and Saved")
        else:
            if (request.GET.get("plan_type") == "exercise"):
                UserPlan.objects.create(user=request.user, exercise_plan=plan_json)
                return Response("Exercise Plan Saved")
            if (request.GET.get("plan_type") == "meal"):
                UserPlan.objects.create(user=request.user, meal_plan=plan_json)
                return Response("Meal Plan Saved")


    def get(self,request):

        if UserPlan.objects.filter(user=request.user).exists():
            user_plan = UserPlan.objects.get(user=request.user)
            exercise_plan = ""
            meal_plan = ""
            if(user_plan.exercise_plan):
                exercise_plan = json.loads(user_plan.exercise_plan)
            if(user_plan.meal_plan):
                meal_plan = json.loads(user_plan.meal_plan)
            return Response({"exercise":exercise_plan,"meal":meal_plan})
        else:
            return Response({"error":"No Exercise Plan"})

class PostQueries(APIView):
    def post(self,request):
        data = request.data
        Queries.objects.create(name=data["name"],email=data["email"],phone=data["phone"],subject=data["subject"],message=data["message"])
        return Response("Query Submitted.Our Team Will get Back to you shortly.")
