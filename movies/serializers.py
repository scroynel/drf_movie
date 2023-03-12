from rest_framework import serializers

from .models import Movie, Review, Rating, Actor

from django.db.models import Avg


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data): # data это наш queryset
        data = data.filter(parent=None)
        return super().to_representation(data) # возвращаем родительский метод класса 

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value): # value - значение одной записи из БД
        serializer = self.parent.parent.__class__(value, context=self.context) # ищим всех детей, который завязаны на нашем отзыве
        return serializer.data


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerailizer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user', 'middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('ip', 'star', 'movie')

    # validated_data - данные который передаем в наш сериализатор с клиентской стороны
    def create(self, validated_data):
        # запись будет записана в rating, а true или false будет дабавлена в _
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={ 'star': validated_data.get('star')}, # обновлять будем поле star
        )
        return rating # возвращаем полученную запись

class MiddleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star',)

    
        

class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reviews = ReviewSerializer(many=True)
    ratings = CreateRatingSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating 

    class Meta:
        model = Movie
        exclude = ('draft',) # все поля кроме draft(черновик)




    
