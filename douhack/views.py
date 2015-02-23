from django.views.generic import TemplateView


class IndexView(TemplateView):
    """View to show landing (index) page of the site
    """
    template_name = 'index.html'

