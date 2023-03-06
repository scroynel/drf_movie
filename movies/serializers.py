from rest_framework import serializers

from .models import Movie, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data): # data это наш queryset
        data = data.filter(parent=None)
        return super().to_representation(data) # возвращаем родительский метод класса 

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value): # value - значение одной записи из БД
        serializer = self.parent.parent.__class__(value, context=self.context) # ищим всех детей, который завязаны на нашем отзыве
        return serializer.data


class MovieListSerailizer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


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


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft',) # все поля кроме draft(черновик)


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    # validated_data - данные который передаем в наш сериализатор с клиентской стороны
    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={ 'star': validated_data.get('star')}, # обновлять будем поле star
        )
        return rating # возвращаем полученную запись
    
