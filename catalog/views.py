import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from .models import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):

        capacities = Capacity.objects.all().order_by('label')
        participants = Participant.objects.all().order_by('user__first_name', 'user__last_name')
        projects = Project.objects.all().order_by('label')

        return {'capacities': capacities, 'participants': participants, 'projects': projects}


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/projects.html'

    def get_context_data(self, **kwargs):
        projects = Project.objects.all()

        return {'projects': projects}


class ProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/project_detail.html'

    def get_context_data(self, **kwargs):
        project = Project.objects.get(id=self.kwargs['pk'])
        if project is not None:
            parts = Participation.objects.filter(project=project.id)\
                .order_by('capacity__label', 'participant__user__first_name', 'participant__user__last_name')
            project_capacities = list()
            participations = list()
            for part in parts:
                cap = {'name': part.capacity.name, 'label': part.capacity.label,
                       'id': part.capacity.id}
                if cap not in project_capacities:
                    project_capacities.append(cap)
                participations.append(part)
            capacities = Capacity.objects.all()
            participants = Participant.objects.all()
            return {'project': project, 'capacities': capacities, 'participants': participants,
                    'project_capacities': project_capacities, 'participations': participations}
        else:
            raise Http404


class ParticipantDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/participant_detail.html'

    def get_context_data(self, **kwargs):
        request = self.request
        participant = Participant.objects.get(id=self.kwargs['pk'])
        capacities = participant.capacities.all()
        print('capacities=%s' % capacities)
        if participant is not None:
            parts = Participation.objects.filter(participant=participant.id)\
                .order_by('capacity__label', 'participant__user__first_name', 'participant__user__last_name')
            projects = list()
            projects_parts = dict()
            projects_parts['effective'] = list()
            projects_parts['invitations'] = list()
            projects_parts['propositions'] = list()
            parts_effective = list()
            parts_invitations = list()
            parts_propositions = list()
            for part in parts:
                if part.owner_validation and part.participant_validation:
                    if part.project not in projects_parts['effective']:
                        projects_parts['effective'].append(part.project)
                        parts_effective.append(part)
                if part.owner_validation and not part.participant_validation:
                    if part.project not in projects_parts['invitations']:
                        projects_parts['invitations'].append(part.project)
                        parts_invitations.append(part)
                if (not part.owner_validation) and part.participant_validation:
                    if part.project not in projects_parts['propositions']:
                        projects_parts['propositions'].append(part.project)
                        parts_propositions.append(part)

            result = dict()
            result['request'] = request
            result['participant'] = participant
            result['capacities'] = capacities
            result['projects'] = projects
            result['participations'] = parts
            result['projects_participations'] = projects_parts
            result['participations_effective'] = parts_effective
            result['participations_invitations'] = parts_invitations
            result['participations_propositions'] = parts_propositions

            return result
        else:
            raise Http404


class CapacityDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/capacity_detail.html'

    def get_context_data(self, **kwargs):
        capacity = Capacity.objects.get(id=self.kwargs['pk'])
        if capacity is not None:
            parts = Participation.objects.filter(capacity=capacity.id)\
                .order_by('capacity__label', 'participant__user__first_name', 'participant__user__last_name')
            participations = list()
            participants = list()
            for part in parts:
                if part.owner_validation and part.participant_validation:
                    if part.participant not in participants:
                        participants.append(part.participant)
                    participations.append(part)
            return {'capacity': capacity,
                    'participants': participants, 'participations': participations}
        else:
            raise Http404


class MyView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/my.html'

    def get_context_data(self, **kwargs):

        created_projects = Project.objects.filter(creator=self.request.user)
        projects_parts = dict()
        projects_parts['effective'] = list()
        projects_parts['invitations'] = list()
        projects_parts['propositions'] = list()
        parts_effective = list()
        parts_invitations = list()
        parts_propositions = list()
        my_projects = dict()
        my_projects['invitations'] = list()
        my_projects['propositions'] = list()
        my_projects_invitations = list()
        my_projects_propositions = list()
        parts = Participation.objects.all()\
            .order_by('capacity__label', 'participant__user__first_name', 'participant__user__last_name')
        for part in parts:
            if part.participant.user == self.request.user:
                if part.owner_validation and part.participant_validation:
                    if part.project not in projects_parts['effective']:
                        projects_parts['effective'].append(part.project)
                        parts_effective.append(part)
                if part.owner_validation and not part.participant_validation:
                    if part.project not in projects_parts['invitations']:
                        projects_parts['invitations'].append(part.project)
                        parts_invitations.append(part)
                if (not part.owner_validation) and part.participant_validation:
                    if part.project not in projects_parts['propositions']:
                        projects_parts['propositions'].append(part.project)
                        parts_propositions.append(part)

            elif part.project.creator == self.request.user:
                if part.owner_validation and not part.participant_validation:
                    if part.project not in my_projects['invitations']:
                        my_projects['invitations'].append(part.project)
                    my_projects_invitations.append(part)
                if (not part.owner_validation) and part.participant_validation:
                    if part.project not in my_projects['propositions']:
                        my_projects['propositions'].append(part.project)
                    my_projects_propositions.append(part)

        result = dict()
        result['created_projects'] = created_projects
        result['participations'] = parts
        result['projects_participations'] = projects_parts
        result['participations_effective'] = parts_effective
        result['participations_invitations'] = parts_invitations
        result['participations_propositions'] = parts_propositions
        result['my_projects'] = my_projects
        result['my_projects_invitations'] = my_projects_invitations
        result['my_projects_propositions'] = my_projects_propositions
        return result


