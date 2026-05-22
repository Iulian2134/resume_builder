from django.contrib import admin
from .models import Template, Resume, Education, Experience, Skill, Announcement


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_name', 'job_title', 'user', 'updated_at')
    list_filter = ('template', 'created_at', 'updated_at')
    search_fields = ('title', 'full_name', 'job_title', 'email', 'phone')
    inlines = [ExperienceInline, EducationInline, SkillInline]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'body')


admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
