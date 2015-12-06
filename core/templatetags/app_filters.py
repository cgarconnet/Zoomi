from django import template

register = template.Library()

@register.filter(name='filter_list')
def filter_list(things):
    return things.all()
    # the code .filter(section=1) works well already
		# return coremodels.Entry.objects.filter(Q(user=self.request.user, transfered=0) | Q(assignees=self.request.user), done=0)
