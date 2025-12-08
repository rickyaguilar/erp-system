from django import forms
from django.forms import formset_factory, inlineformset_factory
from .models import MaterialRequest, MaterialRequestItem


class MaterialRequestForm(forms.ModelForm):
    """Form for creating material purchase requests"""
    
    class Meta:
        model = MaterialRequest
        fields = [
            'project_name', 'project_location', 'site_supervisor',
            'purpose', 'delivery_date_needed'
        ]
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name'
            }),
            'project_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project location'
            }),
            'site_supervisor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Site supervisor name'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the purpose of this material request'
            }),
            'delivery_date_needed': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

        }
        labels = {
            'project_name': 'Project Name',
            'project_location': 'Project Location',
            'site_supervisor': 'Site Supervisor',
            'purpose': 'Purpose of Request',
            'delivery_date_needed': 'Required Delivery Date',

        }


class MaterialRequestItemForm(forms.ModelForm):
    """Form for individual material items"""
    
    def clean(self):
        """Custom validation for material request items"""
        cleaned_data = super().clean()
        
        # If this form is marked for deletion, skip validation
        if cleaned_data.get('DELETE'):
            return cleaned_data
            
        return cleaned_data
    
    class Meta:
        model = MaterialRequestItem
        fields = [
            'material_name', 'description', 'specification',
            'quantity', 'estimated_unit_price',
            'supplier_preference', 'notes'
        ]
        widgets = {
            'material_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'specification': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input',
                'step': '0.01',
                'min': '0'
            }),

            'estimated_unit_price': forms.NumberInput(attrs={
                'class': 'form-control price-input',
                'step': '0.01',
                'min': '0'
            }),
            'supplier_preference': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            })
        }
        labels = {
            'material_name': 'Material Name',
            'description': 'Description',
            'specification': 'Specification',
            'quantity': 'Quantity',

            'estimated_unit_price': 'Estimated Unit Price',
            'supplier_preference': 'Supplier Preference',
            'notes': 'Notes'
        }


class MaterialRequestItemFormSet(forms.BaseInlineFormSet):
    """Custom formset to handle validation of deleted items"""
    
    def clean(self):
        """Override clean to skip validation for forms marked for deletion"""
        if any(self.errors):
            return
            
        # Check if at least one form has material_name (basic check)
        has_valid_form = False
        for form in self.forms:
            if hasattr(form, 'cleaned_data') and form.cleaned_data:
                if not form.cleaned_data.get('DELETE') and form.cleaned_data.get('material_name'):
                    has_valid_form = True
                    break
        
        if not has_valid_form:
            raise forms.ValidationError('At least one material item is required.')

# Create a formset for multiple material items
MaterialItemFormSet = inlineformset_factory(
    MaterialRequest,
    MaterialRequestItem,
    form=MaterialRequestItemForm,
    extra=1,  # Start with one empty form
    can_delete=True,
    min_num=1,  # Require at least one item
    validate_min=True
)