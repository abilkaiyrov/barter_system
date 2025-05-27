from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

# DRF
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import AdSerializer, ProposalSerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# HTML Views
def ad_list(request):
    ads = Ad.objects.all()

    query = request.GET.get('q')
    if query:
        ads = ads.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    category = request.GET.get('category')
    if category:
        ads = ads.filter(category__icontains=category)

    condition = request.GET.get('condition')
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'query': query,
        'category': category,
        'condition': condition
    })

@login_required
def ad_create(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        ad = form.save(commit=False)
        ad.user = request.user
        ad.save()
        return redirect('ad_list')
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def proposal_create(request):
    form = ProposalForm(request.POST or None)
    if form.is_valid():
        proposal = form.save()
        return redirect('ad_list')
    return render(request, 'ads/proposal_form.html', {'form': form})

@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором этого объявления.")

    form = AdForm(request.POST or None, instance=ad)
    if form.is_valid():
        form.save()
        return redirect('ad_detail', pk=ad.pk)

    return render(request, 'ads/ad_form.html', {'form': form, 'ad': ad})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")

    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user
    ) | ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    )
    return render(request, 'ads/proposal_list.html', {'proposals': proposals})

@login_required
def proposal_update(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)

    if proposal.ad_receiver.user != request.user:
        return HttpResponseForbidden("Вы не получатель этого предложения.")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'declined']:
            proposal.status = new_status
            proposal.save()
        return redirect('proposal_list')

    return render(request, 'ads/proposal_update_form.html', {'proposal': proposal})

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    )

    status = request.GET.get('status')
    sender_id = request.GET.get('sender_id')
    receiver_id = request.GET.get('receiver_id')

    if status:
        proposals = proposals.filter(status=status)
    if sender_id:
        proposals = proposals.filter(ad_sender__user__id=sender_id)
    if receiver_id:
        proposals = proposals.filter(ad_receiver__user__id=receiver_id)

    return render(request, 'ads/proposal_list.html', {'proposals': proposals})

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

@login_required
def ad_create(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        ad = form.save(commit=False)
        ad.user = request.user
        ad.save()
        return redirect('ad_detail', pk=ad.pk)
    return render(request, 'ads/ad_form.html', {'form': form})