"""
Data Form with Validation - Siemens iX

This example demonstrates a comprehensive form application with validation
following Panel best practices:
- Parameter-driven validation using param.Parameterized
- Real-time validation feedback
- Material UI components with Siemens iX theming
- Proper error handling and user feedback
- Form submission and data processing

Run with:
    panel serve data_form.py --dev --show
Or:
    python data_form.py
"""

import panel as pn
import panel_material_ui as pmui
import param
import re
import datetime
from typing import Dict, List
from panel_siemens_ix import configure


class EquipmentRegistrationForm(param.Parameterized):
    """
    Equipment registration form with comprehensive validation.
    
    This class demonstrates Panel's parameter-driven validation approach
    where validation logic is centralized and reactive.
    """
    
    # Equipment basic information
    equipment_name = param.String(
        default="",
        doc="Name of the equipment"
    )
    equipment_type = param.Selector(
        default="Motor",
        objects=["Motor", "Pump", "Conveyor", "Robot", "Sensor", "Controller"],
        doc="Type of equipment"
    )
    manufacturer = param.String(
        default="",
        doc="Equipment manufacturer"
    )
    model_number = param.String(
        default="",
        doc="Model/serial number"
    )
    
    # Technical specifications
    voltage = param.Number(
        default=400.0,
        bounds=(0, 1000),
        doc="Operating voltage (V)"
    )
    power_rating = param.Number(
        default=5.0,
        bounds=(0, 1000),
        doc="Power rating (kW)"
    )
    installation_date = param.Date(
        default=datetime.date.today(),
        doc="Equipment installation date"
    )
    
    # Location and contact
    location = param.Selector(
        default="Building A",
        objects=["Building A", "Building B", "Building C", "Warehouse", "Outdoor"],
        doc="Equipment location"
    )
    department = param.String(
        default="",
        doc="Responsible department"
    )
    contact_email = param.String(
        default="",
        doc="Contact email address"
    )
    
    # Multi-select options
    maintenance_types = param.ListSelector(
        default=["Preventive"],
        objects=["Preventive", "Predictive", "Corrective", "Emergency"],
        doc="Required maintenance types"
    )
    safety_features = param.ListSelector(
        default=[],
        objects=["Emergency Stop", "Safety Guard", "Lockout/Tagout", "Warning Lights", "Audible Alarm"],
        doc="Safety features present"
    )
    
    # Additional options
    critical_equipment = param.Boolean(
        default=False,
        doc="Mark as critical equipment"
    )
    requires_certification = param.Boolean(
        default=False,
        doc="Requires special certification"
    )
    notes = param.String(
        default="",
        doc="Additional notes"
    )
    
    # Validation state
    validation_errors = param.Dict(default={}, doc="Current validation errors")
    is_valid = param.Boolean(default=False, doc="Overall form validity")
    
    def __init__(self, **params):
        super().__init__(**params)
        # Validate on initialization
        self._validate_form()
    
    @param.depends(
        "equipment_name", "manufacturer", "model_number", "department", 
        "contact_email", "voltage", "power_rating", "installation_date",
        watch=True
    )
    def _validate_form(self):
        """
        Comprehensive form validation.
        
        Uses watch=True to automatically validate when parameters change.
        This is appropriate for validation as it's a side effect, not UI update.
        """
        errors = {}
        
        # Required field validation
        if not self.equipment_name.strip():
            errors['equipment_name'] = "Equipment name is required"
        elif len(self.equipment_name) < 3:
            errors['equipment_name'] = "Equipment name must be at least 3 characters"
        
        if not self.manufacturer.strip():
            errors['manufacturer'] = "Manufacturer is required"
        
        if not self.model_number.strip():
            errors['model_number'] = "Model number is required"
        elif len(self.model_number) < 2:
            errors['model_number'] = "Model number must be at least 2 characters"
        
        if not self.department.strip():
            errors['department'] = "Department is required"
        
        # Email validation
        if not self.contact_email.strip():
            errors['contact_email'] = "Contact email is required"
        elif not self._is_valid_email(self.contact_email):
            errors['contact_email'] = "Please enter a valid email address"
        
        # Technical specification validation
        if self.voltage <= 0:
            errors['voltage'] = "Voltage must be greater than 0"
        elif self.voltage > 1000:
            errors['voltage'] = "Voltage cannot exceed 1000V"
        
        if self.power_rating <= 0:
            errors['power_rating'] = "Power rating must be greater than 0"
        
        # Date validation
        if self.installation_date > datetime.date.today():
            errors['installation_date'] = "Installation date cannot be in the future"
        elif self.installation_date < datetime.date(1900, 1, 1):
            errors['installation_date'] = "Installation date seems too old"
        
        # Business logic validation
        if self.critical_equipment and not self.safety_features:
            errors['safety_features'] = "Critical equipment must have safety features"
        
        if self.power_rating > 100 and not self.requires_certification:
            errors['requires_certification'] = "High power equipment typically requires certification"
        
        # Update validation state
        self.validation_errors = errors
        self.is_valid = len(errors) == 0
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_form_data(self) -> Dict:
        """Export form data as dictionary."""
        return {
            'equipment_name': self.equipment_name,
            'equipment_type': self.equipment_type,
            'manufacturer': self.manufacturer,
            'model_number': self.model_number,
            'voltage': self.voltage,
            'power_rating': self.power_rating,
            'installation_date': self.installation_date.isoformat(),
            'location': self.location,
            'department': self.department,
            'contact_email': self.contact_email,
            'maintenance_types': self.maintenance_types,
            'safety_features': self.safety_features,
            'critical_equipment': self.critical_equipment,
            'requires_certification': self.requires_certification,
            'notes': self.notes
        }
    
    def reset_form(self):
        """Reset form to default values."""
        self.param.update(
            equipment_name="",
            equipment_type="Motor",
            manufacturer="",
            model_number="",
            voltage=400.0,
            power_rating=5.0,
            installation_date=datetime.date.today(),
            location="Building A",
            department="",
            contact_email="",
            maintenance_types=["Preventive"],
            safety_features=[],
            critical_equipment=False,
            requires_certification=False,
            notes=""
        )