class CommandView(LoginRequiredMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CommandView, self).dispatch(*args, **kwargs)

    def post(self, request):
        command = request.POST['command']
        param_1 = request.POST['param_1']
        param_2 = request.POST['param_2']
        param_3 = request.POST['param_3']
        print('command:%s, param_1:%s, param_2:%s, param_3:%s' % (command, param_1, param_2, param_3))
        result = {'command': command, 'status': 'error', 'message': 'unknown command'}

        if command == 'project_archive':
            project = Project.objects.get(id=param_1)
            project.status = 'archive'
            project.save()
        elif command == 'project_reactivate':
            project = Project.objects.get(id=param_1)
            project.status = 'active'
            project.save()
        elif command == 'participation_proposition':
            project = Project.objects.get(id=param_1)
            capacity = Capacity.objects.get(id=param_2)
            participant = Participant.objects.filter(user=request.user.id).first()
            if participant is None:
                print('participant must be created')
                participant = Participant(user=request.user)
                participant.save()
            else:
                print('participant exists')
            print('participant.id : %s' % participant.id)
            part = Participation(project=project, capacity=capacity, participant=participant,
                                 owner_validation=False, participant_validation=True)
            part.save()
            result = {'command': command, 'status': 'success', 'message': ''}
        elif command == 'participation_invitation':
            project = Project.objects.get(id=param_1)
            capacity = Capacity.objects.get(id=param_2)
            participant = Participant.objects.get(id=param_3)
            if participant is None:
                print('participant must be created')
                participant = Participant(user=request.user)
                participant.save()
            else:
                print('participant exists')
            print('participant.id : %s' % participant.id)
            part = Participation(project=project, capacity=capacity, participant=participant,
                                 owner_validation=True, participant_validation=False)
            part.save()
            result = {'command': command, 'status': 'success', 'message': ''}
        elif command == 'participation_proposition_validated':
            part = Participation.objects.get(id=param_1)
            part.owner_validation = True
            part.save()
        elif command == 'participation_proposition_denied':
            part = Participation.objects.get(id=param_1)
            part.delete()
        elif command == 'participation_proposition_remove':
            part = Participation.objects.get(id=param_1)
            part.delete()
        elif command == 'participation_invitation_validated':
            part = Participation.objects.get(id=param_1)
            part.participant_validation = True
            part.save()
            result = {'command': command, 'status': 'success', 'message': ''}
        elif command == 'participation_invitation_denied':
            part = Participation.objects.get(id=param_1)
            part.delete()
            result = {'command': command, 'status': 'success', 'message': ''}
        elif command == 'participation_invitation_canceled':
            part = Participation.objects.get(id=param_1)
            part.delete()
            result = {'command': command, 'status': 'success', 'message': ''}
        elif command == 'participants_by_capacity':
            parts = Participant.objects.all().order_by('user__first_name', 'user__last_name')
            participants_data = list()
            if param_2 == 'on':
                for part in parts:
                    part_name = '%s %s' % (part.user.first_name, part.user.last_name)
                    part_caps = part.capacities.filter(id=param_1)
                    if part_caps.count() > 0:
                        participants_data.append({'id': part.id, 'label': part_name})

            participants_data.append({'id': '', 'label': '------'})
            for part in parts:
                part_name = '%s %s' % (part.user.first_name, part.user.last_name)
                if not {'id': part.id, 'label': part_name} in participants_data:
                    participants_data.append({'id': part.id, 'label': part_name})
            result = dict()
            result['command'] = command
            result['status'] = 'success'
            result['data'] = participants_data
        else:
            result = {'command': command, 'status': 'error', 'message': 'unknown command'}
        return HttpResponse(json.dumps(result), status=200)
