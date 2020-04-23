from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    mult_pizza_form = MultiplePizzaForm()
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            topping1 = filled_form.cleaned_data['topping1']
            topping2 = filled_form.cleaned_data['topping2']
            size = filled_form.cleaned_data['size']
            message = f'Your order for {size} {topping1} and {topping2} has been taken'
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'pizzaform':new_form,'message':message,'mult_pizza_form':mult_pizza_form})
    else:        
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform':form,'mult_pizza_form':mult_pizza_form})

def pizzas(request):
    default_number = 2
    filled_mult_pizza = MultiplePizzaForm(request.GET)
    if filled_mult_pizza.is_valid():
        default_number = filled_mult_pizza.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm,extra=default_number)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data)
            message = 'Pizzas have been ordered'
        else:
            message = f'Order was not processed, try again, {filled_formset.data}'
        return render(request,'pizza/pizzas.html',{'formset':formset,'message':message})
    else:
        return render(request,'pizza/pizzas.html',{'formset':formset})