class FormApplication(pn.viewable.Viewer):
    """
    Main form application with Material UI components and Siemens iX theming.
    
    This class demonstrates how to build forms with proper validation
    feedback and user experience patterns.
    """
    
    submission_count = param.Integer(default=0, doc="Number of successful submissions")
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # Create form model
        self.form_model = EquipmentRegistrationForm()
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_widgets()
            self._create_layout()
    
    def _create_widgets(self):
        """Create form widgets with validation feedback."""
        
        # Basic Information Section
        self._equipment_name = self._create_validated_input(
            self.form_model.param.equipment_name,
            "Equipment Name *",
            "Enter equipment name...",
            'equipment_name'
        )
        
        self._equipment_type = pmui.Select.from_param(
            self.form_model.param.equipment_type,
            name="Equipment Type *"
        )
        
        self._manufacturer = self._create_validated_input(
            self.form_model.param.manufacturer,
            "Manufacturer *",
            "e.g., Siemens, ABB, Schneider...",
            'manufacturer'
        )
        
        self._model_number = self._create_validated_input(
            self.form_model.param.model_number,
            "Model Number *",
            "Enter model/serial number...",
            'model_number'
        )
        
        # Technical Specifications Section
        self._voltage = self._create_validated_number_input(
            self.form_model.param.voltage,
            "Operating Voltage (V) *",
            'voltage'
        )
        
        self._power_rating = self._create_validated_number_input(
            self.form_model.param.power_rating,
            "Power Rating (kW) *",
            'power_rating'
        )
        
        self._installation_date = self._create_validated_date_input(
            self.form_model.param.installation_date,
            "Installation Date *",
            'installation_date'
        )
        
        # Location and Contact Section
        self._location = pmui.Select.from_param(
            self.form_model.param.location,
            name="Location *"
        )
        
        self._department = self._create_validated_input(
            self.form_model.param.department,
            "Department *",
            "e.g., Production, Maintenance...",
            'department'
        )
        
        self._contact_email = self._create_validated_input(
            self.form_model.param.contact_email,
            "Contact Email *",
            "user@company.com",
            'contact_email'
        )
        
        # Multi-select options
        self._maintenance_types = pmui.MultiSelect.from_param(
            self.form_model.param.maintenance_types,
            name="Maintenance Types *"
        )
        
        self._safety_features = self._create_validated_multiselect(
            self.form_model.param.safety_features,
            "Safety Features",
            'safety_features'
        )
        
        # Additional Options
        self._critical_equipment = pmui.Switch.from_param(
            self.form_model.param.critical_equipment,
            name="Critical Equipment"
        )
        
        self._requires_certification = self._create_validated_switch(
            self.form_model.param.requires_certification,
            "Requires Certification",
            'requires_certification'
        )
        
        self._notes = pmui.TextAreaInput.from_param(
            self.form_model.param.notes,
            name="Additional Notes",
            placeholder="Enter any additional information...",
            height=100
        )
        
        # Form actions
        self._submit_button = pmui.Button(
            name="Register Equipment",
            button_type="primary",
            icon="save",
            on_click=self._submit_form,
            disabled=pn.bind(lambda valid: not valid, self.form_model.param.is_valid)
        )
        
        self._reset_button = pmui.Button(
            name="Reset Form",
            button_type="secondary",
            variant="outlined",
            icon="refresh",
            on_click=self._reset_form
        )
        
        # Validation summary
        self._validation_summary = pmui.Alert(
            object=self.validation_summary_display,
            alert_type="error",
            visible=pn.bind(lambda errors: len(errors) > 0, self.form_model.param.validation_errors)
        )
    
    def _create_validated_input(self, param_ref, name, placeholder, error_key):
        """Create text input with validation feedback."""
        input_widget = pmui.TextInput.from_param(
            param_ref,
            name=name,
            placeholder=placeholder
        )
        
        # Add error styling - in a real app, you might use sx prop for styling
        return pmui.Column(
            input_widget,
            pmui.Typography(
                object=pn.bind(lambda errors: errors.get(error_key, ""), self.form_model.param.validation_errors),
                variant="caption",
                styles={"color": "error.main", "marginTop": "4px"},
                visible=pn.bind(lambda errors: error_key in errors, self.form_model.param.validation_errors)
            )
        )
    
    def _create_validated_number_input(self, param_ref, name, error_key):
        """Create number input with validation feedback."""
        input_widget = pmui.FloatInput.from_param(param_ref, name=name)
        
        return pmui.Column(
            input_widget,
            pmui.Typography(
                object=pn.bind(lambda errors: errors.get(error_key, ""), self.form_model.param.validation_errors),
                variant="caption",
                styles={"color": "error.main", "marginTop": "4px"},
                visible=pn.bind(lambda errors: error_key in errors, self.form_model.param.validation_errors)
            )
        )
    
    def _create_validated_date_input(self, param_ref, name, error_key):
        """Create date input with validation feedback."""
        input_widget = pmui.DatePicker.from_param(param_ref, name=name)
        
        return pmui.Column(
            input_widget,
            pmui.Typography(
                object=pn.bind(lambda errors: errors.get(error_key, ""), self.form_model.param.validation_errors),
                variant="caption",
                styles={"color": "error.main", "marginTop": "4px"},
                visible=pn.bind(lambda errors: error_key in errors, self.form_model.param.validation_errors)
            )
        )
    
    def _create_validated_multiselect(self, param_ref, name, error_key):
        """Create multi-select with validation feedback."""
        input_widget = pmui.MultiSelect.from_param(param_ref, name=name)
        
        return pmui.Column(
            input_widget,
            pmui.Typography(
                object=pn.bind(lambda errors: errors.get(error_key, ""), self.form_model.param.validation_errors),
                variant="caption",
                styles={"color": "error.main", "marginTop": "4px"},
                visible=pn.bind(lambda errors: error_key in errors, self.form_model.param.validation_errors)
            )
        )
    
    def _create_validated_switch(self, param_ref, name, error_key):
        """Create switch with validation feedback."""
        input_widget = pmui.Switch.from_param(param_ref, name=name)
        
        return pmui.Column(
            input_widget,
            pmui.Typography(
                object=pn.bind(lambda errors: errors.get(error_key, ""), self.form_model.param.validation_errors),
                variant="caption",
                styles={"color": "error.main", "marginTop": "4px"},
                visible=pn.bind(lambda errors: error_key in errors, self.form_model.param.validation_errors)
            )
        )
    
    def _create_layout(self):
        """Create the main form layout."""
        
        # Header
        header = pmui.Paper(
            pmui.Typography("🏭 Equipment Registration Form", variant="h4", styles={"marginBottom": "10px"}),
            pmui.Typography(
                "Register new industrial equipment with comprehensive specifications and validation.",
                variant="body1"
            ),
            styles={"padding": "30px", "marginBottom": "20px"}
        )
        
        # Form sections
        basic_info_section = pmui.Card(
            pmui.Typography("Basic Information", variant="h6", styles={"marginBottom": "20px"}),
            pmui.Row(self._equipment_name, self._equipment_type),
            pmui.Row(self._manufacturer, self._model_number),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
        
        tech_specs_section = pmui.Card(
            pmui.Typography("Technical Specifications", variant="h6", styles={"marginBottom": "20px"}),
            pmui.Row(self._voltage, self._power_rating),
            self._installation_date,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
        
        location_contact_section = pmui.Card(
            pmui.Typography("Location & Contact", variant="h6", styles={"marginBottom": "20px"}),
            pmui.Row(self._location, self._department),
            self._contact_email,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
        
        options_section = pmui.Card(
            pmui.Typography("Options & Features", variant="h6", styles={"marginBottom": "20px"}),
            self._maintenance_types,
            self._safety_features,
            pmui.Row(self._critical_equipment, self._requires_certification),
            self._notes,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
        
        # Form actions
        actions_section = pmui.Paper(
            self._validation_summary,
            pmui.Row(
                self._submit_button,
                self._reset_button,
                styles={"justifyContent": "center", "gap": "20px"}
            ),
            styles={"padding": "20px", "textAlign": "center"}
        )
        
        # Main layout
        self._layout = pmui.Container(
            header,
            basic_info_section,
            tech_specs_section,
            location_contact_section,
            options_section,
            actions_section,
            width_option="md"
        )
    
    @param.depends("form_model.validation_errors")
    def validation_summary_display(self):
        """Display validation errors summary."""
        errors = self.form_model.validation_errors
        if not errors:
            return ""
        
        error_list = "\n".join([f"• {error}" for error in errors.values()])
        return f"Please fix the following errors:\n{error_list}"
    
    def _submit_form(self, event):
        """Handle form submission."""
        if self.form_model.is_valid:
            # Process form data
            form_data = self.form_model.get_form_data()
            self.submission_count += 1
            
            # Show success notification
            if hasattr(pn.state, 'notifications'):
                pn.state.notifications.success(
                    f"Equipment '{form_data['equipment_name']}' registered successfully! "
                    f"(Submission #{self.submission_count})",
                    duration=4000
                )
            
            # Reset form after successful submission
            self.form_model.reset_form()
        else:
            # Show validation error notification
            if hasattr(pn.state, 'notifications'):
                pn.state.notifications.error(
                    "Please fix validation errors before submitting.",
                    duration=3000
                )
    
    def _reset_form(self, event):
        """Handle form reset."""
        self.form_model.reset_form()
        
        if hasattr(pn.state, 'notifications'):
            pn.state.notifications.info("Form reset to default values.", duration=2000)
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """Create a servable form application."""
        instance = cls(**params)
        
        # Form validation info for sidebar
        validation_info = pmui.Column(
            pmui.Typography("Form Validation", variant="h6"),
            pmui.Typography(
                "This form demonstrates comprehensive validation patterns:",
                variant="body2",
                styles={"marginBottom": "15px"}
            ),
            pmui.Alert(
                object="✅ Real-time validation feedback",
                alert_type="success",
                styles={"marginBottom": "10px"}
            ),
            pmui.Alert(
                object="📧 Email format validation",
                alert_type="info",
                styles={"marginBottom": "10px"}
            ),
            pmui.Alert(
                object="🔒 Business logic validation",
                alert_type="warning",
                styles={"marginBottom": "10px"}
            ),
            pmui.Typography(
                f"Successful submissions: {instance.submission_count}",
                variant="body2",
                styles={"marginTop": "15px"}
            )
        )
        
        page = pmui.Page(
            title="Equipment Registration - Siemens iX",
            main=[instance],
            sidebar=[validation_info],
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension(notifications=True)

# Apply Siemens iX configuration
configure()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python data_form.py`
    FormApplication.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve data_form.py --port 5007 --dev --show`
    FormApplication.create_app().servable()