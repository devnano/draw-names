from django.db import models
import uuid

# Create your models here.


class Participant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DrawNames(models.Model):
    shuffled = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

    def shuffle(self):
        # assign a to_participant to each from_participant
        draw_names = self.drawname_set.all().order_by("exclude_participant_id")
        all_to_participants_pks = []
        for draw_name in draw_names:
            # print(draw_name.from_participant.pk)
            exclude = [draw_name.from_participant.pk] + all_to_participants_pks + ([] if not draw_name.exclude_participant else [draw_name.exclude_participant.pk])
            # print(exclude)
            to_participant = Participant.objects.exclude(pk__in=exclude).order_by("?").first()
            all_to_participants_pks += [to_participant.pk]
            draw_name.to_participant = to_participant
            # print(f"from {draw_name.from_participant.name} to {draw_name.to_participant.name}")
            draw_name.save()
        self.shuffled = True
        self.save()

    def __str__(self):
        return self.name


class DrawName(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    draw_names = models.ForeignKey(DrawNames, on_delete=models.CASCADE)
    exclude_participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="as_exclude_participants")
    from_participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="as_from_participants")
    to_participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="as_to_participants")
    wished_gift = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.from_participant.name} -> {self.to_participant.name}"
