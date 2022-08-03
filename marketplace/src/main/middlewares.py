from .models import SubRubric


def marketplace_context_processor(request):
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    return context
