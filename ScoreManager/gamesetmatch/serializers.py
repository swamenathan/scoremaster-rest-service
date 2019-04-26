from rest_framework import serializers
from .models import *
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


    # def to_internal_value(self, data):
    #     validate_data = super(RegisterSerializer, self).to_internal_value(data)
    #     print(validate_data)
    #     validate_data['is_active'] = False
    #     print(validate_data)
    #     return validate_data
    #
    # def to_representation(self, instance):
    #     validated_data = super(RegisterSerializer, self).to_representation(instance)
    #     print('instance = ', instance)
    #     validated_data['is_active'] = instance['is_active']
    #     print('validated_data = ', validated_data)
    #     return validated_data

class PlayerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerProfile
        fields = ('id', 'division', 'seeding_points', 'rr_points')
        read_only_fields = ('player', )

    def create(self, validated_data):
        validated_data['player'] = self.context['request'].user
        super(PlayerProfileSerializer, self).create(validated_data)
        return validated_data


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'main_player', 'partner_player', 'seeding_points', 'rr_points')

    def validate(self, attrs):
        if 'partner_player' in attrs:
            if attrs['partner_player'] == self.context['request'].user:
                raise serializers.ValidationError("A team cannot have duplicate users")
        return attrs

    def to_internal_value(self, data):
        validated_data = super(TeamSerializer, self).to_internal_value(data)
        validated_data['main_player'] = self.context['request'].user
        return validated_data

    def validate_team_name(self, value):
        """
        Check if two team names are the same
        :param value:
        :return:
        """
        if Team.objects.filter(team_name=value):
            raise serializers.ValidationError("Team of the same name exits, choose another name")
        return value


    #TODO: Two teams cannot have the same members


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'
        read_only_field = ('match_uuid', )

    def to_internal_value(self, data):
        validated_data = super(MatchSerializer, self).to_internal_value(data)
        validated_data['player_id'] = self.context['request'].user
        return validated_data

    def to_representation(self, instance):
        validated_data = super(MatchSerializer, self).to_representation(instance)
        team_1 = Team.objects.filter(id=validated_data['team_1'])
        team_2 = Team.objects.filter(id=validated_data['team_2'])
        validated_data['team_1_name'] = team_1[0].team_name
        validated_data['team_2_name'] = team_2[0].team_name
        return validated_data


class TournamentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = '__all__'






