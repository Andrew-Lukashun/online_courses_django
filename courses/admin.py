from django.contrib import admin
from courses import models
from django.utils.html import format_html


class TopicDocumentInline(admin.StackedInline):
    model = models.TopicDocument
    extra = 0
    fields = ('name', 'file', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return models.TopicDocument.all_objects.get_queryset()


class CourseTopicInline(admin.StackedInline):
    model = models.CourseTopic
    extra = 0
    fields = ('title', 'description', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return models.CourseTopic.all_objects.get_queryset()


class CoursePartInline(admin.StackedInline):
    model = models.CoursePart
    extra = 0
    fields = ('title', 'description', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return models.CoursePart.all_objects.get_queryset()



@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'parts_count', 'deleted_at')
    list_filter = ('created_at', 'deleted_at')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'deleted_at', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CoursePartInline]

    def get_queryset(self, request):
        return models.Course.all_objects.get_queryset()

    def parts_count(self, obj):
        return obj.parts.all_objects.count()
    parts_count.short_description = 'Количество частей'


@admin.register(models.CoursePart)
class CoursePartAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'topics_count', 'deleted_at')
    list_filter = ('course', 'created_at', 'deleted_at')
    search_fields = ('title', 'description', 'course__title')
    fields = ('course', 'title', 'description', 'deleted_at', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CourseTopicInline]

    def get_queryset(self, request):
        return models.CoursePart.all_objects.get_queryset()

    def topics_count(self, obj):
        return obj.topics.all_objects.count()
    topics_count.short_description = 'Количество тем'


@admin.register(models.CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'part', 'course', 'created_at', 'documents_count', 'deleted_at')
    list_filter = ('part__course', 'created_at', 'deleted_at')
    search_fields = ('title', 'description', 'part__title', 'part__course__title')
    fields = ('part', 'title', 'description', 'deleted_at', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TopicDocumentInline]

    def get_queryset(self, request):
        return models.CourseTopic.all_objects.get_queryset()

    def course(self, obj):
        return obj.part.course
    course.short_description = 'Курс'

    def documents_count(self, obj):
        return obj.documents.all_objects.count()
    documents_count.short_description = 'Количество документов'


@admin.register(models.TopicDocument)
class TopicDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'part', 'course', 'created_at', 'file_link', 'deleted_at')
    list_filter = ('topic__part__course', 'created_at', 'deleted_at')
    search_fields = ('name', 'topic__title', 'topic__part__title', 'topic__part__course__title')
    fields = ('topic', 'name', 'file', 'deleted_at', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'file_link')

    def get_queryset(self, request):
        return models.TopicDocument.all_objects.get_queryset()

    def part(self, obj):
        return obj.topic.part
    part.short_description = 'Часть'

    def course(self, obj):
        return obj.topic.part.course
    course.short_description = 'Курс'

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Открыть файл</a>', obj.file.url)
        return '-'
    file_link.short_description = 'Файл'