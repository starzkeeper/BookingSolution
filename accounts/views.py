from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
