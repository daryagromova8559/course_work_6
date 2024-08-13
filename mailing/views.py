from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.forms import MailingForm, MessageForm, CustomersForm, MailingManagerForm
from mailing.models import Mailing, Customers, Message, Mailing_attempt
from mailing.services import get_qs_from_cache


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/home.html'


    def get_queryset(self):
       return get_qs_from_cache(qs=Message.objects.filter()[:20], key='message_list')

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(MessageListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['is_active'] = Mailing.objects.filter(is_active=True)
        context['customer'] = Customers.objects.all()
        context['message'] = Message.objects.all()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        user = self.request.user
        self.object.owner = user
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        mailing_template = form.save()
        self.object = form.save()
        self.object.owner = self.request.user
        mailing_template.owner = self.object.owner
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            mailing_template.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            MailingFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        elif user.is_staff or user.superuser:
            MailingFormset = inlineformset_factory(Message, Mailing, form=MailingManagerForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        massage_template = form.save()
        self.object = form.save()
        self.object.owner = self.request.user
        massage_template.owner = self.object.owner
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            massage_template.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"


def settings_toggle_active(request, pk):
    mailing_item = get_object_or_404(Mailing_attempt, pk=pk)
    if mailing_item.is_active is True:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
        mailing_item.save()
    return redirect(reverse('mailing:home'))


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersCreateView(LoginRequiredMixin, CreateView):
    model = Customers
    form_class = CustomersForm
    success_url = reverse_lazy('mailing:home')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        customer = form.save()
        user = self.request.user
        customer.owner = user
        customer.save()
        return super().form_valid(form)


class CustomersUpdateView(LoginRequiredMixin, UpdateView):
    model = Customers
    form_class = CustomersForm
    success_url = reverse_lazy('mailing:customers_list')
    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        customer = form.save()
        user = self.request.user
        customer.owner = user
        customer.save()
        return super().form_valid(form)


class CustomersDeleteView(LoginRequiredMixin, DeleteView):
    model = Customers
    success_url = reverse_lazy('mailing:customers_list')
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'mailing/customers_detail.html'
    login_url = "users:login"
    redirect_field_name = "redirect_to"


class CustomersListView(ListView):
    model = Customers
    template_name = 'mailing/customers_list.html'

    def get_queryset(self):
        return get_qs_from_cache(qs=Customers.objects.all(), key='customers_list')

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        user = self.request.user
        self.object.owner = user
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)


