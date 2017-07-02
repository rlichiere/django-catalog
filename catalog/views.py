import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponse
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
                    'project_capacities': project_capacities, 'participations': participations, 'request': self.request}
        else:
            raise Http404


class ParticipantDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/participant_detail.html'

    def get_context_data(self, **kwargs):
        request = self.request
        participant = Participant.objects.get(id=self.kwargs['pk'])
        capacities_selected = participant.capacities.all()
        print('capacities=%s' % capacities_selected)
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
            capacities_effective = list()
            for part in parts:
                if part.owner_validation and part.participant_validation:
                    if part.project not in projects_parts['effective']:
                        projects_parts['effective'].append(part.project)
                        parts_effective.append(part)
                        if not part.capacity in capacities_effective:
                            capacities_effective.append(part.capacity)
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
            result['capacities_selected'] = capacities_selected
            result['capacities_effective'] = capacities_effective
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
        effective_capacities = dict()
        selected_capacities = dict()
        invited_capacities = dict()
        purposed_capacities = dict()
        if capacity is not None:
            parts = Participation.objects.filter(capacity=capacity.id)\
                .order_by('capacity__label', 'participant__user__first_name', 'participant__user__last_name')
            effective_participations = list()
            effective_participants = list()
            selected_participations = list()
            selected_participants = list()
            invited_participations = list()
            invited_participants = list()
            purposed_participations = list()
            purposed_participants = list()
            for part in parts:
                if part.owner_validation and part.participant_validation:
                    if part.participant not in effective_participants:
                        effective_participants.append(part.participant)
                        effective_participations.append(part)
                elif part.owner_validation and not part.participant_validation:
                    if part.participant not in invited_participants:
                        invited_participants.append(part.participant)
                        invited_participations.append(part)
                elif (not part.owner_validation) and part.participant_validation:
                    if part.participant not in purposed_participants:
                        purposed_participants.append(part.participant)
                        purposed_participations.append(part)
            effective_capacities['participations'] = effective_participations
            effective_capacities['participants'] = effective_participants
            invited_capacities['participations'] = invited_participations
            invited_capacities['participants'] = invited_participants
            purposed_capacities['participations'] = purposed_participations
            purposed_capacities['participants'] = purposed_participants

            participants = Participant.objects.all()
            for participant in participants:
                part_caps = participant.capacities.filter(id=capacity.id)
                if part_caps.count() > 0:
                    selected_participations.append(part_caps)
                    selected_participants.append(participant)
            selected_capacities['participations'] = selected_participations
            selected_capacities['participants'] = selected_participants

            return {'capacity': capacity,
                    'effective_capacities': effective_capacities, 'invited_capacities': invited_capacities,
                    'purposed_capacities': purposed_capacities, 'selected_capacities': selected_capacities,
                    }
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
                if part.project.label == 'Star Truc':
                    print('%s, o_v:%s, p_v:%s, cap:%s' % (
                        part.project, part.owner_validation, part.participant_validation, part.capacity)
                          )
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
        print('len participations_propositions : %s' % len(result['participations_propositions']))
        result['my_projects'] = my_projects
        result['my_projects_invitations'] = my_projects_invitations
        result['my_projects_propositions'] = my_projects_propositions

        my_objects = Object.objects.filter(owner=Participant.objects.filter(user=self.request.user))
        result['my_objects'] = my_objects

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
            if param_2 == 'selected':
                for part in parts:
                    part_name = '%s %s' % (part.user.first_name, part.user.last_name)
                    part_caps = part.capacities.filter(id=param_1)
                    if part_caps.count() > 0:
                        participants_data.append({'id': part.id, 'label': part_name})
            elif param_2 == 'effective':
                for part in parts:
                    part_name = '%s %s' % (part.user.first_name, part.user.last_name)
                    participations = Participation.objects.filter(
                            participant=part,
                            owner_validation=True,
                            participant_validation=True,
                            capacity=param_1
                    )
                    if participations.count() > 0:
                        participants_data.append({'id': part.id, 'label': part_name})
            elif param_2 == 'off':
                for part in parts:
                    part_name = '%s %s' % (part.user.first_name, part.user.last_name)
                    participants_data.append({'id': part.id, 'label': part_name})
            result = dict()
            result['command'] = command
            result['status'] = 'success'
            result['data'] = participants_data
        else:
            result = {'command': command, 'status': 'error', 'message': 'unknown command'}
        return HttpResponse(json.dumps(result), status=200)


class CatalogView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)

        query_result = dict()
        query_result['actors'] = Actor.objects.all()
        query_result['decors'] = Decor.objects.all()
        query_result['accessories'] = Accessory.objects.all()
        query_result['locations'] = Location.objects.all()
        context['query_result'] = query_result
        return context

    def post(self, request):
        query_form = dict()
        query_result = dict()

        if 'check_all' in self.request.POST:
            query_form['check_all'] = 'on'
        else:
            query_form['check_all'] = 'off'

        if 'search_query' in self.request.POST:
            query = self.request.POST['search_query']
        else:
            query = ''
        query_form['query'] = query
        print('query received : %s' % query)

        if 'search_actors' in request.POST:
            query_form['search_actors'] = 'on'
            if query in ['*', '']:
                query_result['actors'] = Actor.objects.all()
            else:
                query_result['actors'] = Actor.objects.filter(
                        Q(label__contains=query) |
                        Q(owner__user__last_name__contains=query) |
                        Q(owner__user__first_name__contains=query)
                )
        else:
            query_form['search_actors'] = 'off'
            query_result['actors'] = None

        if 'search_decors' in request.POST:
            query_form['search_decors'] = 'on'
            if query in ['*', '']:
                query_result['decors'] = Decor.objects.all()
            else:
                query_result['decors'] = Decor.objects.filter(label__contains=query)
        else:
            query_form['search_decors'] = 'off'
            query_result['decors'] = None

        if 'search_accessories' in request.POST:
            query_form['search_accessories'] = 'on'
            if query in ['*', '']:
                query_result['accessories'] = Accessory.objects.all()
            else:
                query_result['accessories'] = Accessory.objects.filter(label__contains=query)
        else:
            query_form['search_accessories'] = 'off'
            query_result['decors'] = None

        if 'search_locations' in request.POST:
            query_form['search_locations'] = 'on'
            if query in ['*', '']:
                query_result['locations'] = Location.objects.all()
            else:
                query_result['locations'] = Location.objects.filter(label__contains=query)
        else:
            query_form['search_locations'] = 'off'
            query_result['locations'] = None

        return render(request, self.template_name, {'query_result': query_result, 'query_form': query_form})


class CatalogActorView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/catalog_actor.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogActorView, self).get_context_data(**kwargs)
        context['actor'] = Actor.objects.get(id=kwargs['pk'])
        return context


class CatalogDecorView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/catalog_decor.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogDecorView, self).get_context_data(**kwargs)
        context['decor'] = Decor.objects.get(id=kwargs['pk'])
        return context


class CatalogAccessoryView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/catalog_accessory.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogAccessoryView, self).get_context_data(**kwargs)
        context['accessory'] = Accessory.objects.get(id=kwargs['pk'])
        return context


class CatalogLocationView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/catalog_location.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogLocationView, self).get_context_data(**kwargs)
        context['location'] = Location.objects.get(id=kwargs['pk'])
        return context
