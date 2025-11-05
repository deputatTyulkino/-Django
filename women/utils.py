class DataMixin:
    title_page = None
    cat_id = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_id is not None:
            self.extra_context['cat_id'] = self.cat_id

    def get_mixin_context(self, context, **kwargs):
        # context['menu'] = ...
        context['cat_id'] = None
        context.update(kwargs)
        return context
