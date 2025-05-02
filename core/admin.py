from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    Profile,
    ExecutiveMember,
    Event,
    PersonalityOfTheWeek,
    Sermon,
    Member,
    ContactMessage,
)

# 1️⃣ Unregister the default User admin, then re-register including profile inline
admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Extend the default UserAdmin to include our Profile inline"""
    inlines = (ProfileInline,)

# 2️⃣ Register your other models as before
@admin.register(ExecutiveMember)
class ExecutiveMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')

@admin.register(PersonalityOfTheWeek)
class PersonalityOfTheWeekAdmin(admin.ModelAdmin):
    list_display = ('name', 'week_date')

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
