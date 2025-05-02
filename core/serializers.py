from rest_framework import serializers
from .models import ExecutiveMember, Event, PersonalityOfTheWeek, Sermon, Member, Profile
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    # User fields
    password  = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    # Profile fields (write-only)
    other_names     = serializers.CharField(write_only=True, required=False, allow_blank=True)
    gender          = serializers.ChoiceField(choices=Profile.GENDER_CHOICES, write_only=True, required=False)
    date_of_birth   = serializers.DateField(write_only=True, required=False)
    student_id      = serializers.CharField(write_only=True, required=True)
    phone           = serializers.CharField(write_only=True, required=False, allow_blank=True)
    programme       = serializers.CharField(write_only=True, required=False, allow_blank=True)
    graduation_year = serializers.IntegerField(write_only=True, required=False)
    residence       = serializers.CharField(write_only=True, required=False, allow_blank=True)
    home_residence  = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model  = User
        # Only include real User fields in the output
        fields = [
            'username','email','password','password2',
            'first_name','last_name',
            # extra profile fields declared as write-only
            'other_names','gender','date_of_birth','student_id',
            'phone','programme','graduation_year','residence','home_residence',
        ]

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Extract profile data
        profile_data = {
            'other_names':     validated_data.pop('other_names', ''),
            'gender':          validated_data.pop('gender', ''),
            'date_of_birth':   validated_data.pop('date_of_birth', None),
            'student_id':      validated_data.pop('student_id'),
            'phone':           validated_data.pop('phone', ''),
            'programme':       validated_data.pop('programme', ''),
            'graduation_year': validated_data.pop('graduation_year', None),
            'residence':       validated_data.pop('residence', ''),
            'home_residence':  validated_data.pop('home_residence', ''),
        }

        # Create the user
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Populate the Profile
        Profile.objects.filter(user=user).update(**profile_data)
        return user

class NullableImageField(serializers.ImageField):
    """
    Custom ImageField that treats empty string and None as no file.
    """
    def to_internal_value(self, data):
        if data in ('', None):
            return None
        return super().to_internal_value(data)

class ExecutiveMemberSerializer(serializers.ModelSerializer):
    photo = NullableImageField(required=False, allow_null=True)

    class Meta:
        model = ExecutiveMember
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    image = NullableImageField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = '__all__'

class PersonalityOfTheWeekSerializer(serializers.ModelSerializer):
    photo = NullableImageField(required=False, allow_null=True)

    class Meta:
        model = PersonalityOfTheWeek
        fields = '__all__'

class SermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sermon
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'other_names',
            'gender',
            'date_of_birth',
            'student_id',
            'phone',
            'programme',
            'graduation_year',
            'residence',
            'home_residence',
        ]

class UserSerializer(serializers.ModelSerializer):
    # nest the ProfileSerializer, read-only
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile',
        ]
        read_only_fields = ['id', 'username']

