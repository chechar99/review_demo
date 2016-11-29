from __future__ import unicode_literals
from django.db import models

# Acceptance Criteria
# Users are able to submit reviews to the API
# Users are able to retrieve reviews that they submitted
# Users cannot see reviews submitted by other users
# Use of the API requires a unique auth token for each user
# Submitted reviews must include, at least, the following attributes:
# Rating - must be between 1 - 5
# Title - no more than 64 chars
# Summary - no more than 10k chars
# IP Address - IP of the review submitter
# Submission date - the date the review was submitted
# Company - information about the company for which the review was submitted,
# can be simple text (name, company id, etc.) or a separate model altogether
# Reviewer Metadata - information about the reviewer, can be simple text
# (e.g., name, email, reviewer id, etc.) or a separate model altogether


class Entity(models.Model):
    created_time = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True)
    updated_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Company(Entity):
    name = models.CharField(max_length=100)
    summary = models.TextField(max_length=10000)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Review(Entity):
    RATING_CHOICES = (
        (1, "1 Point (Bad)"),
        (2, '2 Points (Regular)'),
        (3, '3 Points (Good)'),
        (4, '4 Points (Very Good)'),
        (5, '5 Points (Excelent)'),
    )
    title = models.CharField(max_length=64)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    summary = models.TextField(max_length=10000)
    ip_address = models.GenericIPAddressField()
    reviewer = models.ForeignKey('auth.User')
    company = models.ForeignKey('Company')

    def get_submission_date(self):
        return self.created_time.date()

    def __unicode__(self):
        return self.title
