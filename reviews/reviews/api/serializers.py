from rest_framework import serializers

from reviews.models import Survey, Question, QuestionChoice, Answer


class QuestionSerializer(serializers.ModelSerializer):
    """ Question serializer class """

    name = serializers.CharField(max_length=100)
    question_type = serializers.CharField()
    question_text = serializers.CharField()

    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, attrs):
        types = ['TEXT', 'ONE', 'ONE_CHOICE', 'MULTIPLE', 'MULTIPLE_CHOICE']
        question_type = attrs['question_type']
        if question_type in types:
            return attrs
        raise serializers.ValidationError('Wrong question type')

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """ Question choice acceptable answers serializer """

    question = QuestionSerializer
    question_text = serializers.CharField(max_length=100)

    class Meta:
        model = QuestionChoice
        fields = '__all__'

    def validate(self, attrs):
        try:
            QuestionChoice.objects.get(question=attrs['question'].id, choice_text=attrs['choice_text'])
        except QuestionChoice.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Question choice already exist')

    def create(self, validated_data):
        return QuestionChoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SurveySerializer(serializers.ModelSerializer):
    """ Create survey serializer """

    title = serializers.CharField(max_length=100)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'

    def create(self, validated_data):
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'start_time' in validated_data:
            raise serializers.ValidationError('You cannot make changes')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    """ Answer serializer class """

    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    question_choice = QuestionChoiceSerializer(read_only=True)
    answer_text = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
