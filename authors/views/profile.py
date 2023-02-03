from django.views.generic import TemplateView
# class based view q exige template
from django.shortcuts import get_object_or_404
from authors.models import Profile


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, *args, **kwargs):
        # se a gente quiser sobrescrever o contexto, usamos o método get
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')

        # se quisermos usar o select/prefetch_related temos q fazer
        # dessa maneira abaixo
        profile = get_object_or_404(Profile.objects.filter(
            pk=profile_id,
        ).select_related('author'), pk=profile_id)

        # render_to_response tá passando o contexto
        return self.render_to_response({
            # desempacotamento
            **context,
            'profile': profile,
        })
