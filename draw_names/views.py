from django.shortcuts import render
from django.template import loader
from draw_names.models import DrawNames
from django.http import HttpResponse, HttpResponseRedirect

from django import forms


class WishedGitForm(forms.Form):
    wished_gift = forms.CharField(
        label="",
        max_length=200,
        widget=forms.Textarea(attrs={"rows": "5"}),
        required=False,
    )


def draw_name(request, uuid):
    draw = DrawNames.objects.first()
    if not draw.shuffled:
        draw.shuffle()

    draw_name = draw.drawname_set.get(uuid=uuid)
    draw_name_as_receiver = draw.drawname_set.get(
        to_participant__pk=draw_name.from_participant.pk
    )

    # uuid = request.get_full_path().split("/")[-1]
    if request.method == "GET":
        form = WishedGitForm(data={"wished_gift": draw_name_as_receiver.wished_gift})
        # uuid = request.GET.get("uuid", None)

    saved = False
    if request.method == "POST":
        form = WishedGitForm(request.POST)
        if form.is_valid():
            draw_name_as_receiver.wished_gift = form.cleaned_data.get(
                "wished_gift", None
            )
            draw_name_as_receiver.save()
            saved = True
    context = {
        "draw_name": draw_name,
        "uuid": uuid,
        "draw_name_as_receiver": draw_name_as_receiver,
        "form": form,
        "saved": saved,
    }
    template = loader.get_template("draw_name.html")

    return HttpResponse(template.render(context, request))
